import os
import json
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models.model_version import ModelVersion
from app.auth.decorators import roles_required
from app.audit.services import log_action
from app.ml.dataset_loader import load_dataset
from app.ml.dataset_validator import validate_dataset
from app.ml.train import train_model, compute_file_hash

model_management_bp = Blueprint('model_management', __name__, url_prefix='/model')

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml', 'artifacts')


@model_management_bp.route('/')
@login_required
@roles_required('Administrator')
def index():
    versions = ModelVersion.query.order_by(ModelVersion.created_at.desc()).all()
    metrics_path = os.path.join(ARTIFACTS_DIR, 'metrics.json')
    metrics = None
    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)
    return render_template('model_management/index.html', versions=versions, metrics=metrics)


@model_management_bp.route('/latih', methods=['POST'])
@login_required
@roles_required('Administrator')
def train():
    dataset_path = current_app.config['DATASET_PATH']
    if not os.path.exists(dataset_path):
        flash(f'File dataset tidak ditemukan: {dataset_path}. Pastikan file sudah diunggah.', 'error')
        return redirect(url_for('model_management.index'))

    try:
        df = load_dataset(dataset_path)
        is_valid, errors = validate_dataset(df)
        if not is_valid:
            for err in errors:
                flash(err, 'error')
            return redirect(url_for('model_management.index'))

        result = train_model(df, dataset_path)
        metadata = result['metadata']
        metrics = result['metrics']

        # Nonaktifkan semua model sebelumnya
        ModelVersion.query.update({'is_active': False})

        version = ModelVersion(
            model_name=metadata['model_name'],
            version=metadata['model_version'],
            algorithm='CategoricalNB',
            artifact_path=result['pipeline_path'],
            dataset_filename=metadata['dataset_filename'],
            dataset_hash=metadata.get('dataset_hash'),
            training_date=__import__('datetime').datetime.utcnow(),
            training_data_count=metadata['training_rows'],
            testing_data_count=metadata['testing_rows'],
            accuracy=metrics['accuracy'],
            precision_macro=metrics['precision_macro'],
            recall_macro=metrics['recall_macro'],
            f1_macro=metrics['f1_macro'],
            best_alpha=metadata['best_alpha'],
            metrics_json=json.dumps(metrics, ensure_ascii=False),
            is_active=True
        )
        db.session.add(version)
        db.session.commit()

        log_action(current_user.id, 'train_model', 'ModelVersion', version.id,
                   f"Model versi {version.version} berhasil dilatih. Accuracy: {metrics['accuracy']:.4f}",
                   ip_address=request.remote_addr)

        flash(f'Model berhasil dilatih. Accuracy: {metrics["accuracy"]:.2%}, F1-Macro: {metrics["f1_macro"]:.4f}', 'success')
    except Exception as e:
        flash(f'Gagal melatih model: {str(e)}', 'error')

    return redirect(url_for('model_management.index'))


@model_management_bp.route('/<int:version_id>/aktifkan', methods=['POST'])
@login_required
@roles_required('Administrator')
def activate(version_id):
    ModelVersion.query.update({'is_active': False})
    version = ModelVersion.query.get_or_404(version_id)
    version.is_active = True
    db.session.commit()
    flash(f'Model versi {version.version} diaktifkan.', 'success')
    return redirect(url_for('model_management.index'))


@model_management_bp.route('/evaluasi')
@login_required
@roles_required('Administrator')
def evaluation():
    active_model = ModelVersion.query.filter_by(is_active=True).first()
    metrics = None
    confusion_matrix_exists = False

    metrics_path = os.path.join(ARTIFACTS_DIR, 'metrics.json')
    cm_path = os.path.join(ARTIFACTS_DIR, 'confusion_matrix.png')

    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)
    confusion_matrix_exists = os.path.exists(cm_path)

    return render_template('model_management/evaluation.html',
                           active_model=active_model,
                           metrics=metrics,
                           confusion_matrix_exists=confusion_matrix_exists)

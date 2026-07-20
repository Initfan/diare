from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models.examination import Examination
from app.models.prediction import Prediction
from app.models.clinical_validation import ClinicalValidation
from app.validations.forms import ValidationForm
from app.auth.decorators import roles_required
from app.audit.services import log_action

validations_bp = Blueprint('validations', __name__, url_prefix='/validasi')


@validations_bp.route('/')
@login_required
@roles_required('Dokter', 'Administrator')
def index():
    page = request.args.get('page', 1, type=int)
    examinations = (
        Examination.query
        .filter_by(status='waiting_validation')
        .order_by(Examination.submitted_at.asc())
        .paginate(page=page, per_page=15, error_out=False)
    )
    return render_template('validations/index.html', examinations=examinations)


@validations_bp.route('/<int:exam_id>', methods=['GET', 'POST'])
@login_required
@roles_required('Dokter', 'Administrator')
def validate(exam_id):
    examination = Examination.query.get_or_404(exam_id)
    prediction = Prediction.query.filter_by(examination_id=exam_id).first_or_404()

    if examination.status == 'validated':
        flash('Pemeriksaan ini sudah divalidasi dan dikunci.', 'info')
        return redirect(url_for('validations.view', exam_id=exam_id))

    form = ValidationForm()
    if form.validate_on_submit():
        decision = form.decision.data
        override_reason = form.override_reason.data

        # Jika override wajib ada alasan
        if decision == 'overridden' and not override_reason:
            flash('Alasan perubahan wajib diisi jika mengubah hasil model.', 'error')
            return render_template('validations/validate.html',
                                   form=form, examination=examination, prediction=prediction)

        final_class = form.final_class.data if decision == 'overridden' else prediction.predicted_class

        clinical_val = ClinicalValidation(
            prediction_id=prediction.id,
            doctor_id=current_user.id,
            decision=decision,
            final_class=final_class,
            initial_clinical_diagnosis=form.initial_clinical_diagnosis.data,
            override_reason=override_reason if decision == 'overridden' else None,
            clinical_note=form.clinical_note.data,
            validated_at=datetime.utcnow()
        )
        db.session.add(clinical_val)

        # Update examination: validated & locked
        examination.status = 'validated'
        examination.initial_clinical_diagnosis = form.initial_clinical_diagnosis.data
        examination.locked_at = datetime.utcnow()

        db.session.commit()

        log_action(current_user.id, 'validate_examination', 'Examination', examination.id,
                   f"Pemeriksaan #{examination.id} divalidasi oleh dr. {current_user.full_name}. Keputusan: {decision}.",
                   ip_address=request.remote_addr)

        flash('Pemeriksaan berhasil divalidasi dan dikunci.', 'success')
        return redirect(url_for('validations.view', exam_id=exam_id))

    # Pre-fill final_class from prediction
    if request.method == 'GET':
        form.final_class.data = prediction.predicted_class

    return render_template('validations/validate.html',
                           form=form, examination=examination, prediction=prediction)


@validations_bp.route('/<int:exam_id>/lihat')
@login_required
def view(exam_id):
    examination = Examination.query.get_or_404(exam_id)
    prediction = Prediction.query.filter_by(examination_id=exam_id).first()
    validation = prediction.clinical_validation if prediction else None
    return render_template('validations/view.html',
                           examination=examination, prediction=prediction, validation=validation)

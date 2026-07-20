from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models.patient import Patient
from app.models.examination import Examination
from app.models.prediction import Prediction
from app.examinations.forms import ExaminationForm
from app.predictions.services import run_prediction_service
from app.auth.decorators import roles_required
from app.audit.services import log_action

examinations_bp = Blueprint('examinations', __name__, url_prefix='/pemeriksaan')


def _build_input_data(form):
    return {
        "Umur_bulan": form.age_months.data,
        "Jenis_Kelamin": form.sex.data,
        "Lama_Diare_hari": form.diarrhea_duration_days.data,
        "Frekuensi_BAB_per_hari": form.bowel_movement_frequency.data,
        "Konsistensi_Feses": form.stool_consistency.data,
        "Warna_Feses": form.stool_color.data,
        "Ada_Lendir": form.has_mucus.data,
        "Ada_Darah": form.has_blood.data,
        "Demam": form.has_fever.data,
        "Suhu_Tubuh_C": form.body_temperature.data,
        "Muntah": form.has_vomiting.data,
        "Tanda_Dehidrasi": form.dehydration_sign.data,
    }


@examinations_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    query = Examination.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    pagination = query.order_by(Examination.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('examinations/index.html', pagination=pagination, status_filter=status_filter)


@examinations_bp.route('/buat/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@roles_required('Administrator', 'Perawat', 'Dokter')
def create(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = ExaminationForm()
    form.patient_id.data = patient_id

    if form.validate_on_submit():
        examination = Examination(
            patient_id=patient_id,
            assessor_id=current_user.id,
            examination_date=datetime.utcnow(),
            age_months=form.age_months.data,
            diarrhea_duration_days=form.diarrhea_duration_days.data,
            bowel_movement_frequency=form.bowel_movement_frequency.data,
            stool_consistency=form.stool_consistency.data,
            stool_color=form.stool_color.data,
            has_mucus=form.has_mucus.data,
            has_blood=form.has_blood.data,
            has_fever=form.has_fever.data,
            body_temperature=form.body_temperature.data,
            has_vomiting=form.has_vomiting.data,
            dehydration_sign=form.dehydration_sign.data,
            notes=form.notes.data,
            status='draft'
        )
        db.session.add(examination)
        db.session.flush()  # Get the ID before commit

        if form.submit.data:
            # Run prediction
            input_data = _build_input_data(form)
            prediction, errors, warnings = run_prediction_service(examination, input_data)
            if errors:
                for err in errors:
                    flash(err, 'error')
                db.session.rollback()
                return render_template('examinations/form.html', form=form, patient=patient)
            
            db.session.commit()
            log_action(current_user.id, 'run_prediction', 'Examination', examination.id,
                       f"Skrining dijalankan untuk pemeriksaan #{examination.id}",
                       ip_address=request.remote_addr)
            if warnings:
                for w in warnings:
                    flash(w, 'warning')
            flash('Skrining berhasil dijalankan. Menunggu validasi dokter.', 'success')
            return redirect(url_for('examinations.result', exam_id=examination.id))
        else:
            # Save draft
            db.session.commit()
            flash('Draft pemeriksaan tersimpan.', 'info')
            return redirect(url_for('examinations.detail', exam_id=examination.id))

    return render_template('examinations/form.html', form=form, patient=patient)


@examinations_bp.route('/<int:exam_id>')
@login_required
def detail(exam_id):
    examination = Examination.query.get_or_404(exam_id)
    return render_template('examinations/detail.html', examination=examination)


@examinations_bp.route('/<int:exam_id>/hasil')
@login_required
def result(exam_id):
    examination = Examination.query.get_or_404(exam_id)
    prediction = Prediction.query.filter_by(examination_id=exam_id).first_or_404()
    return render_template('examinations/result.html', examination=examination, prediction=prediction)

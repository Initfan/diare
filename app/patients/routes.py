from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models.patient import Patient
from app.models.examination import Examination
from app.patients.forms import PatientForm
from app.patients.services import create_patient, update_patient, get_age_months
from app.auth.decorators import roles_required
from app.audit.services import log_action
from app.extensions import db

patients_bp = Blueprint('patients', __name__, url_prefix='/pasien')

ALLOWED_ROLES = ('Administrator', 'Petugas administrasi', 'Perawat', 'Dokter')


@patients_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '')
    sex_filter = request.args.get('sex', '')

    query = Patient.query.filter_by(is_active=True)
    if search:
        query = query.filter(Patient.initials.ilike(f'%{search}%') | Patient.patient_code.ilike(f'%{search}%'))
    if sex_filter:
        query = query.filter_by(sex=sex_filter)

    pagination = query.order_by(Patient.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('patients/index.html', pagination=pagination, search=search, sex_filter=sex_filter)


@patients_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@roles_required('Administrator', 'Petugas administrasi', 'Perawat')
def create():
    form = PatientForm()
    if form.validate_on_submit():
        data = {
            'initials': form.initials.data,
            'medical_record_number': form.medical_record_number.data,
            'birth_date': form.birth_date.data,
            'sex': form.sex.data
        }
        patient = create_patient(data, current_user.id)
        log_action(current_user.id, 'create_patient', 'Patient', patient.id,
                   f"Pasien {patient.patient_code} didaftarkan.", ip_address=request.remote_addr)
        flash(f'Pasien {patient.patient_code} berhasil didaftarkan.', 'success')
        return redirect(url_for('patients.detail', patient_id=patient.id))
    return render_template('patients/form.html', form=form, title='Tambah Pasien')


@patients_bp.route('/<int:patient_id>')
@login_required
def detail(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    examinations = Examination.query.filter_by(patient_id=patient.id).order_by(Examination.created_at.desc()).all()
    age_months = get_age_months(patient.birth_date)
    return render_template('patients/detail.html', patient=patient, examinations=examinations, age_months=age_months)


@patients_bp.route('/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
@roles_required('Administrator', 'Petugas administrasi')
def edit(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        data = {
            'initials': form.initials.data,
            'medical_record_number': form.medical_record_number.data,
            'birth_date': form.birth_date.data,
            'sex': form.sex.data
        }
        update_patient(patient, data)
        log_action(current_user.id, 'update_patient', 'Patient', patient.id,
                   f"Data pasien {patient.patient_code} diperbarui.", ip_address=request.remote_addr)
        flash('Data pasien berhasil diperbarui.', 'success')
        return redirect(url_for('patients.detail', patient_id=patient.id))
    return render_template('patients/form.html', form=form, patient=patient, title='Edit Pasien')

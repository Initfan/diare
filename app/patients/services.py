from datetime import date
from app.extensions import db
from app.models.patient import Patient
from app.models.user import User


def generate_patient_code():
    """Generate unique patient code like PSN-0001."""
    last = Patient.query.order_by(Patient.id.desc()).first()
    num = (last.id + 1) if last else 1
    return f"PSN-{num:04d}"


def create_patient(form_data: dict, created_by: int) -> Patient:
    code = generate_patient_code()
    patient = Patient(
        patient_code=code,
        initials=form_data['initials'].strip().upper(),
        medical_record_number=form_data.get('medical_record_number') or None,
        birth_date=form_data['birth_date'],
        sex=form_data['sex'],
        is_active=True,
        created_by=created_by
    )
    db.session.add(patient)
    db.session.commit()
    return patient


def update_patient(patient: Patient, form_data: dict) -> Patient:
    patient.initials = form_data['initials'].strip().upper()
    patient.medical_record_number = form_data.get('medical_record_number') or None
    patient.birth_date = form_data['birth_date']
    patient.sex = form_data['sex']
    db.session.commit()
    return patient


def get_age_months(birth_date: date) -> int:
    today = date.today()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    return max(0, months)

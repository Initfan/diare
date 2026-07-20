from app.extensions import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_code = db.Column(db.String(50), unique=True, nullable=False)
    external_dataset_id = db.Column(db.String(50))
    medical_record_number = db.Column(db.String(50), unique=True)
    initials = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(20), nullable=False) # Laki-laki / Perempuan
    is_active = db.Column(db.Boolean, default=True)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    examinations = db.relationship('Examination', backref='patient', lazy=True)

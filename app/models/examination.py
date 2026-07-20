from app.extensions import db
from datetime import datetime

class Examination(db.Model):
    __tablename__ = 'examinations'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    assessor_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Perawat/Dokter yg input
    
    examination_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Fitur model
    age_months = db.Column(db.Integer)
    diarrhea_duration_days = db.Column(db.Integer)
    bowel_movement_frequency = db.Column(db.Integer)
    stool_consistency = db.Column(db.String(50))
    stool_color = db.Column(db.String(50))
    has_mucus = db.Column(db.String(10))
    has_blood = db.Column(db.String(10))
    has_fever = db.Column(db.String(10))
    body_temperature = db.Column(db.Float)
    has_vomiting = db.Column(db.String(10))
    dehydration_sign = db.Column(db.String(50))
    
    # Diagnosis klinis (tidak digunakan utk fitur model, diisi oleh dokter)
    initial_clinical_diagnosis = db.Column(db.String(255))
    
    status = db.Column(db.String(20), default='draft') # draft, waiting_validation, validated, cancelled
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = db.Column(db.DateTime)
    locked_at = db.Column(db.DateTime)
    
    prediction = db.relationship('Prediction', backref='examination', uselist=False, lazy=True)

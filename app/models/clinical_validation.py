from app.extensions import db
from datetime import datetime

class ClinicalValidation(db.Model):
    __tablename__ = 'clinical_validations'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    decision = db.Column(db.String(20), nullable=False) # accepted, overridden
    final_class = db.Column(db.String(50), nullable=False)
    initial_clinical_diagnosis = db.Column(db.String(255))
    override_reason = db.Column(db.Text)
    clinical_note = db.Column(db.Text)
    
    validated_at = db.Column(db.DateTime, default=datetime.utcnow)

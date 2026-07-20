from app.extensions import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'), nullable=False)
    model_version_id = db.Column(db.Integer, db.ForeignKey('model_versions.id'), nullable=False)
    
    predicted_class = db.Column(db.String(50), nullable=False)
    mild_score = db.Column(db.Float)
    moderate_score = db.Column(db.Float)
    severe_score = db.Column(db.Float)
    
    input_snapshot_json = db.Column(db.Text)
    warning_metadata_json = db.Column(db.Text)
    
    predicted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    clinical_validation = db.relationship('ClinicalValidation', backref='prediction', uselist=False, lazy=True)

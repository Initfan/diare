from app.extensions import db
from datetime import datetime

class ModelVersion(db.Model):
    __tablename__ = 'model_versions'
    
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50), nullable=False, unique=True)
    algorithm = db.Column(db.String(100))
    artifact_path = db.Column(db.String(255))
    
    dataset_filename = db.Column(db.String(255))
    dataset_hash = db.Column(db.String(255))
    
    training_date = db.Column(db.DateTime)
    training_data_count = db.Column(db.Integer)
    testing_data_count = db.Column(db.Integer)
    
    accuracy = db.Column(db.Float)
    precision_macro = db.Column(db.Float)
    recall_macro = db.Column(db.Float)
    f1_macro = db.Column(db.Float)
    best_alpha = db.Column(db.Float)
    
    metrics_json = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    predictions = db.relationship('Prediction', backref='model_version', lazy=True)

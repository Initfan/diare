import os
import json
import joblib
from datetime import datetime

import pandas as pd

from app.ml.constants import MODEL_FEATURES

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')


def get_active_pipeline():
    """Load the trained pipeline from disk."""
    pipeline_path = os.path.join(ARTIFACTS_DIR, 'diarrhea_severity_pipeline.joblib')
    if not os.path.exists(pipeline_path):
        raise FileNotFoundError("Model pipeline belum dilatih. Jalankan training terlebih dahulu.")
    return joblib.load(pipeline_path)


def get_model_metadata():
    """Load model metadata from JSON."""
    metadata_path = os.path.join(ARTIFACTS_DIR, 'model_metadata.json')
    if not os.path.exists(metadata_path):
        return {}
    with open(metadata_path, 'r') as f:
        return json.load(f)


def predict(input_data: dict) -> dict:
    """
    Run prediction using the trained pipeline.
    
    input_data: dict with keys matching MODEL_FEATURES
    Returns: dict with predicted_class, probabilities, model_version, predicted_at
    """
    pipeline = get_active_pipeline()
    metadata = get_model_metadata()
    
    # Pastikan urutan fitur konsisten dengan MODEL_FEATURES
    row = {feature: input_data[feature] for feature in MODEL_FEATURES}
    X_input = pd.DataFrame([row])
    
    # Predict class
    predicted_class = pipeline.predict(X_input)[0]
    
    # Predict probabilities
    proba = pipeline.predict_proba(X_input)[0]
    classes = pipeline.named_steps['classifier'].classes_.tolist()
    
    # Map probabilitas berdasarkan nama kelas (jangan asumsikan urutan)
    probabilities = {cls: round(float(prob), 4) for cls, prob in zip(classes, proba)}
    
    return {
        "predicted_class": predicted_class,
        "probabilities": probabilities,
        "model_version": metadata.get("model_version", "unknown"),
        "training_date": metadata.get("training_date", ""),
        "predicted_at": datetime.utcnow().isoformat()
    }

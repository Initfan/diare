import json
from datetime import datetime
from app.extensions import db
from app.models import Prediction, ModelVersion, Examination
from app.ml.predict import predict as ml_predict
from app.predictions.validators import validate_prediction_input


def run_prediction_service(examination: Examination, input_data: dict):
    """
    Full prediction flow:
    1. Validate input
    2. Get active model version
    3. Run ML prediction
    4. Save Prediction record
    5. Update examination status
    """
    # 1. Validate input
    is_valid, errors, warnings = validate_prediction_input(input_data)
    if not is_valid:
        return None, errors, []
    
    # 2. Get active model version from DB
    active_model = ModelVersion.query.filter_by(is_active=True).first()
    if not active_model:
        return None, ["Tidak ada model aktif. Hubungi administrator untuk melatih model."], []
    
    # 3. Run ML prediction
    result = ml_predict(input_data)
    
    probs = result["probabilities"]
    
    # 4. Save prediction record
    prediction = Prediction(
        examination_id=examination.id,
        model_version_id=active_model.id,
        predicted_class=result["predicted_class"],
        mild_score=probs.get("Ringan", 0.0),
        moderate_score=probs.get("Sedang", 0.0),
        severe_score=probs.get("Berat", 0.0),
        input_snapshot_json=json.dumps(input_data, ensure_ascii=False),
        warning_metadata_json=json.dumps(warnings, ensure_ascii=False) if warnings else None,
        predicted_at=datetime.utcnow()
    )
    db.session.add(prediction)
    
    # 5. Update examination status to waiting_validation
    examination.status = 'waiting_validation'
    examination.submitted_at = datetime.utcnow()
    
    db.session.commit()
    
    return prediction, [], warnings

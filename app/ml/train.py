import os
import json
import hashlib
import joblib
from datetime import datetime

import pandas as pd
from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline

from app.ml.constants import MODEL_FEATURES, TARGET_COLUMN, NUMERIC_FEATURES, CATEGORICAL_FEATURES
from app.ml.preprocessing import build_preprocessor
from app.ml.evaluate import compute_evaluation_metrics

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')


def compute_file_hash(filepath):
    """Compute MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def train_model(df: pd.DataFrame, dataset_path: str) -> dict:
    """
    Trains the Naive Bayes pipeline.
    Returns a dict with model metadata and metrics.
    """
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    
    # --- 1. Prepare features and target ---
    X = df[MODEL_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()
    
    print(f"Jumlah data: {len(df)}")
    print(f"Jumlah fitur: {len(MODEL_FEATURES)}")
    print(f"Distribusi target:\n{y.value_counts().to_string()}")
    
    # --- 2. Stratified train/test split (hanya fit preprocessor pada training data) ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
    print(f"Training size: {len(X_train)}")
    print(f"Testing size: {len(X_test)}")
    
    # --- 3. Build preprocessing and model pipeline ---
    preprocessor = build_preprocessor()
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', CategoricalNB())
    ])
    
    # --- 4. GridSearchCV + StratifiedKFold cross-validation ---
    param_grid = {
        "classifier__alpha": [0.1, 0.5, 1.0, 2.0, 5.0]
    }
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    grid_search = GridSearchCV(
        pipeline,
        param_grid=param_grid,
        cv=cv,
        scoring='f1_macro',
        n_jobs=-1,
        refit=True
    )
    
    grid_search.fit(X_train, y_train)
    
    best_pipeline = grid_search.best_estimator_
    best_alpha = grid_search.best_params_['classifier__alpha']
    
    print(f"Best alpha: {best_alpha}")
    
    # --- 5. Evaluate on test set ---
    metrics = compute_evaluation_metrics(best_pipeline, X_test, y_test, cv_results=grid_search.cv_results_)
    
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Macro F1-score: {metrics['f1_macro']:.4f}")
    
    # --- 6. Save pipeline ---
    pipeline_path = os.path.join(ARTIFACTS_DIR, 'diarrhea_severity_pipeline.joblib')
    joblib.dump(best_pipeline, pipeline_path)
    print(f"Pipeline disimpan di: {pipeline_path}")
    
    # --- 7. Save feature schema ---
    feature_schema = {
        "features": MODEL_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES
    }
    with open(os.path.join(ARTIFACTS_DIR, 'feature_schema.json'), 'w') as f:
        json.dump(feature_schema, f, indent=2)
    
    # --- 8. Save category schema ---
    classes_in_model = best_pipeline.named_steps['classifier'].classes_.tolist()
    category_schema = {
        "target_classes": classes_in_model
    }
    with open(os.path.join(ARTIFACTS_DIR, 'category_schema.json'), 'w') as f:
        json.dump(category_schema, f, indent=2)
    
    # --- 9. Build model metadata ---
    dataset_hash = compute_file_hash(dataset_path) if os.path.exists(dataset_path) else None
    training_date = datetime.utcnow().isoformat()
    
    metadata = {
        "model_name": "Categorical Naive Bayes",
        "model_version": f"1.0.0-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "dataset_filename": os.path.basename(dataset_path),
        "dataset_hash": dataset_hash,
        "target_column": TARGET_COLUMN,
        "excluded_columns": ["ID_Pasien", "Diagnosis_Klinis_Awal"],
        "training_date": training_date,
        "training_rows": len(X_train),
        "testing_rows": len(X_test),
        "random_state": 42,
        "best_alpha": best_alpha,
        "classes": classes_in_model
    }
    
    with open(os.path.join(ARTIFACTS_DIR, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # --- 10. Save metrics ---
    with open(os.path.join(ARTIFACTS_DIR, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    return {
        "metadata": metadata,
        "metrics": metrics,
        "pipeline_path": pipeline_path
    }

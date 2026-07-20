import numpy as np
import json
import os
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')


def compute_evaluation_metrics(pipeline, X_test, y_test, cv_results=None) -> dict:
    """
    Computes all evaluation metrics and saves confusion matrix image.
    """
    y_pred = pipeline.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    
    report = classification_report(
        y_test, y_pred,
        output_dict=True,
        zero_division=0
    )
    
    cm = confusion_matrix(y_test, y_pred)
    classes = pipeline.named_steps['classifier'].classes_.tolist()
    
    # Save confusion matrix image
    _save_confusion_matrix_image(cm, classes)
    
    # Gather CV results
    cv_info = {}
    if cv_results is not None:
        cv_info = {
            "mean_test_scores": cv_results.get('mean_test_score', []).tolist(),
            "params": [str(p) for p in cv_results.get('params', [])]
        }
    
    metrics = {
        "accuracy": round(accuracy, 4),
        "precision_macro": round(report['macro avg']['precision'], 4),
        "recall_macro": round(report['macro avg']['recall'], 4),
        "f1_macro": round(report['macro avg']['f1-score'], 4),
        "precision_weighted": round(report['weighted avg']['precision'], 4),
        "recall_weighted": round(report['weighted avg']['recall'], 4),
        "f1_weighted": round(report['weighted avg']['f1-score'], 4),
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "classes": classes,
        "cv_results": cv_info
    }
    
    return metrics


def _save_confusion_matrix_image(cm, classes):
    """Save confusion matrix as PNG."""
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.colorbar(im, ax=ax)
    
    tick_marks = np.arange(len(classes))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(classes, rotation=45, ha='right')
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(classes)
    
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                    ha='center', va='center',
                    color='white' if cm[i, j] > thresh else 'black')
    
    ax.set_ylabel('Label Aktual')
    ax.set_xlabel('Label Prediksi')
    ax.set_title('Confusion Matrix')
    
    plt.tight_layout()
    plt.savefig(os.path.join(ARTIFACTS_DIR, 'confusion_matrix.png'), dpi=100)
    plt.close()

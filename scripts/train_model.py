import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.ml.dataset_loader import load_dataset
from app.ml.dataset_validator import validate_dataset
from app.ml.train import train_model

DATASET_PATH = os.environ.get('DATASET_PATH', 'datasets/dataset_pasien_diare_anak_revisi.csv')


def main():
    print("=" * 60)
    print("TRAINING MODEL: Deteksi Dini Keparahan Diare pada Anak")
    print("=" * 60)
    
    if not os.path.exists(DATASET_PATH):
        print(f"\n[ERROR] Dataset tidak ditemukan di: {DATASET_PATH}")
        print("Pastikan file dataset sudah disalin ke folder 'datasets/'")
        print("Nama file yang diharapkan: dataset_pasien_diare_anak_revisi.csv")
        sys.exit(1)

    print(f"\nDataset ditemukan: {DATASET_PATH}")
    
    # Load dataset
    try:
        df = load_dataset(DATASET_PATH)
    except Exception as e:
        print(f"[ERROR] Gagal membaca dataset: {e}")
        sys.exit(1)

    print(f"Dataset berhasil dimuat")
    print(f"  Jumlah data: {len(df)} baris")
    print(f"  Jumlah kolom: {len(df.columns)}")

    # Validate dataset
    is_valid, errors = validate_dataset(df)
    if not is_valid:
        print("\n[ERROR] Validasi dataset gagal:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print(f"\nValidasi dataset berhasil.\n")

    # Train model
    result = train_model(df, DATASET_PATH)
    metadata = result['metadata']
    metrics = result['metrics']

    print("\n" + "=" * 60)
    print("TRAINING SELESAI")
    print("=" * 60)
    print(f"  Model: {metadata['model_name']}")
    print(f"  Versi: {metadata['model_version']}")
    print(f"  Dataset: {metadata['dataset_filename']}")
    print(f"  Training rows: {metadata['training_rows']}")
    print(f"  Testing rows: {metadata['testing_rows']}")
    print(f"  Best Alpha: {metadata['best_alpha']}")
    print(f"  Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']:.2%})")
    print(f"  Macro F1-score: {metrics['f1_macro']:.4f}")
    print(f"  Artifact: {result['pipeline_path']}")
    
    print("\n[INFO] Perhatian recall kelas 'Berat':")
    report = metrics.get('classification_report', {})
    if 'Berat' in report:
        print(f"  Precision: {report['Berat']['precision']:.4f}")
        print(f"  Recall: {report['Berat']['recall']:.4f}")
        print(f"  F1-score: {report['Berat']['f1-score']:.4f}")
    
    # Save model version to DB if Flask app is available
    try:
        app = create_app('development')
        with app.app_context():
            import json
            from datetime import datetime
            from app.extensions import db
            from app.models.model_version import ModelVersion
            
            db.create_all()
            
            ModelVersion.query.update({'is_active': False})
            version = ModelVersion(
                model_name=metadata['model_name'],
                version=metadata['model_version'],
                algorithm='CategoricalNB',
                artifact_path=result['pipeline_path'],
                dataset_filename=metadata['dataset_filename'],
                dataset_hash=metadata.get('dataset_hash'),
                training_date=datetime.utcnow(),
                training_data_count=metadata['training_rows'],
                testing_data_count=metadata['testing_rows'],
                accuracy=metrics['accuracy'],
                precision_macro=metrics['precision_macro'],
                recall_macro=metrics['recall_macro'],
                f1_macro=metrics['f1_macro'],
                best_alpha=metadata['best_alpha'],
                metrics_json=json.dumps(metrics, ensure_ascii=False),
                is_active=True
            )
            db.session.add(version)
            db.session.commit()
            print(f"\n[INFO] Model version ID {version.id} tersimpan di database.")
    except Exception as e:
        print(f"\n[WARNING] Tidak bisa menyimpan ke database: {e}")
        print("         Jalankan 'flask db upgrade' dan 'python scripts/seed.py' terlebih dahulu.")


if __name__ == '__main__':
    main()

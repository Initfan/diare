import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-default'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DATASET_PATH = os.environ.get('DATASET_PATH', 'datasets/dataset_pasien_diare_anak_revisi.csv')
    MODEL_ARTIFACT_PATH = os.environ.get('MODEL_ARTIFACT_PATH', 'app/ml/artifacts/diarrhea_severity_pipeline.joblib')
    MODEL_METADATA_PATH = os.environ.get('MODEL_METADATA_PATH', 'app/ml/artifacts/model_metadata.json')
    MODEL_METRICS_PATH = os.environ.get('MODEL_METRICS_PATH', 'app/ml/artifacts/metrics.json')
    
    PERMANENT_SESSION_LIFETIME = int(os.environ.get('SESSION_LIFETIME_MINUTES', 30)) * 60
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH_MB', 5)) * 1024 * 1024

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

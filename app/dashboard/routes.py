from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, date
from app.models import Patient, Examination, Prediction, ModelVersion
from app.extensions import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    today = date.today()
    
    total_patients = Patient.query.filter_by(is_active=True).count()
    total_examinations = Examination.query.count()
    today_examinations = Examination.query.filter(
        func.date(Examination.examination_date) == today
    ).count()
    waiting_validation = Examination.query.filter_by(status='waiting_validation').count()
    
    # Distribusi hasil prediksi
    ringan_count = Prediction.query.filter_by(predicted_class='Ringan').count()
    sedang_count = Prediction.query.filter_by(predicted_class='Sedang').count()
    berat_count = Prediction.query.filter_by(predicted_class='Berat').count()
    
    # Model aktif
    active_model = ModelVersion.query.filter_by(is_active=True).first()
    
    # Pemeriksaan terbaru
    recent_examinations = (
        Examination.query
        .order_by(Examination.created_at.desc())
        .limit(8)
        .all()
    )
    
    return render_template(
        'dashboard/index.html',
        total_patients=total_patients,
        total_examinations=total_examinations,
        today_examinations=today_examinations,
        waiting_validation=waiting_validation,
        ringan_count=ringan_count,
        sedang_count=sedang_count,
        berat_count=berat_count,
        active_model=active_model,
        recent_examinations=recent_examinations,
    )

from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models.audit_log import AuditLog
from app.auth.decorators import roles_required

audit_bp = Blueprint('audit', __name__, url_prefix='/audit')


@audit_bp.route('/')
@login_required
@roles_required('Administrator')
def index():
    page = request.args.get('page', 1, type=int)
    action_filter = request.args.get('action', '')
    query = AuditLog.query
    if action_filter:
        query = query.filter(AuditLog.action.ilike(f'%{action_filter}%'))
    pagination = query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('audit/index.html', pagination=pagination, action_filter=action_filter)

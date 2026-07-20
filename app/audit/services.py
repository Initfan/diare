import json
from datetime import datetime
from app.extensions import db
from app.models.audit_log import AuditLog


def log_action(user_id, action, entity_type=None, entity_id=None,
               description=None, metadata=None, ip_address=None):
    """Log a user action to the audit trail."""
    try:
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            metadata_json=json.dumps(metadata, ensure_ascii=False) if metadata else None,
            ip_address=ip_address,
            created_at=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()

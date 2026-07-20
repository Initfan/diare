from functools import wraps
from flask import abort
from flask_login import current_user


def roles_required(*role_names):
    """Decorator to restrict access to specific roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role is None or current_user.role.name not in role_names:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def roles_forbidden(*role_names):
    """Decorator to forbid access to specific roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role and current_user.role.name in role_names:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

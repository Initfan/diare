import os
from flask import Flask, render_template
from app.config import config
from app.extensions import db, migrate, login_manager, csrf
from app.models.user import User


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    if config_name not in ('development', 'testing', 'production'):
        config_name = 'development'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.patients.routes import patients_bp
    from app.examinations.routes import examinations_bp
    from app.validations.routes import validations_bp
    from app.model_management.routes import model_management_bp
    from app.audit.routes import audit_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(examinations_bp)
    app.register_blueprint(validations_bp)
    app.register_blueprint(model_management_bp)
    app.register_blueprint(audit_bp)

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    # Static route to serve confusion matrix
    @app.route('/static/ml/confusion_matrix.png')
    def confusion_matrix_image():
        import os as _os
        from flask import send_file
        cm_path = _os.path.join(app.root_path, 'ml', 'artifacts', 'confusion_matrix.png')
        if _os.path.exists(cm_path):
            return send_file(cm_path, mimetype='image/png')
        return '', 404

    return app

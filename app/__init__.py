import os
from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload folder exists
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.scan import bp as scan_bp
    app.register_blueprint(scan_bp, url_prefix='/scan')

    from app.recommendation import bp as recommendation_bp
    app.register_blueprint(recommendation_bp, url_prefix='/recommendation')

    from app.quiz import bp as quiz_bp
    app.register_blueprint(quiz_bp, url_prefix='/quiz')

    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    # Error handler for file too large
    @app.errorhandler(413)
    def too_large(e):
        flash('File too large. Maximum allowed size is 5 MB. Please choose a smaller image.', 'danger')
        return redirect(url_for('scan.index'))

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

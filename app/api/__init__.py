from functools import wraps
from flask import Blueprint, jsonify
from flask_login import current_user

api_bp = Blueprint('api', __name__, url_prefix='/api')


def api_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required.'}), 401
        return f(*args, **kwargs)
    return decorated


def api_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required.'}), 401
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required.'}), 403
        return f(*args, **kwargs)
    return decorated


def api_super_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required.'}), 401
        if not current_user.is_super_admin:
            return jsonify({'error': 'Super admin access required.'}), 403
        return f(*args, **kwargs)
    return decorated


# Import routes to register them with the blueprint
from app.api import auth, scan, recommendation, quiz, blog

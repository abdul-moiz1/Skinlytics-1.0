from flask import request, jsonify
from flask_login import login_user, logout_user, current_user
from app.api import api_bp, api_login_required, api_super_admin_required
from app.models import User
from app import db


@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required.'}), 400

    if len(username) < 3 or len(username) > 80:
        return jsonify({'error': 'Username must be between 3 and 80 characters.'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered.'}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken.'}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'user': user.to_dict()}), 201


@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    if not user.is_active:
        return jsonify({'error': 'Your account has been deactivated.'}), 403

    login_user(user)
    return jsonify({'user': user.to_dict()}), 200


@api_bp.route('/auth/logout', methods=['POST'])
@api_login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully.'}), 200


@api_bp.route('/auth/me', methods=['GET'])
@api_login_required
def api_me():
    return jsonify({'user': current_user.to_dict()}), 200


# --- Admin: User Management ---

@api_bp.route('/admin/users', methods=['GET'])
@api_super_admin_required
def api_admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({'users': [u.to_dict() for u in users]}), 200


@api_bp.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
@api_super_admin_required
def api_admin_toggle_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    if user.id == current_user.id:
        return jsonify({'error': 'Cannot change your own admin status.'}), 400

    user.is_admin = not user.is_admin
    db.session.commit()

    action = 'promoted to admin' if user.is_admin else 'removed from admin'
    return jsonify({'message': f'{user.username} has been {action}.', 'user': user.to_dict()}), 200


@api_bp.route('/admin/users/<int:user_id>/ban', methods=['POST'])
@api_super_admin_required
def api_admin_ban_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    if user.id == current_user.id:
        return jsonify({'error': 'Cannot ban yourself.'}), 400

    if user.is_super_admin:
        return jsonify({'error': 'Cannot ban a super admin.'}), 400

    user.is_active = not user.is_active
    db.session.commit()

    action = 'unbanned' if user.is_active else 'banned'
    return jsonify({'message': f'{user.username} has been {action}.', 'user': user.to_dict()}), 200

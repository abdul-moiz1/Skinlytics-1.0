from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from app import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('scan.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('scan.index'))
        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


# --- User Admin ---

@bp.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_super_admin:
        abort(403)
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('auth/admin/list.html', users=users)


@bp.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
@login_required
def admin_toggle_user(user_id):
    if not current_user.is_super_admin:
        abort(403)

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('auth.admin_users'))

    user.is_admin = not user.is_admin
    db.session.commit()

    action = 'promoted to admin' if user.is_admin else 'removed from admin'
    flash(f'{user.username} has been {action}.', 'success')
    return redirect(url_for('auth.admin_users'))

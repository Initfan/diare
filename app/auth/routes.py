from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models.user import User
from app.auth.forms import LoginForm
from app.audit.services import log_action

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.username.data
        # Support login via username atau email
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Username/email atau password salah.', 'error')
            log_action(None, 'login_failed', 'User', None,
                       f"Percobaan login gagal untuk: {identifier}",
                       ip_address=request.remote_addr)
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Akun Anda telah dinonaktifkan. Hubungi administrator.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        log_action(user.id, 'login', 'User', user.id,
                   f"Pengguna {user.username} berhasil masuk.",
                   ip_address=request.remote_addr)
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard.index'))
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    log_action(current_user.id, 'logout', 'User', current_user.id,
               f"Pengguna {current_user.username} keluar.",
               ip_address=request.remote_addr)
    logout_user()
    flash('Anda telah keluar dari sistem.', 'info')
    return redirect(url_for('auth.login'))

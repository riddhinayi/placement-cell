from flask import redirect, url_for
from flask_login import login_required, current_user
from app.main import main


@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role == 'student':
        return redirect(url_for('student.dashboard'))
    elif current_user.role == 'company':
        return redirect(url_for('company.dashboard'))
    return redirect(url_for('auth.login'))
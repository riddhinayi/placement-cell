from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Student, Company
from app.auth import auth
from app.auth.forms import RegisterForm, LoginForm


# ── REGISTER ──────────────────────────────────────────────────────────────────
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            name     = form.name.data,
            email    = form.email.data,
            password = hashed_pw,
            role     = form.role.data
        )
        db.session.add(user)
        db.session.flush()   # get user.id before commit

        # Create linked profile based on role
        if user.role == 'student':
            student = Student(
                user_id     = user.id,
                roll_number = f'ROLL{user.id:04d}',  # temporary roll number
                branch      = 'Not Set',
                cgpa        = 0.0
            )
            db.session.add(student)

        elif user.role == 'company':
            company = Company(
                user_id      = user.id,
                company_name = user.name,
            )
            db.session.add(company)

        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


# ── LOGIN ─────────────────────────────────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)


# ── LOGOUT ────────────────────────────────────────────────────────────────────
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
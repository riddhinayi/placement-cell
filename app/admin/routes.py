from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Student, Company, JobDrive, Application
from app.admin import admin
from functools import wraps


# ── Admin required decorator ──────────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access only.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_students'  : Student.query.count(),
        'total_companies' : Company.query.count(),
        'total_drives'    : JobDrive.query.count(),
        'total_placed'    : Student.query.filter_by(is_placed=True).count(),
        'pending_companies': Company.query.filter_by(is_approved=False).count(),
        'pending_drives'  : JobDrive.query.filter_by(is_approved=False).count(),
        'total_applications': Application.query.count(),
    }
    recent_drives = JobDrive.query.order_by(JobDrive.created_at.desc()).limit(5).all()
    recent_applications = Application.query.order_by(Application.applied_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_drives=recent_drives,
                           recent_applications=recent_applications)


# ── STUDENTS LIST ─────────────────────────────────────────────────────────────
@admin.route('/admin/students')
@login_required
@admin_required
def students():
    all_students = Student.query.all()
    return render_template('admin/students.html', students=all_students)


# ── STUDENT DELETE ────────────────────────────────────────────────────────────
@admin.route('/admin/students/delete/<int:id>')
@login_required
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    user    = User.query.get(student.user_id)
    db.session.delete(student)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Student deleted.', 'success')
    return redirect(url_for('admin.students'))


# ── COMPANIES LIST ────────────────────────────────────────────────────────────
@admin.route('/admin/companies')
@login_required
@admin_required
def companies():
    all_companies = Company.query.all()
    return render_template('admin/companies.html', companies=all_companies)


# ── APPROVE COMPANY ───────────────────────────────────────────────────────────
@admin.route('/admin/companies/approve/<int:id>')
@login_required
@admin_required
def approve_company(id):
    company = Company.query.get_or_404(id)
    company.is_approved = True
    db.session.commit()
    flash(f'{company.company_name} approved!', 'success')
    return redirect(url_for('admin.companies'))


# ── REJECT / DELETE COMPANY ───────────────────────────────────────────────────
@admin.route('/admin/companies/delete/<int:id>')
@login_required
@admin_required
def delete_company(id):
    company = Company.query.get_or_404(id)
    user    = User.query.get(company.user_id)
    db.session.delete(company)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Company removed.', 'success')
    return redirect(url_for('admin.companies'))


# ── JOB DRIVES LIST ───────────────────────────────────────────────────────────
@admin.route('/admin/drives')
@login_required
@admin_required
def drives():
    all_drives = JobDrive.query.order_by(JobDrive.created_at.desc()).all()
    return render_template('admin/drives.html', drives=all_drives)


# ── APPROVE DRIVE ─────────────────────────────────────────────────────────────
@admin.route('/admin/drives/approve/<int:id>')
@login_required
@admin_required
def approve_drive(id):
    drive = JobDrive.query.get_or_404(id)
    drive.is_approved = True
    db.session.commit()
    flash(f'Drive "{drive.title}" approved!', 'success')
    return redirect(url_for('admin.drives'))


# ── DELETE DRIVE ──────────────────────────────────────────────────────────────
@admin.route('/admin/drives/delete/<int:id>')
@login_required
@admin_required
def delete_drive(id):
    drive = JobDrive.query.get_or_404(id)
    db.session.delete(drive)
    db.session.commit()
    flash('Drive deleted.', 'success')
    return redirect(url_for('admin.drives'))


# ── APPLICATIONS LIST ─────────────────────────────────────────────────────────
@admin.route('/admin/applications')
@login_required
@admin_required
def applications():
    all_apps = Application.query.order_by(Application.applied_at.desc()).all()
    return render_template('admin/applications.html', applications=all_apps)


# ── UPDATE APPLICATION STATUS ─────────────────────────────────────────────────
@admin.route('/admin/applications/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_application(id):
    app_obj = Application.query.get_or_404(id)
    new_status = request.form.get('status')
    app_obj.status = new_status

    # If selected, mark student as placed
    if new_status == 'selected':
        app_obj.student.is_placed = True

    db.session.commit()
    flash('Application status updated.', 'success')
    return redirect(url_for('admin.applications'))
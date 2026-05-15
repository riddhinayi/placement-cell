from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Company, JobDrive, Application, Student
from app.company import company
from app.company.forms import CompanyProfileForm, JobDriveForm
from functools import wraps
from datetime import datetime


# ── Company required decorator ────────────────────────────────────────────────
def company_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'company':
            flash('Company access only.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
@company.route('/company/dashboard')
@login_required
@company_required
def dashboard():
    profile = Company.query.filter_by(user_id=current_user.id).first()
    drives  = JobDrive.query.filter_by(
                  company_id=profile.id
              ).order_by(JobDrive.created_at.desc()).all() if profile else []

    stats = {
        'total_drives'      : len(drives),
        'approved_drives'   : sum(1 for d in drives if d.is_approved),
        'total_applications': sum(len(d.applications) for d in drives),
        'total_selected'    : Application.query.join(JobDrive).filter(
                                  JobDrive.company_id == profile.id,
                                  Application.status == 'selected'
                              ).count() if profile else 0,
    }
    recent_apps = Application.query.join(JobDrive).filter(
                      JobDrive.company_id == profile.id
                  ).order_by(Application.applied_at.desc()).limit(6).all() if profile else []

    return render_template('company/dashboard.html',
                           profile=profile,
                           drives=drives,
                           stats=stats,
                           recent_apps=recent_apps)


# ── COMPANY PROFILE ───────────────────────────────────────────────────────────
@company.route('/company/profile', methods=['GET', 'POST'])
@login_required
@company_required
def profile():
    profile = Company.query.filter_by(user_id=current_user.id).first()
    form    = CompanyProfileForm(obj=profile)

    if form.validate_on_submit():
        profile.company_name = form.company_name.data
        profile.industry     = form.industry.data
        profile.website      = form.website.data
        profile.location     = form.location.data
        profile.description  = form.description.data
        db.session.commit()
        flash('Company profile updated!', 'success')
        return redirect(url_for('company.dashboard'))

    return render_template('company/profile.html', form=form, profile=profile)


# ── POST NEW JOB DRIVE ────────────────────────────────────────────────────────
@company.route('/company/drives/new', methods=['GET', 'POST'])
@login_required
@company_required
def new_drive():
    profile = Company.query.filter_by(user_id=current_user.id).first()

    if not profile.is_approved:
        flash('Your company must be approved by admin before posting drives.', 'warning')
        return redirect(url_for('company.dashboard'))

    form = JobDriveForm()
    if form.validate_on_submit():
        drive_date     = None
        apply_deadline = None

        if form.drive_date.data:
            try:
                drive_date = datetime.strptime(form.drive_date.data, '%Y-%m-%d')
            except ValueError:
                flash('Invalid drive date format. Use YYYY-MM-DD.', 'danger')
                return render_template('company/new_drive.html', form=form)

        if form.apply_deadline.data:
            try:
                apply_deadline = datetime.strptime(form.apply_deadline.data, '%Y-%m-%d')
            except ValueError:
                flash('Invalid deadline format. Use YYYY-MM-DD.', 'danger')
                return render_template('company/new_drive.html', form=form)

        drive = JobDrive(
            company_id      = profile.id,
            title           = form.title.data,
            description     = form.description.data,
            job_type        = form.job_type.data,
            package         = form.package.data,
            location        = form.location.data,
            min_cgpa        = form.min_cgpa.data,
            allowed_branches= form.allowed_branches.data,
            max_backlogs    = form.max_backlogs.data,
            drive_date      = drive_date,
            apply_deadline  = apply_deadline,
            is_approved     = False,
        )
        db.session.add(drive)
        db.session.commit()
        flash('Job drive posted! Waiting for admin approval.', 'success')
        return redirect(url_for('company.my_drives'))

    return render_template('company/new_drive.html', form=form)


# ── MY DRIVES ─────────────────────────────────────────────────────────────────
@company.route('/company/drives')
@login_required
@company_required
def my_drives():
    profile = Company.query.filter_by(user_id=current_user.id).first()
    drives  = JobDrive.query.filter_by(
                  company_id=profile.id
              ).order_by(JobDrive.created_at.desc()).all()
    return render_template('company/drives.html', drives=drives)


# ── DELETE DRIVE ──────────────────────────────────────────────────────────────
@company.route('/company/drives/delete/<int:id>')
@login_required
@company_required
def delete_drive(id):
    drive = JobDrive.query.get_or_404(id)
    profile = Company.query.filter_by(user_id=current_user.id).first()
    if drive.company_id != profile.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('company.my_drives'))
    db.session.delete(drive)
    db.session.commit()
    flash('Drive deleted.', 'success')
    return redirect(url_for('company.my_drives'))


# ── VIEW APPLICANTS FOR A DRIVE ───────────────────────────────────────────────
@company.route('/company/drives/<int:drive_id>/applicants')
@login_required
@company_required
def applicants(drive_id):
    profile = Company.query.filter_by(user_id=current_user.id).first()
    drive   = JobDrive.query.get_or_404(drive_id)

    if drive.company_id != profile.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('company.my_drives'))

    applications = Application.query.filter_by(
                       job_drive_id=drive_id
                   ).order_by(Application.applied_at.desc()).all()

    return render_template('company/applicants.html',
                           drive=drive,
                           applications=applications)


# ── UPDATE APPLICANT STATUS ───────────────────────────────────────────────────
@company.route('/company/applicants/update/<int:app_id>', methods=['POST'])
@login_required
@company_required
def update_status(app_id):
    application = Application.query.get_or_404(app_id)
    new_status  = request.form.get('status')
    application.status = new_status

    if new_status == 'selected':
        application.student.is_placed = True

    db.session.commit()
    flash('Applicant status updated!', 'success')
    return redirect(url_for('company.applicants',
                            drive_id=application.job_drive_id))
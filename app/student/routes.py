from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Student, JobDrive, Application
from app.student import student
from app.student.forms import StudentProfileForm
from functools import wraps
from datetime import datetime


# ── Student required decorator ────────────────────────────────────────────────
def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'student':
            flash('Student access only.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
@student.route('/student/dashboard')
@login_required
@student_required
def dashboard():
    profile      = Student.query.filter_by(user_id=current_user.id).first()
    applications = Application.query.filter_by(
                       student_id=profile.id
                   ).order_by(Application.applied_at.desc()).all() if profile else []
    open_drives  = JobDrive.query.filter_by(
                       is_approved=True, is_active=True
                   ).order_by(JobDrive.created_at.desc()).limit(5).all()

    stats = {
        'total_applied'     : len(applications),
        'shortlisted'       : sum(1 for a in applications if a.status == 'shortlisted'),
        'interviews'        : sum(1 for a in applications if a.status == 'interview'),
        'selected'          : sum(1 for a in applications if a.status == 'selected'),
    }
    return render_template('student/dashboard.html',
                           profile=profile,
                           applications=applications,
                           open_drives=open_drives,
                           stats=stats)


# ── PROFILE ───────────────────────────────────────────────────────────────────
@student.route('/student/profile', methods=['GET', 'POST'])
@login_required
@student_required
def profile():
    profile = Student.query.filter_by(user_id=current_user.id).first()
    form    = StudentProfileForm(obj=profile)

    if form.validate_on_submit():
        profile.roll_number = form.roll_number.data
        profile.branch      = form.branch.data
        profile.cgpa        = form.cgpa.data
        profile.backlogs    = form.backlogs.data
        profile.phone       = form.phone.data
        profile.skills      = form.skills.data
        profile.resume_url  = form.resume_url.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.dashboard'))

    return render_template('student/profile.html', form=form, profile=profile)


# ── JOB DRIVES (available to student) ────────────────────────────────────────
@student.route('/student/drives')
@login_required
@student_required
def drives():
    profile     = Student.query.filter_by(user_id=current_user.id).first()
    all_drives  = JobDrive.query.filter_by(
                      is_approved=True, is_active=True
                  ).order_by(JobDrive.created_at.desc()).all()

    # Get IDs of drives student already applied to
    applied_ids = [a.job_drive_id for a in
                   Application.query.filter_by(student_id=profile.id).all()] if profile else []

    return render_template('student/drives.html',
                           drives=all_drives,
                           applied_ids=applied_ids,
                           profile=profile)


# ── APPLY TO DRIVE ────────────────────────────────────────────────────────────
@student.route('/student/apply/<int:drive_id>')
@login_required
@student_required
def apply(drive_id):
    profile = Student.query.filter_by(user_id=current_user.id).first()
    drive   = JobDrive.query.get_or_404(drive_id)

    # Check already applied
    existing = Application.query.filter_by(
                   student_id=profile.id,
                   job_drive_id=drive_id
               ).first()
    if existing:
        flash('You have already applied to this drive.', 'warning')
        return redirect(url_for('student.drives'))

    # Check eligibility
    if profile.cgpa < drive.min_cgpa:
        flash(f'Your CGPA ({profile.cgpa}) is below the required {drive.min_cgpa}.', 'danger')
        return redirect(url_for('student.drives'))

    if drive.allowed_branches:
        allowed = [b.strip() for b in drive.allowed_branches.split(',')]
        if profile.branch not in allowed:
            flash(f'Your branch ({profile.branch}) is not eligible for this drive.', 'danger')
            return redirect(url_for('student.drives'))

    if profile.backlogs > drive.max_backlogs:
        flash(f'You have {profile.backlogs} backlogs. Max allowed is {drive.max_backlogs}.', 'danger')
        return redirect(url_for('student.drives'))

    # Check deadline
    if drive.apply_deadline and datetime.utcnow() > drive.apply_deadline:
        flash('Application deadline has passed.', 'danger')
        return redirect(url_for('student.drives'))

    # All good — create application
    application = Application(
        student_id   = profile.id,
        job_drive_id = drive_id,
        status       = 'applied'
    )
    db.session.add(application)
    db.session.commit()
    flash(f'Successfully applied to {drive.title}!', 'success')
    return redirect(url_for('student.my_applications'))


# ── MY APPLICATIONS ───────────────────────────────────────────────────────────
@student.route('/student/applications')
@login_required
@student_required
def my_applications():
    profile      = Student.query.filter_by(user_id=current_user.id).first()
    applications = Application.query.filter_by(
                       student_id=profile.id
                   ).order_by(Application.applied_at.desc()).all()
    return render_template('student/applications.html', applications=applications)
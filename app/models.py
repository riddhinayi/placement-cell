from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─── USER (common login for all roles) ───────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password      = db.Column(db.String(200), nullable=False)
    role          = db.Column(db.String(20), nullable=False)  # 'admin' | 'student' | 'company'
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student       = db.relationship('Student', backref='user', uselist=False)
    company       = db.relationship('Company', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.email} | {self.role}>'


# ─── STUDENT PROFILE ─────────────────────────────────────────────────────────
class Student(db.Model):
    __tablename__ = 'students'

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    roll_number   = db.Column(db.String(30), unique=True, nullable=False)
    branch        = db.Column(db.String(50), nullable=False)   # CSE, IT, ECE, etc.
    cgpa          = db.Column(db.Float, nullable=False)
    backlogs      = db.Column(db.Integer, default=0)
    phone         = db.Column(db.String(15))
    skills        = db.Column(db.Text)                         # comma-separated
    resume_url    = db.Column(db.String(200))
    is_placed     = db.Column(db.Boolean, default=False)

    # Relationships
    applications  = db.relationship('Application', backref='student', lazy=True)

    def __repr__(self):
        return f'<Student {self.roll_number}>'


# ─── COMPANY PROFILE ──────────────────────────────────────────────────────────
class Company(db.Model):
    __tablename__ = 'companies'

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    company_name  = db.Column(db.String(100), nullable=False)
    industry      = db.Column(db.String(50))                   # IT, Finance, Core, etc.
    website       = db.Column(db.String(100))
    description   = db.Column(db.Text)
    location      = db.Column(db.String(100))
    is_approved   = db.Column(db.Boolean, default=False)       # Admin approves company

    # Relationships
    job_drives    = db.relationship('JobDrive', backref='company', lazy=True)

    def __repr__(self):
        return f'<Company {self.company_name}>'


# ─── JOB DRIVE ───────────────────────────────────────────────────────────────
class JobDrive(db.Model):
    __tablename__ = 'job_drives'

    id              = db.Column(db.Integer, primary_key=True)
    company_id      = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    title           = db.Column(db.String(100), nullable=False)  # Job title
    description     = db.Column(db.Text)
    job_type        = db.Column(db.String(30))                   # Full-time | Internship
    package         = db.Column(db.Float)                        # CTC in LPA
    location        = db.Column(db.String(100))

    # Eligibility criteria
    min_cgpa        = db.Column(db.Float, default=0.0)
    allowed_branches= db.Column(db.String(200))                  # CSE,IT,ECE
    max_backlogs    = db.Column(db.Integer, default=0)

    # Drive dates
    drive_date      = db.Column(db.DateTime)
    apply_deadline  = db.Column(db.DateTime)

    # Status
    is_active       = db.Column(db.Boolean, default=True)
    is_approved     = db.Column(db.Boolean, default=False)       # Admin approves drive
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications    = db.relationship('Application', backref='job_drive', lazy=True)

    def __repr__(self):
        return f'<JobDrive {self.title}>'


# ─── APPLICATION ─────────────────────────────────────────────────────────────
class Application(db.Model):
    __tablename__ = 'applications'

    id            = db.Column(db.Integer, primary_key=True)
    student_id    = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_drive_id  = db.Column(db.Integer, db.ForeignKey('job_drives.id'), nullable=False)

    applied_at    = db.Column(db.DateTime, default=datetime.utcnow)
    status        = db.Column(db.String(30), default='applied')
    # Status flow: applied → shortlisted → interview → selected | rejected

    interview_date= db.Column(db.DateTime)
    interview_round = db.Column(db.String(50))                   # Aptitude, Technical, HR
    feedback      = db.Column(db.Text)

    def __repr__(self):
        return f'<Application student={self.student_id} drive={self.job_drive_id}>'
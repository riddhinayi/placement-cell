from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class CompanyProfileForm(FlaskForm):
    company_name = StringField('Company Name',
                   validators=[DataRequired(), Length(min=2, max=100)])
    industry     = SelectField('Industry', choices=[
                     ('IT',      'Information Technology'),
                     ('Finance', 'Finance & Banking'),
                     ('Core',    'Core Engineering'),
                     ('Consult', 'Consulting'),
                     ('Product', 'Product Based'),
                     ('Service', 'Service Based'),
                     ('Other',   'Other'),
                   ])
    website      = StringField('Website URL', validators=[Optional(), Length(max=100)])
    location     = StringField('Location',    validators=[Optional(), Length(max=100)])
    description  = TextAreaField('About Company', validators=[Optional(), Length(max=500)])
    submit       = SubmitField('Save Profile')


class JobDriveForm(FlaskForm):
    title            = StringField('Job Title',
                       validators=[DataRequired(), Length(min=2, max=100)])
    description      = TextAreaField('Job Description',
                       validators=[Optional(), Length(max=1000)])
    job_type         = SelectField('Job Type', choices=[
                         ('Full-time',  'Full-time'),
                         ('Internship', 'Internship'),
                         ('Part-time',  'Part-time'),
                       ])
    package          = FloatField('Package (LPA)',
                       validators=[DataRequired(), NumberRange(min=0)])
    location         = StringField('Job Location',
                       validators=[Optional(), Length(max=100)])
    min_cgpa         = FloatField('Minimum CGPA',
                       validators=[DataRequired(), NumberRange(min=0.0, max=10.0)])
    allowed_branches = StringField('Allowed Branches (comma separated)',
                       validators=[Optional(), Length(max=200)])
    max_backlogs     = IntegerField('Max Backlogs Allowed',
                       validators=[NumberRange(min=0)])
    drive_date       = StringField('Drive Date (YYYY-MM-DD)',
                       validators=[Optional()])
    apply_deadline   = StringField('Application Deadline (YYYY-MM-DD)',
                       validators=[Optional()])
    submit           = SubmitField('Post Drive')
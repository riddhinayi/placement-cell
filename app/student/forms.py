from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class StudentProfileForm(FlaskForm):
    roll_number = StringField('Roll Number',
                  validators=[DataRequired(), Length(min=3, max=30)])
    branch      = SelectField('Branch', choices=[
                    ('CSE','Computer Science (CSE)'),
                    ('IT','Information Technology (IT)'),
                    ('ECE','Electronics & Communication (ECE)'),
                    ('ME','Mechanical Engineering (ME)'),
                    ('CE','Civil Engineering (CE)'),
                    ('EE','Electrical Engineering (EE)'),
                  ])
    cgpa        = FloatField('CGPA',
                  validators=[DataRequired(), NumberRange(min=0.0, max=10.0)])
    backlogs    = IntegerField('Active Backlogs',
                  validators=[NumberRange(min=0, max=20)])
    phone       = StringField('Phone Number',
                  validators=[Length(max=15)])
    skills      = TextAreaField('Skills (comma separated)',
                  validators=[Length(max=500)])
    resume_url  = StringField('Resume Link (Google Drive / URL)',
                  validators=[Length(max=200)])
    submit      = SubmitField('Save Profile')
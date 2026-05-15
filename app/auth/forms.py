from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    name     = StringField('Full Name',
                validators=[DataRequired(), Length(min=2, max=100)])
    email    = StringField('Email',
                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                validators=[DataRequired(), Length(min=6)])
    confirm  = PasswordField('Confirm Password',
                validators=[DataRequired(), EqualTo('password')])
    role     = SelectField('Register As',
                choices=[('student','Student'), ('company','Company')])
    submit   = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please login.')


class LoginForm(FlaskForm):
    email    = StringField('Email',
                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                validators=[DataRequired()])
    submit   = SubmitField('Login')
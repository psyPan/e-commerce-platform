from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from store.users.models import User

class RegistrationForm(FlaskForm):
    # 'Username' will be used as label in html
    f_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter your First Name"})
    l_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter your Last Name"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "your_email@example.com"})
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username): # this validation is needed because we set 'User's username' as 'unique' in models.py
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
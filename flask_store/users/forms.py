from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_store.users.models import User
from flask_store.stores.models import Store

class RegistrationForm(FlaskForm):
    f_name = StringField('First Name', 
                         validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter your First Name"})
    l_name = StringField('Last Name', 
                         validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter your Last Name"})
    email = StringField('Email', 
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "your_email@example.com"})
    birth = DateField('Birthday', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=10)], render_kw={"placeholder": "09XXXXXXXX"})
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone is already in use. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    birth = DateField('Birthday', format='%Y-%m-%d')
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    address = StringField('Address')
    submit = SubmitField('Save')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class AssignOwnerForm(FlaskForm):
    owner_email = StringField('Email', validators=[DataRequired(), Email()])
    store_id = SelectField('Store Name', validators=[DataRequired()], choices=[])
    submit = SubmitField('Assign')

# ===============================
# ADMIN – CREATE CUSTOMER
# ===============================
class CreateCustomerForm(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Create Customer')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already exists.')

# ===============================
# ADMIN – CREATE OWNER
# ===============================
class CreateOwnerForm(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    store_id = SelectField(
        'Assign Store',
        coerce=int,
        validators=[DataRequired()],
        choices=[]
    )

    submit = SubmitField('Create Owner')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already exists.')

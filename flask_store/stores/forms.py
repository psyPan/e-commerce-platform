from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_store.stores.models import Store

class StoreForm(FlaskForm):
    store_name = StringField('Store Name', validators=[DataRequired(), Length(min=2, max=20)])
    owner_f_name = StringField('Owner First Name', validators=[DataRequired(), Length(min=2, max=20)])
    owner_l_name = StringField('Owner Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                         validators=[DataRequired(), Email()], render_kw={"placeholder": "email@example.com"})
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=10)], render_kw={"placeholder": "09XXXXXXXX"})
    submit = SubmitField('Create Store')

    def validate_store_name(self, store_name):
        store = Store.query.filter_by(name=store_name.data).first()
        if store:
            raise ValidationError('That store name is already taken. Please choose a different one.')

    def validate_email(self, email):
        store = Store.query.filter_by(email=email.data).first()
        if store:
            raise ValidationError('That email is already registered. Please choose a different one.')
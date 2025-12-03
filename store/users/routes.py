from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from store import db, bcrypt
from store.users.forms import RegistrationForm
from store.users.models import User

users = Blueprint('users', __name__)

@users.route('/')
@users.route('/home')
def home():
    return "Hello world"

@users.route('/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # utf-8 creates 'string' type hashed password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit() # saving data in database
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)
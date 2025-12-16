from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_store import db, bcrypt
from flask_store.users.forms import RegistrationForm, LoginForm, EditProfileForm
from flask_store.users.models import User

users = Blueprint('users', __name__)

@users.route('/')
@users.route('/home')
def home():
    return render_template('home.html', title='Home')

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(f_name=form.f_name.data, l_name=form.l_name.data, 
                    email=form.email.data, password=hashed_password, phone=form.phone.data,
                    birth=form.birth.data, address=form.address.data, a_flag=False, o_flag=False, c_flag=True)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.home'))
    return render_template('register.html',title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/credit')
def credit():
    return render_template('credit_card.html')

@users.route('/profile', methods=['GET', 'POST'])
def profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.f_name = form.f_name.data
        current_user.l_name = form.l_name.data
        current_user.birth = form.birth.data
        current_user.gender = form.gender.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data

        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for("users.profile"))

    return render_template(
        'profile.html',
        form=form
    )

@users.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        return redirect(url_for("users.profile"))

    return render_template("change_password.html")

@users.route('/order_history')
def order_history():
    return render_template('order_history.html')


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
        return redirect(url_for('users.login'))
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
@login_required
def profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.f_name = form.f_name.data
        current_user.l_name = form.l_name.data
        current_user.birth = form.birth.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data

        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for("users.profile"))

    return render_template(
        'profile.html',
        form=form
    )

# Alternative: Separate route for update
@users.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    """Handle profile update"""
    form = EditProfileForm()
    
    if form.validate_on_submit():
        current_user.f_name = form.f_name.data
        current_user.l_name = form.l_name.data
        current_user.birth = form.birth.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'danger')
    else:
        # Display validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    
    return redirect(url_for('users.profile'))

@users.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        return redirect(url_for("users.profile"))

    return render_template("change_password.html")

@users.route('/order_history')
def order_history():
    return render_template('order_history.html')


# admin youssel test
@users.route('/admin/user-management')
# @login_required
def user_list():
    return render_template('admin/user_management.html')

@users.route('/admin/user/1')
# @login_required
def user_detail():
    return render_template('admin/user_detail.html')

@users.route('/admin/user/1/edit')
# @login_required
def user_edit():
    return render_template('admin/user_edit.html')

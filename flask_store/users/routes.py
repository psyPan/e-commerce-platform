from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_store import db, bcrypt
from flask_store.products.forms import ProductForm
from flask_store.users.forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm
from flask_store.users.models import User
from flask_store.orders.models import Order
from flask_store.line_items.models import LineItem
from flask_store.products.models import Product


users = Blueprint('users', __name__)

@users.route('/')
@users.route('/home')
def home():
    return render_template('/customer/home.html', title='Home')

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
    return render_template('old/register.html',title='Register', form=form)

@users.route('/register_owner', methods=['GET', 'POST'])
@login_required
def register_owner():
    if not current_user.a_flag:
        flash('You do not have permission to this page', 'danger')
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        owner = User(f_name=form.f_name.data, l_name=form.l_name.data, 
                    email=form.email.data, password=hashed_password, phone=form.phone.data,
                    birth=form.birth.data, address=form.address.data, a_flag=False, o_flag=True, c_flag=False)
        try:
            db.session.add(owner)
            db.session.commit()
            flash(f'Owner account "{owner.email}" created successfully!', 'success')
            return redirect(url_for('users.home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the owner account.', 'danger')
            return render_template('old/test_product.html', form=form)
    return render_template('old/register.html',title='Register Owner', form=form)

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
    return render_template('old/login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/credit')
def credit():
    return render_template('old/credit_card.html')

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
        'old/profile.html',
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
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not (bcrypt.check_password_hash(current_user.password, form.current_password.data)):
            flash('Current password is not correct!', 'danger')
            return redirect(url_for('users.change_password'))
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        if form.current_password.data == form.new_password.data:
            flash('Your new password is the same as your old password!', 'info')
        else:
            current_user.password = hashed_password
            db.session.commit()
            flash('New password updated!', 'success')
            return redirect(url_for("users.profile"))
    else:
        print(f"Form validation failed: {form.errors}")
    return render_template("old/change_password.html", form=form)

@users.route("/order_history")
@login_required
def order_history():
    # Fetch orders belonging to the current user, ordered by newest first
    orders = Order.query.filter_by(customer_id=current_user.id)\
                        .order_by(Order.id.desc())\
                        .all()
    
    return render_template('old/order_history.html', orders=orders)


# admin youssel test
@users.route('/admin/user-management')
# @login_required
def user_list():
    return render_template('old/admin/user_management.html')

@users.route('/admin/user/1')
# @login_required
def user_detail():
    return render_template('old/admin/user_detail.html')

@users.route('/admin/user/1/edit')
# @login_required
def user_edit():
    return render_template('old/admin/user_edit.html')

# to see credit card page
@users.route('/cart')
# @login_required
def my_cart():
    return render_template('cart.html')

@users.route('/test_product')
def test_product():
    form = ProductForm()
    return render_template('old/test_product.html', form=form)

@users.route("/order/<int:order_id>/cancel", methods=['POST'])
@login_required
def cancel_order(order_id):
    # 1. Get the order
    order = Order.query.get_or_404(order_id)
            
    # 3. Status Check: Only allow cancelling if it hasn't shipped yet
    if order.status not in ['received', 'processed']:
        flash('This order cannot be cancelled because it has already been shipped or closed.', 'danger')
        return redirect(url_for('users.order_history'))

    # 4. RESTORE STOCK (Critical Step)
    # We must find all items in this order and add their quantity back to the Product stock
    # Assuming you have a relationship or we query LineItem directly:
    order_items = LineItem.query.filter_by(order_id=order.id).all()
    
    for item in order_items:
        product = Product.query.get(item.product_id)
        if product:
            product.stock += item.quantity

    # 5. DELETE THE ORDER
    # We delete the line items first to avoid foreign key errors (unless you have cascading delete set up)
    for item in order_items:
        db.session.delete(item)
        
    db.session.delete(order)
    db.session.commit()
    
    flash('Your order has been successfully cancelled.', 'success')
    return redirect(url_for('users.order_history'))
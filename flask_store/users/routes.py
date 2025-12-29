from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_store import db, bcrypt
from flask_store.products.forms import ProductForm
from flask_store.users.forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, AssignOwnerForm
from flask_store.users.models import User
from flask_store.orders.models import Order
from flask_store.stores.models import Store
from flask_store.line_items.models import LineItem
from flask_store.products.models import Product
from flask_store.reviews.models import Review
from flask_store.reviews.forms import ReviewForm
from datetime import datetime


users = Blueprint('users', __name__)

@users.route('/')
@users.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    stores_pagination = Store.query.paginate(page=page, per_page=5, error_out=False)
    return render_template('/customer/home.html', title='Home', stores=stores_pagination.items, pagination=stores_pagination)

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
    return render_template('common/login.html', title='Login', form=form)

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

# In flask_store/users/routes.py

@users.route("/order_history")
@login_required
def order_history():
    # 1. Fetch orders
    orders = Order.query.filter_by(customer_id=current_user.id)\
                        .order_by(Order.id.desc())\
                        .all()
    
    review_form = ReviewForm()
    user_reviews = Review.query.filter_by(user_id=current_user.id).all()
    reviewed_map = {f"{r.order_id}-{r.product_id}" for r in user_reviews}

    return render_template('old/order_history.html', 
                           orders=orders, 
                           review_form=review_form,
                           reviewed_map=reviewed_map)

# admin youssel test
# @login_required
@users.route('/admin/user-management')
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
    return render_template('old/cart.html')

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

  
    for item in order_items:
        db.session.delete(item)
        
    db.session.delete(order)
    db.session.commit()
    
    flash('Your order has been successfully cancelled.', 'success')
    return redirect(url_for('users.order_history'))

@users.route("/assign_owner", methods=["GET", "POST"])
@login_required
def assign_owner():
    if not current_user.a_flag:
        flash('You do not have permission to this page', 'danger')
        return redirect(url_for('users.home'))
    form = AssignOwnerForm()
    stores = Store().query.all()
    form.store_id.choices = [(s.id, s.name) for s in stores]
    if form.validate_on_submit():
        owner = User.query.filter_by(email=form.owner_email.data, o_flag=True).first()
        store = Store.query.filter_by(id=form.store_id.data).first()
        if not owner:
            flash('Owner Not Found!', 'danger')
            return redirect(url_for('users.assign_owner'))
        elif not store:
            flash('Store Not Found!', 'danger')
            return redirect(url_for('users.assign_owner'))
        else:
            owner.store_id = store.id
        try:
            db.session.commit()
            flash('Owner assigned to store successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error assigning owner to store. Please try again.', 'danger')
    else:
        print(f"Form validation failed: {form.errors}")
    return render_template("owner/assign_owner.html", form=form)

@users.route("/store/manage-orders", methods=["GET", "POST"])
@login_required
def manage_orders():
    # 1. Security: Ensure the user actually owns a store
    # (Assuming a user can own one store for simplicity)
    my_store = current_user.store    
    if not my_store:
        flash("You need to create a store before you can process orders!", "warning")
        return redirect(url_for('users.account')) # Or create_store route

    # 2. HANDLE STATUS UPDATES (POST Request)
    if request.method == "POST":
        order_id = request.form.get('order_id')
        new_status = request.form.get('order_status')
        
        # specific order lookup
        order_to_update = Order.query.get_or_404(order_id)
        
        # Basic validation
        valid_statuses = ['received', 'processed', 'shipped', 'delivered', 'closed']
        if new_status in valid_statuses:
            order_to_update.status = new_status
            db.session.commit()
            flash(f"Order #{order_id} status updated to '{new_status}'", "success")
        else:
            flash("Invalid status selected.", "danger")
            
        return redirect(url_for('users.manage_orders'))

    # 3. FETCH ORDERS (GET Request)
    # This query joins tables to find Orders containing Products from My Store
    # Logic: Order -> LineItems -> Product -> Store (matches my_store.id)
    orders = db.session.query(Order)\
        .join(LineItem)\
        .join(Product)\
        .filter(Product.store_id == my_store.id)\
        .order_by(Order.order_time.desc())\
        .distinct()\
        .all()

    return render_template('owner/manage_orders.html', orders=orders)

@users.route('/order/<int:order_id>/product/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(order_id, product_id):
    form = ReviewForm()
    
    # 1. Validation: Does the order exist and belong to user?
    order = Order.query.get_or_404(order_id)
    if order.customer_id != current_user.id:
        abort(403)
        
    # 2. Validation: Is the order completed?
    # Note: I removed the redirect to 'order_details' here
    if order.status not in ['closed']: 
        flash('You can only review products from completed orders.', 'warning')
        return redirect(url_for('users.order_history'))

    # 3. Check if they already reviewed this item in this specific order
    existing_review = Review.query.filter_by(
        order_id=order_id, 
        product_id=product_id, 
        user_id=current_user.id
    ).first()

    if existing_review:
        flash('You have already reviewed this item.', 'info')
        return redirect(url_for('users.order_history'))

    # 4. Save the Review
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            order_id=order_id,
            product_id=product_id,
            stars=int(form.stars.data),
            description=form.description.data,
            review_time=datetime.utcnow()
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully!', 'success')
    else:
        # If form errors exist, flash them
        flash('Error submitting review. Please check the form.', 'danger')

    # CRITICAL CHANGE: Redirect back to Order History, not Order Details
    return redirect(url_for('users.order_history'))
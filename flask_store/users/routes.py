from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_store import db, bcrypt
from flask_store.products.forms import ProductForm
from flask_store.users.forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, AssignOwnerForm, CreateOwnerForm, CreateCustomerForm
from flask_store.users.models import User
from flask_store.orders.models import Order
from flask_store.stores.models import Store
from flask_store.line_items.models import LineItem
from flask_store.products.models import Product
from flask_store.reviews.models import Review
from flask_store.reviews.forms import ReviewForm
from datetime import datetime, timedelta
from sqlalchemy import or_, func, case
from flask_store.credit_card.models import CreditCard # Import your new model


users = Blueprint('users', __name__)

@users.route('/')
@users.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    stores_pagination = Store.query.paginate(page=page, per_page=5, error_out=False)
    return render_template('/common/home.html', title='Home', stores=stores_pagination.items, pagination=stores_pagination)

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
    return render_template('common/register.html',title='Register', form=form)

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
    return render_template('common/register.html',title='Register Owner', form=form)

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
    return render_template('customer/credit_card.html')

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
        'customer/my_profile.html',
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
    return render_template("customer/change_password.html", form=form)

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

    return render_template('customer/my_order.html', 
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
    my_store = current_user.store    
    if not my_store:
        flash("You need to create a store before you can process orders!", "warning")
        return redirect(url_for('users.account'))

    # 2. HANDLE STATUS UPDATES (POST Request)
    if request.method == "POST":
        order_id = request.form.get('order_id')
        new_status = request.form.get('order_status')
        
        # Specific order lookup
        order_to_update = Order.query.get_or_404(order_id)
        
        # Basic validation
        valid_statuses = ['received', 'processed', 'shipped', 'delivered', 'closed']
        if new_status in valid_statuses:
            order_to_update.status = new_status
            
            # Update completion time if order is closed
            if new_status == 'closed':
                from datetime import datetime
                order_to_update.completion_time = datetime.utcnow()
            
            db.session.commit()
            flash(f"Order #{order_id} status updated to '{new_status}'", "success")
        else:
            flash("Invalid status selected.", "danger")
            
        return redirect(url_for('users.manage_orders'))

    # 3. GET FILTER PARAMETERS
    status_filter = request.args.get('status', 'all')  # Default: show all
    search_query = request.args.get('q', '').strip()    # Search by order ID or customer
    sort_by = request.args.get('sort', 'newest')        # Sort option
    page = request.args.get('page', 1, type=int)        # Current page
    per_page = 10                                        # Orders per page

    # 4. BASE QUERY - Orders containing products from my store
    orders_query = db.session.query(Order)\
        .join(LineItem)\
        .join(Product)\
        .filter(Product.store_id == my_store.id)

    # 5. APPLY STATUS FILTER
    if status_filter != 'all':
        orders_query = orders_query.filter(Order.status == status_filter)

    # 6. APPLY SEARCH FILTER (by order ID or customer name/email)
    if search_query:
        from flask_store.users.models import User
        orders_query = orders_query.join(User, Order.customer_id == User.id)\
            .filter(
                or_(
                    Order.id.like(f'%{search_query}%'),
                    User.f_name.ilike(f'%{search_query}%'),
                    User.l_name.ilike(f'%{search_query}%'),
                    User.email.ilike(f'%{search_query}%')
                )
            )

    # 7. APPLY SORTING
    if sort_by == 'oldest':
        orders_query = orders_query.order_by(Order.order_time.asc())
    elif sort_by == 'highest':
        orders_query = orders_query.order_by(Order.total_amount.desc())
    elif sort_by == 'lowest':
        orders_query = orders_query.order_by(Order.total_amount.asc())
    else:  # 'newest' (default)
        orders_query = orders_query.order_by(Order.order_time.desc())

    # 8. REMOVE DUPLICATES
    orders_query = orders_query.distinct()

    # 9. PAGINATE
    orders_pagination = orders_query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    orders = orders_pagination.items

    # 10. GET STATUS COUNTS FOR FILTER BADGES
    status_counts = {}
    base_count_query = db.session.query(Order)\
        .join(LineItem)\
        .join(Product)\
        .filter(Product.store_id == my_store.id)\
        .distinct()
    
    status_counts['all'] = base_count_query.count()
    for status in ['received', 'processed', 'shipped', 'delivered', 'closed']:
        status_counts[status] = base_count_query.filter(Order.status == status).count()

    return render_template(
        'owner/manage_orders.html', 
        orders=orders,
        pagination=orders_pagination,
        status_counts=status_counts,
        current_filters={
            'status': status_filter,
            'search': search_query,
            'sort': sort_by
        }
    )

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


users.route("/credit", methods=['GET'])
@login_required
def credit():
    return render_template('credit.html')


@users.route("/credit/add", methods=['POST'])
@login_required
def add_card():
    # 1. Get data from form
    name = request.form.get('name')
    card_number = request.form.get('card_number')
    expiry_str = request.form.get('expiry') # Format "MM/YY"
    cvv = request.form.get('cvv')

    # 2. Basic Validation
    if not card_number or len(card_number) < 13:
        flash('Invalid card number', 'danger')
        return redirect(url_for('users.credit'))

    # 3. Convert MM/YY to Python Date object
    try:
        # We set day to 1st of the month arbitrarily
        expiry_date = datetime.strptime(expiry_str, '%m/%y').date()
    except ValueError:
        flash('Invalid date format. Use MM/YY', 'danger')
        return redirect(url_for('users.credit'))

    # 4. Save to DB
    new_card = CreditCard(
        user_id=current_user.id,
        name=name,
        Card_Number=card_number,
        Expiration_Date=expiry_date,
        CVV=cvv,
        is_active=True
    )
    
    db.session.add(new_card)
    db.session.commit()
    
    flash('Card added successfully!', 'success')
    return redirect(url_for('users.credit'))


@users.route("/credit/delete/<int:card_id>", methods=['POST'])
@login_required
def delete_card(card_id):
    card = CreditCard.query.get_or_404(card_id)
    
    # Security: Ensure user owns this card
    if card.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('users.credit'))
    
    # Soft Delete (Set is_active to False)
    card.is_active = False
    db.session.commit()
    
    flash('Card removed.', 'info')
    return redirect(url_for('users.credit'))

#admin user management
@users.route('/user_management', methods=['GET', 'POST'])
@login_required
def user_management():
    # Admin only
    if not current_user.a_flag:
        abort(403)

    form = CreateOwnerForm()

    # Populate store dropdown
    form.store_id.choices = [
        (s.id, s.name) for s in Store.query.order_by(Store.name).all()
    ]

    # ===============================
    # DELETE USER
    # ===============================
    if request.method == "POST" and "delete_user_id" in request.form:
        user = User.query.get_or_404(request.form.get("delete_user_id"))

        if user.a_flag:
            flash("Cannot delete administrator", "danger")
        else:
            db.session.delete(user)
            db.session.commit()
            flash("User deleted successfully", "success")

        return redirect(url_for('users.user_management'))

    # ===============================
    # CREATE OWNER
    # ===============================
    if "create_owner" in request.form and form.validate_on_submit():
        owner = User(
            f_name=form.f_name.data,
            l_name=form.l_name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=form.password.data,
            a_flag=False,
            o_flag=True,
            c_flag=False,
            store_id=form.store_id.data
        )
        db.session.add(owner)
        db.session.commit()

        flash("Owner created successfully", "success")
        return redirect(url_for('users.user_management'))

    # ===============================
    # LIST + SEARCH + FILTER
    # ===============================
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    filter_by = request.args.get('filter_by', 'all')

    query = User.query

    if search:
        query = query.filter(
            or_(
                User.f_name.ilike(f'%{search}%'),
                User.l_name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )

    if filter_by == "administrator":
        query = query.filter(User.a_flag == True)
    elif filter_by == "owner":
        query = query.filter(User.o_flag == True)
    elif filter_by == "customer":
        query = query.filter(User.c_flag == True)

    pagination = query.order_by(User.id).paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    users_data = []
    for u in pagination.items:
        role = "Administrator" if u.a_flag else "Owner" if u.o_flag else "Customer"
        users_data.append({
            "id": u.id,
            "name": f"{u.f_name} {u.l_name}",
            "email": u.email,
            "type": role
        })

    return render_template(
        "admin/user_management.html",
        users=users_data,
        pagination=pagination,
        owner_form=form
    )

@users.route('/financial_report')
@login_required
def financial_report():
    # Admin only
    if not current_user.a_flag:
        abort(403)
    
    # Get all stores with their financial data
    stores = Store.query.all()
    
    financial_data = []
    
    for store in stores:
        # Get all products for this store
        product_ids = [p.id for p in store.products]
        
        if not product_ids:
            # Store has no products
            financial_data.append({
                'store_id': store.id,
                'store_name': store.name,
                'total_revenue': 0,
                'total_orders': 0,
                'total_products_sold': 0,
                'average_order_value': 0,
                'pending_revenue': 0,
                'completed_revenue': 0,
                'active_products': 0,
                'total_products': 0,
                'current_balance': store.balance or 0,
                'revenue_this_month': 0,
                'revenue_last_month': 0,
                'growth_rate': 0
            })
            continue
        
        # Calculate total revenue from completed orders
        completed_orders = db.session.query(
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('total_revenue')
        ).join(LineItem, Order.id == LineItem.order_id)\
         .filter(
             LineItem.product_id.in_(product_ids),
             Order.status == 'closed'
         ).first()
        
        # Calculate pending revenue (orders not yet closed)
        pending_orders = db.session.query(
            func.sum(Order.total_amount).label('pending_revenue')
        ).join(LineItem, Order.id == LineItem.order_id)\
         .filter(
             LineItem.product_id.in_(product_ids),
             Order.status.in_(['received', 'processed', 'shipped'])
         ).first()
        
        # Total products sold (quantity from completed orders)
        products_sold = db.session.query(
            func.sum(LineItem.quantity).label('total_sold')
        ).join(Order, LineItem.order_id == Order.id)\
         .filter(
             LineItem.product_id.in_(product_ids),
             Order.status == 'closed'
         ).first()
        
        # Active products count
        active_products = Product.query.filter(
            Product.store_id == store.id,
            Product.is_active == True,
            Product.is_deleted == False
        ).count()
        
        total_products = Product.query.filter(
            Product.store_id == store.id,
            Product.is_deleted == False
        ).count()
        
        # Revenue this month
        first_day_this_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        revenue_this_month = db.session.query(
            func.sum(Order.total_amount)
        ).join(LineItem, Order.id == LineItem.order_id)\
         .filter(
             LineItem.product_id.in_(product_ids),
             Order.status == 'closed',
             Order.completion_time >= first_day_this_month
         ).scalar() or 0
        
        # Revenue last month
        first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)
        revenue_last_month = db.session.query(
            func.sum(Order.total_amount)
        ).join(LineItem, Order.id == LineItem.order_id)\
         .filter(
             LineItem.product_id.in_(product_ids),
             Order.status == 'closed',
             Order.completion_time >= first_day_last_month,
             Order.completion_time < first_day_this_month
         ).scalar() or 0
        
        # Calculate growth rate
        if revenue_last_month > 0:
            growth_rate = ((revenue_this_month - revenue_last_month) / revenue_last_month) * 100
        elif revenue_this_month > 0:
            growth_rate = 100
        else:
            growth_rate = 0
        
        total_revenue = completed_orders.total_revenue or 0
        order_count = completed_orders.order_count or 0
        avg_order_value = (total_revenue / order_count) if order_count > 0 else 0
        
        financial_data.append({
            'store_id': store.id,
            'store_name': store.name,
            'total_revenue': total_revenue,
            'total_orders': order_count,
            'total_products_sold': products_sold.total_sold or 0,
            'average_order_value': avg_order_value,
            'pending_revenue': pending_orders.pending_revenue or 0,
            'completed_revenue': total_revenue,
            'active_products': active_products,
            'total_products': total_products,
            'current_balance': store.balance or 0,
            'revenue_this_month': revenue_this_month,
            'revenue_last_month': revenue_last_month,
            'growth_rate': round(growth_rate, 2)
        })
    
    # Calculate platform totals
    platform_totals = {
        'total_revenue': sum(s['total_revenue'] for s in financial_data),
        'total_orders': sum(s['total_orders'] for s in financial_data),
        'total_products_sold': sum(s['total_products_sold'] for s in financial_data),
        'pending_revenue': sum(s['pending_revenue'] for s in financial_data),
        'total_stores': len(stores),
        'active_stores': sum(1 for s in financial_data if s['active_products'] > 0)
    }
    
    return render_template(
        'admin/financial_report.html',
        financial_data=financial_data,
        platform_totals=platform_totals
    )


@users.route('/financial_report/<int:store_id>')
@login_required
def store_financial_detail(store_id):
    # Admin only
    if not current_user.a_flag:
        abort(403)
    
    store = Store.query.get_or_404(store_id)
    
    # Get detailed product performance
    product_performance = db.session.query(
        Product.id,
        Product.name,
        Product.sell_price,
        Product.buy_price,
        Product.stock,
        func.sum(LineItem.quantity).label('total_sold'),
        func.sum(LineItem.total_price).label('total_revenue'),
        func.count(LineItem.id).label('order_count')
    ).join(LineItem, Product.id == LineItem.product_id)\
     .join(Order, LineItem.order_id == Order.id)\
     .filter(
         Product.store_id == store_id,
         Order.status == 'closed'
     ).group_by(Product.id).all()
    
    products_data = []
    for p in product_performance:
        profit_per_unit = p.sell_price - p.buy_price
        total_profit = profit_per_unit * (p.total_sold or 0)
        products_data.append({
            'id': p.id,
            'name': p.name,
            'sell_price': p.sell_price,
            'buy_price': p.buy_price,
            'stock': p.stock,
            'total_sold': p.total_sold or 0,
            'total_revenue': p.total_revenue or 0,
            'total_profit': total_profit,
            'order_count': p.order_count or 0
        })
    
    # Sort by total revenue
    products_data.sort(key=lambda x: x['total_revenue'], reverse=True)
    
    # Get monthly revenue trend (last 6 months)
    monthly_data = []
    for i in range(5, -1, -1):
        month_start = (datetime.now().replace(day=1) - timedelta(days=i*30)).replace(day=1)
        if i > 0:
            month_end = (datetime.now().replace(day=1) - timedelta(days=(i-1)*30)).replace(day=1)
        else:
            month_end = datetime.now()
        
        product_ids = [p.id for p in store.products]
        monthly_revenue = db.session.query(
            func.sum(Order.total_amount)
        ).join(LineItem, Order.id == LineItem.order_id)\
         .filter(
             LineItem.product_id.in_(product_ids),
             Order.status == 'closed',
             Order.completion_time >= month_start,
             Order.completion_time < month_end
         ).scalar() or 0
        
        monthly_data.append({
            'month': month_start.strftime('%B %Y'),
            'revenue': monthly_revenue
        })
    
    return render_template(
        'admin/store_financial_detail.html',
        store=store,
        products_data=products_data,
        monthly_data=monthly_data
    )
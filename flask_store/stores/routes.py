from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_store import db
from flask_store.stores.forms import StoreForm
from flask_store.users.models import User
from flask_store.stores.models import Store  
from flask_store.products.models import Product  # Add Product import

from sqlalchemy import func, or_, and_

stores = Blueprint('stores', __name__)

@stores.route('/add_store', methods=['GET', 'POST'])
def add_store():
    form = StoreForm()
    
    if form.validate_on_submit():
        # Search for user by first name and last name, and check if o_flag is True
        owner = User.query.filter_by(
            f_name=form.owner_f_name.data,
            l_name=form.owner_l_name.data,
            o_flag=True
        ).first()
        
        if not owner:
            flash('Owner not found or the user is not registered as an owner. Please verify the information.', 'danger')
            return render_template('add_store.html', title='New Store', form=form)
        
        # Create new store only if owner exists and is valid
        new_store = Store(
            name=form.store_name.data,
            email=form.email.data,
            phone=form.phone.data,
            balance=0  # Initialize with 0 balance
        )
        
        db.session.add(new_store)
        db.session.flush()  # Flush to get the store.id
        
        # Assign the store_id to the owner
        owner.store_id = new_store.id
        
        # Commit all changes
        db.session.commit()
        
        flash(f'Store {new_store.name} has been created and assigned to {owner.f_name} {owner.l_name}!', 'success')
        return redirect(url_for('users.home'))  # Redirect to appropriate page
    
    return render_template('add_store.html', title='New Store', form=form)

@stores.route('/stores')
def list_stores():
    """Display all stores with basic info"""
    page = request.args.get('page', 1, type=int)
    per_page = 9
    
    stores_pagination = Store.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Enhance store data with product counts
    store_data = []
    for store in stores_pagination.items:
        product_count = Product.query.filter_by(store_id=store.id).count()
        in_stock_count = Product.query.filter(
            Product.store_id == store.id,
            Product.stock > 0
        ).count()
        
        store_data.append({
            'store': store,
            'product_count': product_count,
            'in_stock_count': in_stock_count
        })
    
    return render_template('stores_list.html', 
                         stores=store_data,
                         pagination=stores_pagination)


@stores.route('/store/<int:store_id>')
def view_store(store_id):
    """Display a store with its products"""
    store = Store.query.get_or_404(store_id)
    
    # Get query parameters
    product_type = request.args.get('type')
    manufacturer = request.args.get('manufacturer')
    sort_by = request.args.get('sort', 'newest')
    search_query = request.args.get('q', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock_only = request.args.get('in_stock', 'false').lower() == 'true'
    
    # Base query
    products_query = Product.query.filter_by(store_id=store_id)
    
    # Apply filters
    if in_stock_only:
        products_query = products_query.filter(Product.stock > 0)
    if product_type:
        products_query = products_query.filter_by(type=product_type)
    if manufacturer:
        products_query = products_query.filter_by(manufacturer=manufacturer)
    if search_query:
        products_query = products_query.filter(
            or_(
                Product.name.ilike(f'%{search_query}%'),
                Product.description.ilike(f'%{search_query}%'),
                Product.model.ilike(f'%{search_query}%')
            )
        )
    if min_price is not None:
        products_query = products_query.filter(Product.sell_price >= min_price)
    if max_price is not None:
        products_query = products_query.filter(Product.sell_price <= max_price)
    
    # Sorting
    if sort_by == 'price_asc':
        products_query = products_query.order_by(Product.sell_price.asc())
    elif sort_by == 'price_desc':
        products_query = products_query.order_by(Product.sell_price.desc())
    elif sort_by == 'name':
        products_query = products_query.order_by(Product.name.asc())
    elif sort_by == 'discount':
        products_query = products_query.order_by(Product.discount.desc())
    else:
        products_query = products_query.order_by(Product.id.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12
    products_pagination = products_query.paginate(page=page, per_page=per_page, error_out=False)
    products = products_pagination.items
    
    # Get filter options
    types = db.session.query(Product.type).filter_by(store_id=store_id)\
        .filter(Product.type.isnot(None)).distinct().all()
    types = [t[0] for t in types]
    
    manufacturers = db.session.query(Product.manufacturer)\
        .filter_by(store_id=store_id)\
        .filter(Product.manufacturer.isnot(None)).distinct().all()
    manufacturers = [m[0] for m in manufacturers]
    
    # Get store owners
    owners = User.query.filter_by(store_id=store_id, o_flag=True).all()
    
    return render_template('store.html', 
                         store=store,
                         owners=owners,
                         products=products,
                         pagination=products_pagination,
                         types=types,
                         manufacturers=manufacturers,
                         current_filters={
                             'type': product_type,
                             'manufacturer': manufacturer,
                             'sort': sort_by,
                             'search': search_query,
                             'min_price': min_price,
                             'max_price': max_price,
                             'in_stock': in_stock_only
                         })


@stores.route('/store/<int:store_id>/product/<int:product_id>')
def product_detail(store_id, product_id):
    """View detailed information about a specific product"""
    store = Store.query.get_or_404(store_id)
    product = Product.query.filter_by(
        id=product_id,
        store_id=store_id
    ).first_or_404()
    
    # Get related products
    related_products = Product.query.filter(
        Product.store_id == store_id,
        Product.id != product_id,
        or_(
            Product.type == product.type,
            Product.manufacturer == product.manufacturer
        ),
        Product.stock > 0
    ).limit(4).all()
    
    return render_template('product_details.html',
                         store=store,
                         product=product,
                         related_products=related_products)


@stores.route('/store/<int:store_id>/deals')
def store_deals(store_id):
    """Show all discounted products in the store"""
    store = Store.query.get_or_404(store_id)
    
    products = Product.query.filter(
        Product.store_id == store_id,
        or_(
            Product.discount > 0,
            Product.discounted_price.isnot(None)
        ),
        Product.stock > 0
    ).order_by(Product.discount.desc()).all()
    
    return render_template('store_deals.html',
                         store=store,
                         products=products)


@stores.route('/search')
def global_search():
    """Search across all stores and products"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return redirect(url_for('stores.list_stores'))
    
    # Search products
    products = Product.query.filter(
        or_(
            Product.name.ilike(f'%{query}%'),
            Product.description.ilike(f'%{query}%'),
            Product.manufacturer.ilike(f'%{query}%')
        )
    ).limit(20).all()
    
    # Search stores
    stores_found = Store.query.filter(
        or_(
            Store.name.ilike(f'%{query}%'),
            Store.address.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return render_template('search_results.html',
                         query=query,
                         products=products,
                         stores=stores_found)



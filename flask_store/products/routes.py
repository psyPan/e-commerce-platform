from ast import mod
from itertools import product
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flask_store import db
from flask_store.products.models import Product
from flask_store.discounts.models import Discount
from flask_store.stores.models import Store
from flask_store.reviews.models import Review
from flask_store.products.forms import ProductForm
from flask_store.products.utils import save_picture

products = Blueprint('products', __name__)

@products.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.c_flag: # is customer
        flash('You do not have permission to this page', 'danger')
        return redirect(url_for('users.home'))
    if not current_user.store_id:
        flash('You need to create a store first', 'danger')
        return redirect(url_for('stores.store_info'))
    form = ProductForm()
    discounts = Discount.query.all()
    form.discount_code.choices = [(d.code, d.code) for d in discounts]
     # Get page number and filters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'all')
    
    # Filter by current user's store only
    query = Product.query.filter_by(store_id=current_user.store_id)
    
    # Apply search filter
    if search_query:
        query = query.filter(Product.name.contains(search_query))
    
    # Apply filters
    if filter_by == 'in_stock':
        query = query.filter(Product.stock > 0)
    elif filter_by == 'out_of_stock':
        query = query.filter(Product.stock == 0)
    elif filter_by == 'with_discount':
        query = query.filter(Product.discount_obj != None)
    elif filter_by == 'no_discount':
        query = query.filter(Product.discount_obj == None)
    # 'all' shows both active and deleted
    
    # Paginate
    products_pagination = query.paginate(page=page, per_page=5, error_out=False)
    if form.validate_on_submit():
        if form.save.data:
            store = current_user.store
            discount = Discount.query.filter_by(code=form.discount_code.data).first()
            if form.image.data:
                picture_file = save_picture(form.image.data)
            else:
                picture_file = 'default.jpg'
            product = Product(name=form.name.data, description=form.description.data, image=picture_file,
                              buy_price=form.buy_price.data, sell_price=form.sell_price.data,
                              stock=form.stock.data, manufacturer=form.manufacturer.data,
                              type=form.type.data, model=form.model.data, is_active=True, is_deleted=False, store_id=store.id, discount_id=discount.id)
            try:
                db.session.add(product)
                db.session.commit()
                flash(f'Product "{product.name}" created successfully!', 'success')
                return redirect(url_for('users.home'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating the product.', 'danger')
                return render_template('owner/add_product.html', form=form)
        elif form.cancel.data:
            return render_template('owner/add_product.html', title='Add Product', form=form)
    return render_template('owner/add_product.html', title='Add Product', form=form, discounts=discounts, 
                           products=products_pagination.items,
                           pagination=products_pagination)

def list_products():
    page = request.args.get('page', 1, type=int)
    per_page = 9
    
    products_pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Enhance store data with product counts
    product_data = []
    for product in products_pagination.items:
        product_data.append({
            'name': product.name,
            'in_stock_quantity': product.stock,
            'description': product.description,
            'sell_price': product.sell_price,
            'type': product.type
        })

    return render_template('old/stores_list.html', 
                         products=product_data,
                         pagination=products_pagination)

@products.route('/product/<int:product_id>')
def view_product(product_id):
    """Display product details"""
    product = Product.query.get_or_404(product_id)
    store = Store.query.get_or_404(product.store_id)
    
    # Get Reviews for this product (Newest first)
    reviews = Review.query.filter_by(product_id=product_id)\
                          .order_by(Review.review_time.desc())\
                          .all()
    return render_template('common/product_detail.html', product=product, store=store, reviews=reviews)

@products.route('/product/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check ownership
    if current_user.store_id != product.store_id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('products.add_product'))
    
    # Soft delete
    product.soft_delete()
    db.session.commit()
    
    flash('Product deleted successfully', 'success')
    return redirect(url_for('products.add_product'))


@products.route('/search')
def search_results():
    query = request.args.get('q', '')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    sort_by = request.args.get('sort_by')

    # Base query
    products_query = Product.query

    # 1. Apply Search Term (Filter by name or description)
    if query:
        products_query = products_query.filter(Product.name.ilike(f'%{query}%'))

    # 2. Apply Price Filters
    if min_price:
        products_query = products_query.filter(Product.price >= float(min_price))
    if max_price:
        products_query = products_query.filter(Product.price <= float(max_price))

    # 3. Apply Sorting
    if sort_by == 'price_low':
        products_query = products_query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        products_query = products_query.order_by(Product.price.desc())
    elif sort_by == 'newest':
        products_query = products_query.order_by(Product.date_added.desc())

    # Execute query
    results = products_query.all()

    return render_template('common/search_results.html', products=results)

@products.route('/edit/<int:product_id>', methods=['POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check ownership
    if not current_user.o_flag or current_user.store_id != product.store_id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('users.home'))
    
    # Update fields
    product.name = request.form.get('name')
    product.type = request.form.get('type')
    product.description = request.form.get('description')
    product.buy_price = request.form.get('buy_price')
    product.sell_price = request.form.get('sell_price')
    product.stock = request.form.get('stock')
    product.manufacturer = request.form.get('manufacturer')
    product.model = request.form.get('model')
    
    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            # Save image logic here
            filename = save_picture(file)  # Your image saving function
            product.image = filename
    product.is_active = True
    product.is_deleted = False
    db.session.commit()
    flash('Product updated successfully!', 'success')
    return redirect(url_for('products.view_product', product_id=product.id))
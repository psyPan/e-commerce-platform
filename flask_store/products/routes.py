from ast import mod
from itertools import product
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flask_store import db
from flask_store.products.models import Product
from flask_store.discounts.models import Discount
from flask_store.products.forms import ProductForm
from flask_store.products.utils import save_picture

products = Blueprint('products', __name__)

@products.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.c_flag: # is customer
        flash('You do not have permission to this page', 'danger')
        return redirect(url_for('users.home'))
    form = ProductForm()
    discounts = Discount.query.all()
    form.discount_code.choices = [(d.code, d.code) for d in discounts]
     # Get page number and filters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'all')
    
    # Build query
    query = Product.query
    
    # Apply search filter
    if search_query:
        query = query.filter(Product.name.contains(search_query))
    
    # Apply category filter
    if filter_by == 'in_stock':
        query = query.filter(Product.stock > 0)
    elif filter_by == 'out_of_stock':
        query = query.filter(Product.stock == 0)
    elif filter_by == 'with_discount':
        query = query.filter(Product.discount_id != None)
    elif filter_by == 'no_discount':
        query = query.filter(Product.discount_id == None)
    
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
                              type=form.type.data, model=form.model.data, store_id=store.id, discount_id=discount.id)
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
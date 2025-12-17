from ast import mod
from itertools import product
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flask_store import db
from flask_store.products.models import Product
from flask_store.discounts.models import Discount
from flask_store.products.forms import ProductForm

products = Blueprint('products', __name__)

@products.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.c_flag: # is customer
        flash('You do not have permission to this page', 'danger')
        return redirect(url_for('users.home'))
    form = ProductForm()
    if form.validate_on_submit():
        if form.save.data:
            if form.discount_code.data:
                discount_code = form.discount_code.data.strip()
                if discount_code:
                    discount = Discount.query.filter_by(code=discount_code).first()
                    if not discount:
                        flash(f'Discount code "{discount_code}" not found!', 'danger')
                        return render_template('add_product.html', title='Add Product', form=form)
                store = current_user.store
                product = Product(name=form.name.data, description=form.description.data,
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
                    return render_template('add_product.html', form=form)
        elif form.cancel.data:
            return render_template('add_product.html', title='Add Product', form=form)
    return render_template('add_product.html', title='Add Product', form=form)
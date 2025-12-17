from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flask_store import db
from flask_store.cart.models import Cart

from flask_store.products.models import Product 


cart = Blueprint('cart', __name__)

@cart.route('/cart', methods=['GET', 'POST'])
@login_required
def My_cart(): # You can rename this to 'view_cart' for standard python naming convention
    
    # 1. Get the items
    Cart_items = db.session.query(Cart, Product)\
        .join(Product, Cart.product_id == Product.id)\
        .filter(Cart.user_id == current_user.id)\
        .all()

    # 2. Calculate Subtotal
    subtotal = 0
    for cart_item, product in Cart_items:
        subtotal += product.sell_price * cart_item.quantity

    # 3. Render
    return render_template('cart.html', 
                           title='My Cart', 
                           cart_items=Cart_items, 
                           subtotal=subtotal)

# flask_store/cart/routes.py

@cart.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # 1. Get the quantity from the form (default to 1 if missing)
    quantity = int(request.form.get('quantity', 1))
    
    # 2. Check if product exists and has stock
    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        flash(f'Not enough stock! Only {product.stock} left.', 'danger')
        return redirect(request.referrer)

    # 3. Check if user already has this item in cart
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        # Update existing item
        cart_item.quantity += quantity
        flash(f'Updated {product.name} quantity in cart.', 'info')
    else:
        # Create new item
        new_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)
        flash(f'Added {product.name} to cart!', 'success')

    db.session.commit()
    
    # Redirect back to the same page they were on
    return redirect(request.referrer)

@cart.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    # 1. Find the specific cart item for this user and product
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    # 2. If it exists, delete it
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from your cart.', 'success')
    else:
        flash('Item not found in your cart.', 'warning')
        
    # 3. Redirect back to the cart page
    return redirect(url_for('cart.My_cart'))
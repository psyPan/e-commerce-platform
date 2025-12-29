from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flask_store import db
from flask_store.cart.models import Cart
from flask_store.orders.models import Order 
from flask_store.line_items.models import LineItem 
from flask_store.products.models import Product 
from datetime import datetime, timedelta



cart = Blueprint('cart', __name__)

@cart.route('/my_cart', methods=['GET', 'POST'])
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
    return render_template('old/my_cart.html', 
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



@cart.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # 1. Fetch Cart Items & Products
    cart_items = db.session.query(Cart, Product)\
        .join(Product, Cart.product_id == Product.id)\
        .filter(Cart.user_id == current_user.id)\
        .all()

    if not cart_items:
        flash('Cart is empty', 'warning')
        return redirect(url_for('cart.My_cart'))

    # 2. Calculate Totals
    subtotal = sum(item.quantity * product.sell_price for item, product in cart_items)
    shipping_cost = 5
    grand_total = subtotal + shipping_cost

    if request.method == 'POST':
        # --- VALIDATION STEP 1: ADDRESS ---
        # We try to get address from form first, then fallback to user profile
        address = request.form.get('address')
        if not address:
             # If form is empty, check if the user model has one saved
            if current_user.address:
                address = current_user.address
            else:
                flash('Shipping address is required.', 'danger')
                return redirect(url_for('cart.checkout'))
        card_id = request.form.get('card_id') # <--- GET THE SELECTED ID

        if not card_id:
            flash('Please select a payment method', 'danger')
            return redirect(url_for('cart.checkout'))

        # --- VALIDATION STEP 2: STOCK CHECK (The "Look Before You Leap" Pattern) ---
        # Check ALL items before creating the order. 
        # If even one fails, we stop everything.
        for cart_row, product in cart_items:
            if product.stock < cart_row.quantity:
                flash(f'Sorry, {product.name} is out of stock (Only {product.stock} left).', 'danger')
                return redirect(url_for('cart.My_cart'))



    
        # --- PHASE 1: CREATE ORDER HEADER ---
        # Now we know we have the address AND the stock. Safe to create Order.
        new_order = Order(
            customer_id=current_user.id,
            total_amount=grand_total,
            shipping_cost=shipping_cost,
            cust_address=address,     
            credit_card_id=card_id, # Save the specific card
            status='received',       
            order_time=datetime.utcnow(), 
            estimated_delivery_date=datetime.utcnow().date() + timedelta(days=5),
            completion_time=None      
        )
        
        db.session.add(new_order)
        db.session.commit() # Commit to generate new_order.id

        # --- PHASE 2: MIGRATE ITEMS (Cart -> LineItem) ---
        try:
            for cart_row, product in cart_items:
                # A. Create the Permanent Record
                line_item = LineItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=cart_row.quantity,
                    total_price=product.sell_price * cart_row.quantity, # Snapshot price
                    type="cart"
                )
                
                # B. Deduct Stock
                product.stock -= cart_row.quantity

                # C. Clear the Temporary Cart
                db.session.add(line_item)
                db.session.delete(cart_row)

            # --- PHASE 3: FINAL COMMIT ---
            db.session.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('users.order_history'))

        except Exception as e:
            # SAFETY NET: If anything fails during migration, rollback everything
            db.session.rollback()
            flash(f'Error processing order: {str(e)}', 'danger')
            return redirect(url_for('cart.My_cart'))

    return render_template('old/checkout.html', cart_items=cart_items, grand_total=grand_total, shipping_cost=shipping_cost)
from datetime import datetime
from store import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'))
    phone = db.Column(db.String(10), nullable=False)
    birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    reg_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    a_flag = db.Column(db.Boolean, nullable=False, default=False)
    o_flag = db.Column(db.Boolean, nullable=False, default=False)
    c_flag = db.Column(db.Boolean, nullable=False, default=True)
    
    # Payment info
    card_no = db.Column(db.String(16))
    card_password = db.Column(db.String(60))
    card_date = db.Column(db.Date)

    def get_user_type(self):
        if self.a_flag:
            return "admin"
        elif self.o_flag:
            return "owner"
        else:
            return "customer"

    def __repr__(self):
        return f"User('{self.f_name} {self.l_name}', '{self.email}', '{self.get_user_type()}')"


class Store(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200))
    reg_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    balance = db.Column(db.Float, default=0.0)
    
    # Relationships
    owners = db.relationship('User', backref='owned_store', lazy=True, foreign_keys=[User.store_id])
    products = db.relationship('Product', backref='store', lazy=True)

    def __repr__(self):
        return f"Store('{self.name}')"


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.discount_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    discount = db.Column(db.Float, default=0.0)
    image = db.Column(db.String(200))
    discounted_price = db.Column(db.Float)
    sell_price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    manufacturer = db.Column(db.String(100))
    type = db.Column(db.String(50))
    model = db.Column(db.String(100))
    
    # Relationship
    discount_obj = db.relationship('Discount', backref='products')
    line_items = db.relationship('LineItem', backref='product', lazy=True)
    
    def get_final_price(self):
        """Calculate the final price considering discounts"""
        if self.discounted_price:
            return self.discounted_price
        elif self.discount > 0:
            return self.sell_price * (1 - self.discount / 100)
        return self.sell_price
    
    def is_in_stock(self):
        """Check if product is available"""
        return self.stock > 0
    
    def __repr__(self):
        return f"Product('{self.name}', ${self.sell_price})"


class Discount(db.Model):
    discount_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    discount_percent = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    code = db.Column(db.String(50), unique=True)
    
    def __repr__(self):
        return f"Discount('{self.name}', {self.discount_percent}%)"


class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_items = db.Column(db.Integer, default=0)
    total_price = db.Column(db.Float, default=0.0)
    checked_out = db.Column(db.Boolean, default=False)
    
    # Relationships
    customer = db.relationship('User', backref='carts')
    line_items = db.relationship('LineItem', backref='cart', lazy=True)
    
    def __repr__(self):
        return f"Cart({self.cart_id}, Items: {self.total_items})"


class LineItem(db.Model):
    line_item_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    type = db.Column(db.String(50))
    total_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"LineItem(Product: {self.product_id}, Qty: {self.quantity})"


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    ao_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin or Owner handling order
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.discount_id'))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'))
    status = db.Column(db.String(50), default='Pending')
    total_price = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, default=0.0)
    cust_address = db.Column(db.String(200), nullable=False)
    estimate_delivery_date = db.Column(db.Date)
    order_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completion_time = db.Column(db.DateTime)
    
    # Relationships
    customer = db.relationship('User', foreign_keys=[customer_id], backref='orders')
    handler = db.relationship('User', foreign_keys=[ao_id], backref='handled_orders')
    discount_applied = db.relationship('Discount', backref='orders')
    line_items = db.relationship('LineItem', backref='order', lazy=True)
    reviews = db.relationship('Review', backref='order', lazy=True)
    
    def __repr__(self):
        return f"Order({self.order_id}, Status: {self.status})"


class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    review_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='reviews')
    
    def __repr__(self):
        return f"Review({self.stars} stars by User {self.user_id})"


# Discount subtypes (optional - for more complex discount logic)
class SeasonalDiscount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    def is_active(self):
        today = datetime.utcnow().date()
        return self.start_date <= today <= self.end_date


class SpecialEventDiscount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    def is_active(self):
        today = datetime.utcnow().date()
        return self.start_date <= today <= self.end_date


class ShippingDiscount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    min_purchase = db.Column(db.Integer, nullable=False)
    
    def applies_to_order(self, order_total):
        return order_total >= self.min_purchase
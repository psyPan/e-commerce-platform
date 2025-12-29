from flask_store import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    
    # 1. Quantity of this specific product
    quantity = db.Column(db.Integer, default=1)
    
    # 2. Link to the User (Who owns this cart item?)
    # Note: Changed 'customer_id' to 'user_id' to match standard naming, 
    # but 'customer_id' is fine if you update your route query to match.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 3. Link to the Product (What is in the cart?)
    # THIS WAS MISSING in your code:
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    # Optional: Date added
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships (Optional but helpful)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('in_carts', lazy=True))
    orders = db.relationship('Order', back_populates='cart')
    line_items = db.relationship('LineItem', backref='cart', lazy=True)

    def __repr__(self):
        return f"Cart(User: {self.user_id}, Product: {self.product_id}, Qty: {self.quantity})"
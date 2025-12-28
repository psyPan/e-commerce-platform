from flask_store import db
from datetime import datetime
from sqlalchemy import event

class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('received', 'processed', 'shipped', 'closed'), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    shipping_cost = db.Column(db.Integer, nullable=False)
    cust_address = db.Column(db.String, nullable=False)
    estimated_delivery_date = db.Column(db.Date, nullable=False)
    order_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completion_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    # Foreign keys
    # Foreign key to the user (admin/owner who manages the order)
    order_manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Foreign key to the user (customer who places the order)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Foreign key to the discount (if shipping discount applied)
    shipping_discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'))
    # Foreign key to the cart
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    # Relationships
    # Relationship to discount
    shipping_discount = db.relationship('Discount', back_populates='orders')
    # Use order_manager_id to link to User table
    order_manager = db.relationship('User', foreign_keys=[order_manager_id])
    # Use customer_id to link to User table
    customer = db.relationship('User', foreign_keys=[customer_id])
    # Relationship to cart
    cart = db.relationship('Cart', back_populates='orders')
    items = db.relationship('LineItem', backref='order_details', lazy=True)

# Event listener to automatically update timestamps 
@event.listens_for(Order, 'before_update') 
def update_status_timestamp(mapper, connection, target): 
    if target.status == 'processed' and not target.processed_at: 
        target.processed_at = datetime.utcnow() 
    elif target.status == 'shipped' and not target.shipped_at: 
        target.shipped_at = datetime.utcnow() 
    elif target.status == 'closed' and not target.closed_at: 
        target.closed_at = datetime.utcnow()
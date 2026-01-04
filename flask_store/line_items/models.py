from flask_store import db

class LineItem(db.Model):
    __tablename__ = 'line_item'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    type =db.Column(db.Enum('cart', 'order', name='line_item_type'), nullable=False)
    total_price = db.Column(db.Float, nullable = False)

    # Foreign keys
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    # Relationships
    product = db.relationship('Product', back_populates='line_items')
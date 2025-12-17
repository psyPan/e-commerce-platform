from flask_store import db

# class LineItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quantity = db.Column(db.Integer, nullable=False)
#     type =db.Column(db.Enum('cart', 'order'), nullable=False)

#     # Foreign keys
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     # cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

#     # Relationships
#     product = db.relationship('Product', back_populates='line_items')
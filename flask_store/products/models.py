from datetime import datetime
from flask_store import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'))
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
    discount_obj = db.relationship('Discount', back_populates='products')
    #line_items = db.relationship('LineItem', backref='product', lazy=True)
    
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
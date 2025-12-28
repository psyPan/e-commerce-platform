# Add this to your imports in flask_store/models.py
from flask_store import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    review_time = db.Column(db.DateTime, nullable= False, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='reviews', lazy=True)
    product = db.relationship('Product', backref='reviews', lazy=True)
    order = db.relationship('Order', backref='reviews', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) # Added this!

    def __repr__(self):
        return f"Review('{self.stars}', '{self.review_time}')"
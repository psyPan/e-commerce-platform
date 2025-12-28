from datetime import datetime
from flask_store import db


class Store(db.Model):
    __tablename__ = 'store'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    reg_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    balance = db.Column(db.Integer)
    
    # Relationships
    # Relation ship to store owners
    owners = db.relationship('User', back_populates='store')
    # Relation ship to store products
    products = db.relationship('Product', back_populates='store')

    def __repr__(self):
        return f"Store('{self.name}')"
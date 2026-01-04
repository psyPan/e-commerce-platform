# flask_store/models.py

from flask_store import db
from datetime import datetime

class CreditCard(db.Model):  # Python classes standard is CapWords
    __tablename__ = 'credit_card' # Standard SQL is snake_case
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Ensure 'user.id' matches your User/Member table name exactly
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # CHANGED: Integer -> String(19) to handle 16 digits + potential spaces/dashes
    Card_Number = db.Column(db.String(20), nullable=False) 
    
    name = db.Column(db.String(100), nullable=False) # Name on card
    
    Expiration_Date = db.Column(db.Date, nullable=False)
    
    # CVV is definitely a string (e.g., "052")
    CVV = db.Column(db.String(4), nullable=False)
    
    is_active = db.Column(db.Boolean, default=True)

    # CHANGED: backref name to plural 'credit_cards'
    user = db.relationship('User', backref='credit_cards', lazy=True)

    def __repr__(self):
        return f"CreditCard('{self.Card_Number}', '{self.name}')"
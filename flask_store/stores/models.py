from datetime import datetime
from flask_store import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    reg_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    balance = db.Column(db.Integer)
    owners = db.relationship('User', backref='store', lazy=True)
    products = db.relationship('Product', backref='store', lazy=True)

    def __repr__(self):
        return f"Store('{self.name}')"
    


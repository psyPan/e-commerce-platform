from flask_store import db
from flask_store.orders.models import Order

class Discount(db.Model):
    __tablename__ = 'discount'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    discount_percent = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    code = db.Column(db.String(50), unique=True)
    type = db.Column(db.Enum('shipping', 'seasoning', 'special_event', name='discount_type_enum'), nullable=False)

    # Foreign Keys
    # admin/owner who creates the discount
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))

    # Relationships
    # Relationship to products
    products = db.relationship('Product', back_populates='discount_obj')
    # Relationship to orders (for shipping discounts)
    orders = db.relationship('Order', back_populates='shipping_discount')
    # Relationship to shipping details (one-to-one)
    shipping_details = db.relationship('Shipping', back_populates='discount', uselist=False)
    # Relationship to seasoning details (one-to-one)
    seasoning_details = db.relationship('Seasoning', back_populates='discount', uselist=False)
    # Relationship to special_event details (one-to-one)
    special_event_details = db.relationship('SpecialEvent', back_populates='discount', uselist=False)

    def __repr__(self):
        return f"Discount('{self.name}', '{self.code}', '{self.type}')"

class Shipping(db.Model):
    __tablename__ = 'shipping'

    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id', onupdate="CASCADE", ondelete="CASCADE"), 
                            primary_key=True, nullable=False)
    min_purchase = db.Column(db.Integer)

    # Relationships
    # Back reference to parent discount
    discount = db.relationship('Discount', back_populates='shipping_details')

class Seasoning(db.Model):
    __tablename__ = 'seasoning'
    
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id', onupdate="CASCADE", ondelete="CASCADE"), 
                            primary_key=True, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    __table_args__ = (db.CheckConstraint('end_date >= start_date', name='seasoning_valid_date_range'),)

    # Relationships
    # Back reference to parent discount
    discount = db.relationship('Discount', back_populates='seasoning_details')

class SpecialEvent(db.Model):
    __tablename__ = 'special_event'
    
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id', onupdate="CASCADE", ondelete="CASCADE"), 
                            primary_key=True, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    __table_args__ = (db.CheckConstraint('end_date >= start_date', name='special_event_valid_date_range'),)

    # Relationships
    # Back reference to parent discount
    discount = db.relationship('Discount', back_populates='special_event_details')
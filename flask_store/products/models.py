from flask_store import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    buy_price = db.Column(db.Integer, nullable=False)
    sell_price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    manufacturer = db.Column(db.String(100))
    type = db.Column(db.String(50))
    model = db.Column(db.String(100))

    # Foreign keys
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'))

    # Relationships
    # Relationship to discount
    discount_obj = db.relationship('Discount', back_populates='products')
    # Relationship to store
    store = db.relationship('Store', back_populates='products')
    # Relationship to line_item
    # line_items = db.relationship('LineItem', back_populates='product')
    
    def get_final_price(self):
        """Calculate the final price considering discounts"""
        if self.discount_obj and self.discount_obj.is_active:
            return self.sell_price * (1 - self.discount_obj.discount_percent)
        return self.sell_price
    
    def get_discount_percent(self):
        """Get the discount percentage if any"""
        if self.discount_obj and self.discount_obj.is_active:
            return self.discount_obj.discount_percent * 100  # Convert to percentage
        return 0
    
    def get_savings(self):
        """Calculate how much the customer saves"""
        if self.discount_obj and self.discount_obj.is_active:
            return self.sell_price * self.discount_obj.discount_percent
        return 0
    
    def is_in_stock(self):
        """Check if product is available"""
        return self.stock > 0
    
    def __repr__(self):
        return f"Product('{self.name}', ${self.sell_price})"
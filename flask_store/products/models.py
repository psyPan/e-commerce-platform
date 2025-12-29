from datetime import datetime
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
    line_items = db.relationship('LineItem', back_populates='product')

    def get_final_price(self):
        """Calculate the final price considering discounts"""
        # 1. Check if a discount object is attached
        if self.discount_obj:
            # OPTIONAL: Check if the discount is "active" (if your Discount model has an is_active field)
            if not self.discount_obj.is_active:
                return self.sell_price

            # 2. Get the percentage (assuming stored as decimal like 0.10 for 10%)
            # We use the relationship 'self.discount_obj' to get the data
            discount_percent = self.discount_obj.discount_percent
            
            # 3. Calculate final price
            discount_amount = self.sell_price * (discount_percent/100)
            return self.sell_price - discount_amount

        # If no discount, return normal price
        return self.sell_price
    
    def is_in_stock(self):
        """Check if product is available"""
        return self.stock > 0
    
    def get_product_discount(self):
        """Get discount only if it's NOT a shipping discount"""
        if self.discount_obj and self.discount_obj.is_active:
            if self.discount_obj.type != 'shipping':
                return self.discount_obj
        return None

    def get_discount_percent(self):
        """Get the discount percentage if any (excluding shipping)"""
        discount = self.get_product_discount()
        if discount:
            return discount.discount_percent
        return 0

    def __repr__(self):
        return f"Product('{self.name}', ${self.sell_price})"
from flask_store import db, create_app, bcrypt
from flask_store.stores.models import Store
from flask_store.products.models import Product

from flask_store.discounts.models import Discount
from flask_store.users.models import User
from datetime import date

app = create_app()

with app.app_context():
    # 1. Clear existing data to start fresh
    db.drop_all()
    db.create_all()

    # 2. Create a test Store
    store1 = Store(
        id = 20000009,
        name="Tech Haven", 
        email="contact@techhaven.com", 
        phone="1234567890", 
        reg_date = date(2025,12,13),
        balance=1000.0
    )

    db.session.add_all([store1])
    db.session.commit() # Commit to generate IDs

    owner = User(
        id = 12345678,
        f_name="John", 
        l_name="Doe", 
        email="owner@test.com", 
        password=bcrypt.generate_password_hash("OwnerPass").decode('utf-8'),
        store_id=store1.id,
        phone = 912345678,
        birth = date(2025,12,13),
        reg_date = date(2025,12,13),
        o_flag=True, 
        a_flag=False, 
        c_flag=False
    )
    db.session.add(owner)

    # 4. Create a Discount
    summer_sale = Discount(
        name="Summer Sale", 
        discount_percent=20.0, 
        code="SUMMER20",
        type='seasoning'
    )
    db.session.add(summer_sale)
    db.session.commit()

    # 5. Create some Products for Tech Haven
    p1 = Product(
        id = 44444444,
        store_id=store1.id,
        name="Gaming Laptop", 
        description="High performance laptop", 
        sell_price=1200.0, 
        stock=10, 
        manufacturer="Asus", 
        type="Electronics",
        discount_id=summer_sale.id
    )
    p2 = Product(
        id = 55555555,        
        store_id=store1.id,
        name="Wireless Mouse", 
        description="Ergonomic mouse", 
        sell_price=50.0, 
        stock=0, # Out of stock to test filter
        manufacturer="Logitech", 
        type="Electronics"
    )
    

    db.session.add_all([p1, p2])
    db.session.commit()

    print("Database seeded successfully!")
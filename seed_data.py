from flask_store import db, create_app, bcrypt
from flask_store.stores.models import Store
from flask_store.products.models import Product

from flask_store.discounts.models import Discount
from flask_store.products.models import Product
from flask_store.users.models import User
from flask_store.reviews.models import Review
from flask_store.orders.models import Order
from datetime import datetime, timedelta


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

    UserCust = User(
        id = 991234567,
        f_name="Abdulahad", 
        l_name="Aswat", 
        email="cust@test.com", 
        password=bcrypt.generate_password_hash("Password1").decode('utf-8'),
        phone = 912345678,
        birth = date(2000,12,13),
        reg_date = date(2025,12,13),
        o_flag=False, 
        a_flag=False, 
        c_flag=True
    )
    db.session.add(UserCust)

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
        buy_price=1000,
        sell_price=1200, 
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
        buy_price=30,
        sell_price=50.0, 
        stock=10, # Out of stock to test filter
        manufacturer="Logitech", 
        type="Electronics"
    )
    order1 = Order(
        id = 9990001,
        customer_id = UserCust.id,
        total_amount = 1205,
        shipping_cost = 5,
        cust_address = "123 Test St",
        status = 'closed',
        order_time = datetime.utcnow(),
        estimated_delivery_date = date(2025,12,20)
    )
    db.session.add(order1)
    db.session.commit()

    order2 = Order(
        id = 9990002,
        customer_id = UserCust.id,
        total_amount = 1205,
        shipping_cost = 5,
        cust_address = "123 Test St",
        status = 'closed',
        order_time = datetime.utcnow(),
        estimated_delivery_date = date(2025,12,20)
    )
    db.session.add(order2)
    db.session.commit()

    r1 = Review(
    id = 3030303,
    stars = 4,
    description = "Good product",
    review_time = datetime.utcnow(),
    user_id = UserCust.id,   # The customer who wrote it
    product_id = p1.id,      # The laptop
    order_id = order1.id
    )

    db.session.add(r1)
    db.session.commit()


    db.session.add_all([p1, p2])
    db.session.commit()

    print("Database seeded successfully!")
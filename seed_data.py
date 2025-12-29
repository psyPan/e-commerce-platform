from flask_store import db, create_app, bcrypt
from flask_store.stores.models import Store
from flask_store.products.models import Product
from flask_store.discounts.models import Discount, Seasoning, Shipping, SpecialEvent
from flask_store.products.models import Product
from flask_store.users.models import User
from flask_store.reviews.models import Review
from flask_store.orders.models import Order
from flask_store.cart.models import Cart
from datetime import datetime, timedelta


from datetime import date

app = create_app()

with app.app_context():
    # 1. Clear existing data to start fresh
    db.drop_all()
    db.create_all()

    # # 2. Create a test Store
    # store1 = Store(
    #     id = 20000009,
    #     name="Tech Haven", 
    #     email="contact@techhaven.com", 
    #     phone="1234567890", 
    #     reg_date = date(2025,12,13),
    #     balance=1000.0
    # )

    # db.session.add_all([store1])
    # db.session.commit() # Commit to generate IDs

    # owner = User(
    #     id = 12345678,
    #     f_name="John", 
    #     l_name="Doe", 
    #     email="owner@test.com", 
    #     password=bcrypt.generate_password_hash("OwnerPass").decode('utf-8'),
    #     store_id=store1.id,
    #     phone = 912345678,
    #     birth = date(2025,12,13),
    #     reg_date = date(2025,12,13),
    #     o_flag=True, 
    #     a_flag=False, 
    #     c_flag=False
    # )
    # db.session.add(owner)

    # UserCust = User(
    #     id = 991234567,
    #     f_name="Abdulahad", 
    #     l_name="Aswat", 
    #     email="cust@test.com", 
    #     password=bcrypt.generate_password_hash("Password1").decode('utf-8'),
    #     phone = 912345678,
    #     birth = date(2000,12,13),
    #     reg_date = date(2025,12,13),
    #     o_flag=False, 
    #     a_flag=False, 
    #     c_flag=True
    # )
    # db.session.add(UserCust)

    # # 4. Create a Discount
    # summer_sale = Discount(
    #     name="Summer Sale", 
    #     discount_percent=20.0, 
    #     code="SUMMER20",
    #     type='seasoning'
    # )
    # db.session.add(summer_sale)
    # db.session.commit()

    # # 5. Create some Products for Tech Haven
    # p1 = Product(
    #     id = 44444444,
    #     store_id=store1.id,
    #     name="Gaming Laptop", 
    #     description="High performance laptop",
    #     buy_price=1000,
    #     sell_price=1200, 
    #     stock=10, 
    #     manufacturer="Asus", 
    #     type="Electronics",
    #     discount_id=summer_sale.id
    # )
    # p2 = Product(
    #     id = 55555555,        
    #     store_id=store1.id,
    #     name="Wireless Mouse", 
    #     description="Ergonomic mouse",
    #     buy_price=30,
    #     sell_price=50.0, 
    #     stock=10, # Out of stock to test filter
    #     manufacturer="Logitech", 
    #     type="Electronics"
    # )
    # order1 = Order(
    #     id = 9990001,
    #     customer_id = UserCust.id,
    #     total_amount = 1205,
    #     shipping_cost = 5,
    #     cust_address = "123 Test St",
    #     status = 'closed',
    #     order_time = datetime.utcnow(),
    #     estimated_delivery_date = date(2025,12,20)
    # )
    # db.session.add(order1)
    # db.session.commit()

    # order2 = Order(
    #     id = 9990002,
    #     customer_id = UserCust.id,
    #     total_amount = 1205,
    #     shipping_cost = 5,
    #     cust_address = "123 Test St",
    #     status = 'closed',
    #     order_time = datetime.utcnow(),
    #     estimated_delivery_date = date(2025,12,20)
    # )
    # db.session.add(order2)
    # db.session.commit()

    # r1 = Review(
    # id = 3030303,
    # stars = 4,
    # description = "Good product",
    # review_time = datetime.utcnow(),
    # user_id = UserCust.id,   # The customer who wrote it
    # product_id = p1.id,      # The laptop
    # order_id = order1.id
    # )

    # db.session.add(r1)
    # db.session.commit()


    # db.session.add_all([p1, p2])
    # db.session.commit()

    print("Database seeded successfully!")

    admin = User(f_name='John', l_name='Doe', email='admin@email.com',
                 password=bcrypt.generate_password_hash('admin').decode('utf-8'),
                 phone='0911223344', birth=date(2000, 1, 1), address='taipei',
                 a_flag=True, o_flag=False, c_flag=False)
    db.session.add(admin)

    store1 = Store(name='Store1', email='store1@email.com', phone='0922334455', balance=0)
    store2 = Store(name='Store2', email='store2@email.com', phone='0922334456', balance=0)
    store3 = Store(name='Store3', email='store3@email.com', phone='0922334457', balance=0)
    store4 = Store(name='Store4', email='store4@email.com', phone='0922334458', balance=0)
    store5 = Store(name='Store5', email='store5@email.com', phone='0922334459', balance=0)
    db.session.add_all([store1, store2, store3, store4, store5])
    db.session.flush()

    owner1 = User(f_name='Barry', l_name='Allen', email='owner1@email.com',
                 password=bcrypt.generate_password_hash('owner1').decode('utf-8'),
                 phone='0911223345', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store1.id)
    owner2 = User(f_name='Bruce', l_name='Wayne', email='owner2@email.com',
                 password=bcrypt.generate_password_hash('owner2').decode('utf-8'),
                 phone='0911223346', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store1.id)
    owner3 = User(f_name='Bruce', l_name='Banner', email='owner3@email.com',
                 password=bcrypt.generate_password_hash('owner3').decode('utf-8'),
                 phone='0911223347', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store2.id)
    owner4 = User(f_name='Tony', l_name='Stark', email='owner4@email.com',
                 password=bcrypt.generate_password_hash('owner4').decode('utf-8'),
                 phone='0911223348', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store2.id)
    owner5 = User(f_name='Harry', l_name='Potter', email='owner5@email.com',
                 password=bcrypt.generate_password_hash('owner5').decode('utf-8'),
                 phone='0911223349', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store3.id)
    owner6 = User(f_name='Ronald', l_name='Wesley', email='owner6@email.com',
                 password=bcrypt.generate_password_hash('owner6').decode('utf-8'),
                 phone='0911223350', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store3.id)
    owner7 = User(f_name='Johnny', l_name='Depp', email='owner7@email.com',
                 password=bcrypt.generate_password_hash('owner7').decode('utf-8'),
                 phone='0911223351', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store4.id)
    owner8 = User(f_name='Justin', l_name='Bieber', email='owner8@email.com',
                 password=bcrypt.generate_password_hash('owner8').decode('utf-8'),
                 phone='0911223352', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store4.id)
    owner9 = User(f_name='John', l_name='Cena', email='owner9@email.com',
                 password=bcrypt.generate_password_hash('owner9').decode('utf-8'),
                 phone='0911223353', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store5.id)
    owner10 = User(f_name='Justin', l_name='Timberlake', email='owner10@email.com',
                 password=bcrypt.generate_password_hash('owner10').decode('utf-8'),
                 phone='0911223354', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store5.id)
    db.session.add_all([owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8, owner9, owner10])

    cust1 = User(f_name='Liam', l_name='Allen', email='cust1@email.com',
                 password=bcrypt.generate_password_hash('cust1').decode('utf-8'),
                 phone='0933445566', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust2 = User(f_name='Sophia', l_name='Rossi', email='cust2@email.com',
                 password=bcrypt.generate_password_hash('cust2').decode('utf-8'),
                 phone='0933445567', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust3 = User(f_name='Noah', l_name='Sato', email='cust4@email.com',
                 password=bcrypt.generate_password_hash('cust4').decode('utf-8'),
                 phone='0933445568', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust4 = User(f_name='Ava', l_name='Patel', email='cust5@email.com',
                 password=bcrypt.generate_password_hash('cust5').decode('utf-8'),
                 phone='0933445569', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust5 = User(f_name='Elijah', l_name='Bennett', email='cust6@email.com',
                 password=bcrypt.generate_password_hash('cust6').decode('utf-8'),
                 phone='0933445570', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust6 = User(f_name='Isabella', l_name='Morales', email='cust7@email.com',
                 password=bcrypt.generate_password_hash('cust7').decode('utf-8'),
                 phone='0933445571', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust7 = User(f_name='Jameson', l_name='Hughes', email='cust8@email.com',
                 password=bcrypt.generate_password_hash('cust8').decode('utf-8'),
                 phone='0933445572', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust8 = User(f_name='Mia', l_name='Chen', email='cust9@email.com',
                 password=bcrypt.generate_password_hash('cust9').decode('utf-8'),
                 phone='0933445573', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    db.session.add_all([cust1, cust2, cust3, cust4, cust5, cust6, cust7, cust8])
    db.session.flush()

    discount1 = Discount(
        name="Summer Sale", 
        discount_percent=20.0, 
        code="SUMMER20",
        type='seasoning'
    )

    discount2 = Discount(
        name="Winter Sale", 
        discount_percent=50.0, 
        code="WINTER50",
        type='seasoning'
    )

    discount3 = Discount(
        name="Black Friday", 
        discount_percent=65.0, 
        code="BLACKFRIDAY",
        type='special_event'
    )

    discount4 = Discount(
        name="New Year Super Save", 
        discount_percent=50.0, 
        code="NEWYEAR",
        type='special_event'
    )

    discount5 = Discount(
        name="Free 500", 
        discount_percent=100.0, 
        code="FREE500",
        type='shipping'
    )

    discount6 = Discount(
        name="Free 1000", 
        discount_percent=100.0, 
        code="FREE1000",
        type='shipping'
    )

    db.session.add_all([discount1, discount2, discount3, discount4, discount5, discount6])
    db.session.flush()

    seasoning1 = Seasoning(discount_id=discount1.id, end_date=date(2025, 4, 1),
                           start_date=date(2025, 3, 1))
    seasoning2 = Seasoning(discount_id=discount2.id, end_date=date(2025, 12, 30),
                           start_date=date(2025, 12, 1))
    special_event1 = SpecialEvent(discount_id=discount3.id, end_date=date(2025, 11, 30),
                                  start_date=date(2025, 11, 25))
    special_event2 = SpecialEvent(discount_id=discount4.id, end_date=date(2025, 12, 31),
                                  start_date=date(2025, 12, 31))
    shipping1 = Shipping(discount_id=discount5.id, min_purchase=500)
    shipping2 = Shipping(discount_id=discount6.id, min_purchase=1000)
    db.session.add_all([seasoning1, seasoning2, special_event1, special_event2, shipping1, shipping2])
    db.session.flush()

    product1 = Product(name="UltraBook Pro 15", description="High-performance laptop with 16GB RAM and 512GB SSD for professionals.",
                       buy_price=950, sell_price=1299, stock=25, manufacturer="TechStream",
                       type='laptop', model="TS-UB15-2024", store_id=store1.id)
    product2 = Product(name="NoiseCancel X Headphones", description="Wireless over-ear headphones with active noise cancellation and 30-hour battery life.",
                       buy_price=120, sell_price=299, stock=100, manufacturer="AudioWave",
                       type='Accessories', model="AW-NCX-01", store_id=store1.id)
    product3 = Product(name="Galaxy Vision 4K Monitor", description="27-inch IPS monitor with 144Hz refresh rate and 1ms response time.",
                       buy_price=220, sell_price=399, stock=60, manufacturer="VisualTech",
                       type='Electronics', model="VT-GV27-4K", store_id=store1.id)
    product4 = Product(name="UltraView 27-inch 4K Monitor", description="Professional IPS display with 100% sRGB color accuracy and ultra-thin bezels.",
                       buy_price=280, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store1.id)
    product5 = Product(name="GamerEdge 144Hz Curved Monitor", description="32-inch curved gaming monitor with 1ms response time and G-Sync compatibility.",
                       buy_price=210, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store1.id)
    product6 = Product(name="UltraBook Pro 15", description="High-performance laptop with 16GB RAM and 512GB SSD for professionals.",
                       buy_price=950, sell_price=1299, stock=25, manufacturer="TechStream",
                       type='laptop', model="TS-UB15-2024", store_id=store2.id)
    product7 = Product(name="NoiseCancel X Headphones", description="Wireless over-ear headphones with active noise cancellation and 30-hour battery life.",
                       buy_price=120, sell_price=299, stock=100, manufacturer="AudioWave",
                       type='Accessories', model="AW-NCX-01", store_id=store2.id)
    product8 = Product(name="Galaxy Vision 4K Monitor", description="27-inch IPS monitor with 144Hz refresh rate and 1ms response time.",
                       buy_price=220, sell_price=399, stock=60, manufacturer="VisualTech",
                       type='Electronics', model="VT-GV27-4K", store_id=store2.id)
    product9 = Product(name="UltraView 27-inch 4K Monitor", description="Professional IPS display with 100% sRGB color accuracy and ultra-thin bezels.",
                       buy_price=280, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store2.id)
    product10 = Product(name="GamerEdge 144Hz Curved Monitor", description="32-inch curved gaming monitor with 1ms response time and G-Sync compatibility.",
                       buy_price=210, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store2.id)
    product11 = Product(name="UltraBook Pro 15", description="High-performance laptop with 16GB RAM and 512GB SSD for professionals.",
                       buy_price=950, sell_price=1299, stock=25, manufacturer="TechStream",
                       type='laptop', model="TS-UB15-2024", store_id=store3.id)
    product12 = Product(name="NoiseCancel X Headphones", description="Wireless over-ear headphones with active noise cancellation and 30-hour battery life.",
                       buy_price=120, sell_price=299, stock=100, manufacturer="AudioWave",
                       type='Accessories', model="AW-NCX-01", store_id=store3.id)
    product13 = Product(name="Galaxy Vision 4K Monitor", description="27-inch IPS monitor with 144Hz refresh rate and 1ms response time.",
                       buy_price=220, sell_price=399, stock=60, manufacturer="VisualTech",
                       type='Electronics', model="VT-GV27-4K", store_id=store3.id)
    product14 = Product(name="UltraView 27-inch 4K Monitor", description="Professional IPS display with 100% sRGB color accuracy and ultra-thin bezels.",
                       buy_price=280, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store3.id)
    product15 = Product(name="GamerEdge 144Hz Curved Monitor", description="32-inch curved gaming monitor with 1ms response time and G-Sync compatibility.",
                       buy_price=210, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store3.id)
    product16 = Product(name="UltraBook Pro 15", description="High-performance laptop with 16GB RAM and 512GB SSD for professionals.",
                       buy_price=950, sell_price=1299, stock=25, manufacturer="TechStream",
                       type='laptop', model="TS-UB15-2024", store_id=store4.id)
    product17 = Product(name="NoiseCancel X Headphones", description="Wireless over-ear headphones with active noise cancellation and 30-hour battery life.",
                       buy_price=120, sell_price=299, stock=100, manufacturer="AudioWave",
                       type='Accessories', model="AW-NCX-01", store_id=store4.id)
    product18 = Product(name="Galaxy Vision 4K Monitor", description="27-inch IPS monitor with 144Hz refresh rate and 1ms response time.",
                       buy_price=220, sell_price=399, stock=60, manufacturer="VisualTech",
                       type='Electronics', model="VT-GV27-4K", store_id=store4.id)
    product19 = Product(name="UltraView 27-inch 4K Monitor", description="Professional IPS display with 100% sRGB color accuracy and ultra-thin bezels.",
                       buy_price=280, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store4.id)
    product20 = Product(name="GamerEdge 144Hz Curved Monitor", description="32-inch curved gaming monitor with 1ms response time and G-Sync compatibility.",
                       buy_price=210, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store4.id)
    product21 = Product(name="UltraBook Pro 15", description="High-performance laptop with 16GB RAM and 512GB SSD for professionals.",
                       buy_price=950, sell_price=1299, stock=25, manufacturer="TechStream",
                       type='laptop', model="TS-UB15-2024", store_id=store5.id)
    product22 = Product(name="NoiseCancel X Headphones", description="Wireless over-ear headphones with active noise cancellation and 30-hour battery life.",
                       buy_price=120, sell_price=299, stock=100, manufacturer="AudioWave",
                       type='Accessories', model="AW-NCX-01", store_id=store5.id)
    product23 = Product(name="Galaxy Vision 4K Monitor", description="27-inch IPS monitor with 144Hz refresh rate and 1ms response time.",
                       buy_price=220, sell_price=399, stock=60, manufacturer="VisualTech",
                       type='Electronics', model="VT-GV27-4K", store_id=store5.id)
    product24 = Product(name="UltraView 27-inch 4K Monitor", description="Professional IPS display with 100% sRGB color accuracy and ultra-thin bezels.",
                       buy_price=280, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store5.id)
    product25 = Product(name="GamerEdge 144Hz Curved Monitor", description="32-inch curved gaming monitor with 1ms response time and G-Sync compatibility.",
                       buy_price=210, sell_price=499, stock=45, manufacturer="ViewMaster",
                       type='Monitor', model="VM-27-Pro4K", store_id=store5.id)
    db.session.add_all([product1, product2, product3, product4, product5,
                        product6, product7, product8, product9, product10,
                        product11, product12, product13, product14, product15,
                        product16, product17, product18, product19, product20,
                        product21, product22, product23, product24, product25])
    
    cart1 = Cart(user_id=cust1.id)
    cart2 = Cart(user_id=cust2.id)
    cart3 = Cart(user_id=cust3.id)
    cart4 = Cart(user_id=cust4.id)
    cart5 = Cart(user_id=cust5.id)
    cart6 = Cart(user_id=cust6.id)
    cart7 = Cart(user_id=cust7.id)
    cart8 = Cart(user_id=cust8.id)
    db.session.add_all([cart1, cart2, cart3, cart4, cart5, cart6, cart7, cart8])
    db.session.commit()
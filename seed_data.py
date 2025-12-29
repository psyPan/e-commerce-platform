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

POSTGRES = {
   'user':'postgres',
   'password':'Keren_12345',
   'db':'mystore',
   'host':'localhost',
   'port':'5432',
}

app = create_app(POSTGRES)

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

    # print("Database seeded successfully!")

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

    # --- STORE 1 DISCOUNTS ---
    s1_d1 = Discount(name="Store 1 Welcome", discount_percent=10.0, code="S1WELCOME", type='seasoning', store_id=store1.id)
    s1_d2 = Discount(name="Tech Summer Sale", discount_percent=20.0, code="TECHSUMMER", type='seasoning', store_id=store1.id)
    s1_d3 = Discount(name="Winter Clearance", discount_percent=40.0, code="S1WINTER40", type='seasoning', store_id=store1.id)
    s1_d4 = Discount(name="Black Friday Tech", discount_percent=50.0, code="S1BF50", type='special_event', store_id=store1.id)
    s1_d5 = Discount(name="Cyber Monday", discount_percent=45.0, code="CYBERMON", type='special_event', store_id=store1.id)
    s1_d6 = Discount(name="Flash Sale", discount_percent=30.0, code="S1FLASH", type='special_event', store_id=store1.id)
    s1_d7 = Discount(name="Student Discount", discount_percent=15.0, code="S1EDU15", type='special_event', store_id=store1.id)
    s1_d8 = Discount(name="Free Shipping > 500", discount_percent=100.0, code="S1SHIP500", type='shipping', store_id=store1.id)
    s1_d9 = Discount(name="Free Shipping > 1000", discount_percent=100.0, code="S1SHIP1000", type='shipping', store_id=store1.id)
    s1_d10 = Discount(name="Member Exclusive", discount_percent=25.0, code="S1VIP25", type='seasoning', store_id=store1.id)
    
    db.session.add_all([s1_d1, s1_d2, s1_d3, s1_d4, s1_d5, s1_d6, s1_d7, s1_d8, s1_d9, s1_d10])

    # --- STORE 2 DISCOUNTS ---
    s2_d1 = Discount(name="Audio Spring Sale", discount_percent=15.0, code="AUDIOSPRING", type='seasoning', store_id=store2.id)
    s2_d2 = Discount(name="Fall Sound Event", discount_percent=20.0, code="SOUNDFALL", type='seasoning', store_id=store2.id)
    s2_d3 = Discount(name="New Year Vibes", discount_percent=30.0, code="S2NEWYEAR", type='seasoning', store_id=store2.id)
    s2_d4 = Discount(name="Music Day Special", discount_percent=25.0, code="MUSICDAY", type='special_event', store_id=store2.id)
    s2_d5 = Discount(name="Audiophile Week", discount_percent=35.0, code="AUDIO35", type='special_event', store_id=store2.id)
    s2_d6 = Discount(name="Weekend Jam", discount_percent=10.0, code="S2WEEKEND", type='special_event', store_id=store2.id)
    s2_d7 = Discount(name="Producer Bundle", discount_percent=18.0, code="PRODUCER18", type='special_event', store_id=store2.id)
    s2_d8 = Discount(name="Free Ship Audio", discount_percent=100.0, code="S2FREESHIP", type='shipping', store_id=store2.id)
    s2_d9 = Discount(name="Heavy Item Ship", discount_percent=100.0, code="S2HEAVY", type='shipping', store_id=store2.id)
    s2_d10 = Discount(name="Store 2 Launch", discount_percent=50.0, code="S2LAUNCH", type='special_event', store_id=store2.id)

    db.session.add_all([s2_d1, s2_d2, s2_d3, s2_d4, s2_d5, s2_d6, s2_d7, s2_d8, s2_d9, s2_d10])

    # --- STORE 3 DISCOUNTS ---
    s3_d1 = Discount(name="Smart Home Summer", discount_percent=20.0, code="SMARTSUMMER", type='seasoning', store_id=store3.id)
    s3_d2 = Discount(name="Cozy Winter", discount_percent=25.0, code="COZYWINTER", type='seasoning', store_id=store3.id)
    s3_d3 = Discount(name="Spring Cleaning", discount_percent=30.0, code="CLEAN30", type='seasoning', store_id=store3.id)
    s3_d4 = Discount(name="Earth Day Sale", discount_percent=22.0, code="EARTH22", type='special_event', store_id=store3.id)
    s3_d5 = Discount(name="Black Friday Home", discount_percent=55.0, code="S3BF55", type='special_event', store_id=store3.id)
    s3_d6 = Discount(name="Father's Day", discount_percent=15.0, code="S3DAD15", type='special_event', store_id=store3.id)
    s3_d7 = Discount(name="Mother's Day", discount_percent=15.0, code="S3MOM15", type='special_event', store_id=store3.id)
    s3_d8 = Discount(name="Free Ship Standard", discount_percent=100.0, code="S3SHIPSTD", type='shipping', store_id=store3.id)
    s3_d9 = Discount(name="Free Ship Express", discount_percent=100.0, code="S3SHIPEXP", type='shipping', store_id=store3.id)
    s3_d10 = Discount(name="IoT Bundle Deal", discount_percent=40.0, code="IOT40", type='special_event', store_id=store3.id)

    db.session.add_all([s3_d1, s3_d2, s3_d3, s3_d4, s3_d5, s3_d6, s3_d7, s3_d8, s3_d9, s3_d10])

    # --- STORE 4 DISCOUNTS ---
    s4_d1 = Discount(name="Photo Season Pass", discount_percent=12.0, code="PHOTO12", type='seasoning', store_id=store4.id)
    s4_d2 = Discount(name="Holiday Memories", discount_percent=20.0, code="MEMORIES20", type='seasoning', store_id=store4.id)
    s4_d3 = Discount(name="Travel Season", discount_percent=18.0, code="TRAVEL18", type='seasoning', store_id=store4.id)
    s4_d4 = Discount(name="World Photo Day", discount_percent=30.0, code="WPD30", type='special_event', store_id=store4.id)
    s4_d5 = Discount(name="Black Friday Cam", discount_percent=45.0, code="S4BF45", type='special_event', store_id=store4.id)
    s4_d6 = Discount(name="Creator Week", discount_percent=25.0, code="CREATOR25", type='special_event', store_id=store4.id)
    s4_d7 = Discount(name="Drone Day", discount_percent=20.0, code="DRONE20", type='special_event', store_id=store4.id)
    s4_d8 = Discount(name="Free Ship Lens", discount_percent=100.0, code="S4SHIPLENS", type='shipping', store_id=store4.id)
    s4_d9 = Discount(name="Free Ship Kit", discount_percent=100.0, code="S4SHIPKIT", type='shipping', store_id=store4.id)
    s4_d10 = Discount(name="Pro Member Deal", discount_percent=35.0, code="PRO35", type='seasoning', store_id=store4.id)

    db.session.add_all([s4_d1, s4_d2, s4_d3, s4_d4, s4_d5, s4_d6, s4_d7, s4_d8, s4_d9, s4_d10])

    # --- STORE 5 DISCOUNTS ---
    s5_d1 = Discount(name="Gaming Summer", discount_percent=20.0, code="GAMESUMMER", type='seasoning', store_id=store5.id)
    s5_d2 = Discount(name="Winter Grind", discount_percent=25.0, code="GRIND25", type='seasoning', store_id=store5.id)
    s5_d3 = Discount(name="Back to School", discount_percent=15.0, code="S5SCHOOL", type='seasoning', store_id=store5.id)
    s5_d4 = Discount(name="E3 Celebration", discount_percent=30.0, code="E3HYPE", type='special_event', store_id=store5.id)
    s5_d5 = Discount(name="Black Friday Gaming", discount_percent=60.0, code="S5BF60", type='special_event', store_id=store5.id)
    s5_d6 = Discount(name="Halloween Spook", discount_percent=33.0, code="SPOOKY33", type='special_event', store_id=store5.id)
    s5_d7 = Discount(name="Valentine's Duo", discount_percent=14.0, code="DUO14", type='special_event', store_id=store5.id)
    s5_d8 = Discount(name="Free Ship Console", discount_percent=100.0, code="S5SHIPCON", type='shipping', store_id=store5.id)
    s5_d9 = Discount(name="Free Ship Acc", discount_percent=100.0, code="S5SHIPACC", type='shipping', store_id=store5.id)
    s5_d10 = Discount(name="Level Up Sale", discount_percent=10.0, code="LEVELUP10", type='seasoning', store_id=store5.id)

    db.session.add_all([s5_d1, s5_d2, s5_d3, s5_d4, s5_d5, s5_d6, s5_d7, s5_d8, s5_d9, s5_d10])
    db.session.flush()

    # --- STORE 1 SUBCLASSES (Tech) ---
    # s1_d1: Welcome (Seasoning - All Year)
    s1_sub1 = Seasoning(discount_id=s1_d1.id, start_date=date(2025, 1, 1), end_date=date(2025, 12, 31))
    # s1_d2: Summer (Seasoning - June to Aug)
    s1_sub2 = Seasoning(discount_id=s1_d2.id, start_date=date(2025, 6, 1), end_date=date(2025, 8, 31))
    # s1_d3: Winter (Seasoning - Dec to Feb)
    s1_sub3 = Seasoning(discount_id=s1_d3.id, start_date=date(2025, 12, 1), end_date=date(2026, 2, 28))
    # s1_d4: Black Friday (SpecialEvent - Late Nov)
    s1_sub4 = SpecialEvent(discount_id=s1_d4.id, start_date=date(2025, 11, 25), end_date=date(2025, 11, 30))
    # s1_d5: Cyber Monday (SpecialEvent - Early Dec)
    s1_sub5 = SpecialEvent(discount_id=s1_d5.id, start_date=date(2025, 12, 1), end_date=date(2025, 12, 5))
    # s1_d6: Flash Sale (SpecialEvent - Short duration)
    s1_sub6 = SpecialEvent(discount_id=s1_d6.id, start_date=date(2025, 5, 10), end_date=date(2025, 5, 12))
    # s1_d7: Student (SpecialEvent - Back to School)
    s1_sub7 = SpecialEvent(discount_id=s1_d7.id, start_date=date(2025, 9, 1), end_date=date(2025, 9, 30))
    # s1_d8: Free Ship > 500 (Shipping)
    s1_sub8 = Shipping(discount_id=s1_d8.id, min_purchase=500)
    # s1_d9: Free Ship > 1000 (Shipping)
    s1_sub9 = Shipping(discount_id=s1_d9.id, min_purchase=1000)
    # s1_d10: Member Exclusive (Seasoning - All Year)
    s1_sub10 = Seasoning(discount_id=s1_d10.id, start_date=date(2025, 1, 1), end_date=date(2025, 12, 31))

    db.session.add_all([s1_sub1, s1_sub2, s1_sub3, s1_sub4, s1_sub5, s1_sub6, s1_sub7, s1_sub8, s1_sub9, s1_sub10])

    # --- STORE 2 SUBCLASSES (Audio) ---
    # s2_d1: Spring (Seasoning - Mar to May)
    s2_sub1 = Seasoning(discount_id=s2_d1.id, start_date=date(2025, 3, 1), end_date=date(2025, 5, 31))
    # s2_d2: Fall (Seasoning - Sept to Nov)
    s2_sub2 = Seasoning(discount_id=s2_d2.id, start_date=date(2025, 9, 1), end_date=date(2025, 11, 30))
    # s2_d3: New Year (Seasoning - Jan)
    s2_sub3 = Seasoning(discount_id=s2_d3.id, start_date=date(2025, 1, 1), end_date=date(2025, 1, 31))
    # s2_d4: Music Day (SpecialEvent - June 21)
    s2_sub4 = SpecialEvent(discount_id=s2_d4.id, start_date=date(2025, 6, 20), end_date=date(2025, 6, 22))
    # s2_d5: Audiophile Week (SpecialEvent)
    s2_sub5 = SpecialEvent(discount_id=s2_d5.id, start_date=date(2025, 4, 10), end_date=date(2025, 4, 17))
    # s2_d6: Weekend Jam (SpecialEvent)
    s2_sub6 = SpecialEvent(discount_id=s2_d6.id, start_date=date(2025, 7, 4), end_date=date(2025, 7, 6))
    # s2_d7: Producer Bundle (SpecialEvent)
    s2_sub7 = SpecialEvent(discount_id=s2_d7.id, start_date=date(2025, 10, 1), end_date=date(2025, 10, 15))
    # s2_d8: Free Ship Audio (Shipping)
    s2_sub8 = Shipping(discount_id=s2_d8.id, min_purchase=300)
    # s2_d9: Heavy Item Ship (Shipping)
    s2_sub9 = Shipping(discount_id=s2_d9.id, min_purchase=800)
    # s2_d10: Store Launch (SpecialEvent)
    s2_sub10 = SpecialEvent(discount_id=s2_d10.id, start_date=date(2025, 1, 1), end_date=date(2025, 1, 7))

    db.session.add_all([s2_sub1, s2_sub2, s2_sub3, s2_sub4, s2_sub5, s2_sub6, s2_sub7, s2_sub8, s2_sub9, s2_sub10])

    # --- STORE 3 SUBCLASSES (Smart Home) ---
    # s3_d1: Summer (Seasoning)
    s3_sub1 = Seasoning(discount_id=s3_d1.id, start_date=date(2025, 6, 1), end_date=date(2025, 8, 31))
    # s3_d2: Cozy Winter (Seasoning)
    s3_sub2 = Seasoning(discount_id=s3_d2.id, start_date=date(2025, 11, 1), end_date=date(2026, 2, 28))
    # s3_d3: Spring Cleaning (Seasoning)
    s3_sub3 = Seasoning(discount_id=s3_d3.id, start_date=date(2025, 3, 20), end_date=date(2025, 4, 20))
    # s3_d4: Earth Day (SpecialEvent - April 22)
    s3_sub4 = SpecialEvent(discount_id=s3_d4.id, start_date=date(2025, 4, 21), end_date=date(2025, 4, 23))
    # s3_d5: Black Friday (SpecialEvent)
    s3_sub5 = SpecialEvent(discount_id=s3_d5.id, start_date=date(2025, 11, 24), end_date=date(2025, 11, 29))
    # s3_d6: Father's Day (SpecialEvent - June)
    s3_sub6 = SpecialEvent(discount_id=s3_d6.id, start_date=date(2025, 6, 10), end_date=date(2025, 6, 16))
    # s3_d7: Mother's Day (SpecialEvent - May)
    s3_sub7 = SpecialEvent(discount_id=s3_d7.id, start_date=date(2025, 5, 5), end_date=date(2025, 5, 12))
    # s3_d8: Free Ship Std (Shipping)
    s3_sub8 = Shipping(discount_id=s3_d8.id, min_purchase=200)
    # s3_d9: Free Ship Exp (Shipping)
    s3_sub9 = Shipping(discount_id=s3_d9.id, min_purchase=600)
    # s3_d10: IoT Bundle (SpecialEvent)
    s3_sub10 = SpecialEvent(discount_id=s3_d10.id, start_date=date(2025, 8, 1), end_date=date(2025, 8, 15))

    db.session.add_all([s3_sub1, s3_sub2, s3_sub3, s3_sub4, s3_sub5, s3_sub6, s3_sub7, s3_sub8, s3_sub9, s3_sub10])

    # --- STORE 4 SUBCLASSES (Photography) ---
    # s4_d1: Season Pass (Seasoning)
    s4_sub1 = Seasoning(discount_id=s4_d1.id, start_date=date(2025, 1, 1), end_date=date(2025, 12, 31))
    # s4_d2: Holiday Memories (Seasoning - Dec)
    s4_sub2 = Seasoning(discount_id=s4_d2.id, start_date=date(2025, 12, 1), end_date=date(2025, 12, 31))
    # s4_d3: Travel Season (Seasoning - Summer)
    s4_sub3 = Seasoning(discount_id=s4_d3.id, start_date=date(2025, 5, 15), end_date=date(2025, 8, 15))
    # s4_d4: World Photo Day (SpecialEvent - Aug 19)
    s4_sub4 = SpecialEvent(discount_id=s4_d4.id, start_date=date(2025, 8, 18), end_date=date(2025, 8, 20))
    # s4_d5: Black Friday (SpecialEvent)
    s4_sub5 = SpecialEvent(discount_id=s4_d5.id, start_date=date(2025, 11, 26), end_date=date(2025, 11, 30))
    # s4_d6: Creator Week (SpecialEvent)
    s4_sub6 = SpecialEvent(discount_id=s4_d6.id, start_date=date(2025, 3, 1), end_date=date(2025, 3, 7))
    # s4_d7: Drone Day (SpecialEvent)
    s4_sub7 = SpecialEvent(discount_id=s4_d7.id, start_date=date(2025, 5, 5), end_date=date(2025, 5, 6))
    # s4_d8: Free Ship Lens (Shipping)
    s4_sub8 = Shipping(discount_id=s4_d8.id, min_purchase=250)
    # s4_d9: Free Ship Kit (Shipping)
    s4_sub9 = Shipping(discount_id=s4_d9.id, min_purchase=1000)
    # s4_d10: Pro Member (Seasoning)
    s4_sub10 = Seasoning(discount_id=s4_d10.id, start_date=date(2025, 1, 1), end_date=date(2025, 12, 31))

    db.session.add_all([s4_sub1, s4_sub2, s4_sub3, s4_sub4, s4_sub5, s4_sub6, s4_sub7, s4_sub8, s4_sub9, s4_sub10])

    # --- STORE 5 SUBCLASSES (Gaming) ---
    # s5_d1: Summer (Seasoning)
    s5_sub1 = Seasoning(discount_id=s5_d1.id, start_date=date(2025, 6, 1), end_date=date(2025, 8, 31))
    # s5_d2: Winter Grind (Seasoning)
    s5_sub2 = Seasoning(discount_id=s5_d2.id, start_date=date(2025, 12, 15), end_date=date(2026, 1, 15))
    # s5_d3: Back to School (Seasoning)
    s5_sub3 = Seasoning(discount_id=s5_d3.id, start_date=date(2025, 8, 20), end_date=date(2025, 9, 20))
    # s5_d4: E3 Hype (SpecialEvent - June)
    s5_sub4 = SpecialEvent(discount_id=s5_d4.id, start_date=date(2025, 6, 10), end_date=date(2025, 6, 15))
    # s5_d5: Black Friday (SpecialEvent)
    s5_sub5 = SpecialEvent(discount_id=s5_d5.id, start_date=date(2025, 11, 25), end_date=date(2025, 11, 30))
    # s5_d6: Halloween (SpecialEvent - Oct)
    s5_sub6 = SpecialEvent(discount_id=s5_d6.id, start_date=date(2025, 10, 25), end_date=date(2025, 10, 31))
    # s5_d7: Valentines (SpecialEvent - Feb)
    s5_sub7 = SpecialEvent(discount_id=s5_d7.id, start_date=date(2025, 2, 10), end_date=date(2025, 2, 15))
    # s5_d8: Free Ship Console (Shipping)
    s5_sub8 = Shipping(discount_id=s5_d8.id, min_purchase=400)
    # s5_d9: Free Ship Acc (Shipping)
    s5_sub9 = Shipping(discount_id=s5_d9.id, min_purchase=100)
    # s5_d10: Level Up (Seasoning - All year)
    s5_sub10 = Seasoning(discount_id=s5_d10.id, start_date=date(2025, 1, 1), end_date=date(2025, 12, 31))

    db.session.add_all([s5_sub1, s5_sub2, s5_sub3, s5_sub4, s5_sub5, s5_sub6, s5_sub7, s5_sub8, s5_sub9, s5_sub10])
    db.session.flush()

    # ... [Previous User/Admin/Store logic remains the same] ...
    # (Assuming admin, stores, owners, customers, and discounts are defined as above)

    # --- UNIQUE PRODUCT GENERATION ---

    # STORE 1: High-End Computing
    product1 = Product(name="Zenith X1 Carbon", description="Ultralight business laptop with carbon fiber chassis and AI-powered noise cancellation.",
                       buy_price=1100, sell_price=1450, stock=15, manufacturer="ZenithComp",
                       type='Laptop', model="ZC-X1-2024", store_id=store1.id, discount_id=s1_d2.id) # Tech Summer Sale
    product2 = Product(name="MechMaster Pro Keyboard", description="Wireless mechanical keyboard with hot-swappable switches and PBT keycaps.",
                       buy_price=80, sell_price=150, stock=50, manufacturer="KeyFlow",
                       type='Peripherals', model="KF-MM-PRO", store_id=store1.id, discount_id=s1_d1.id) # Welcome Discount
    product3 = Product(name="ErgoLift Vertical Mouse", description="Ergonomic vertical mouse designed to reduce wrist strain during long sessions.",
                       buy_price=40, sell_price=89, stock=30, manufacturer="ErgoTech",
                       type='Peripherals', model="ET-VM-02", store_id=store1.id, discount_id=s1_d10.id) # Member Exclusive
    product4 = Product(name="ThunderBolt Dock G4", description="12-in-1 docking station supporting dual 4K monitors and 100W PD charging.",
                       buy_price=150, sell_price=299, stock=20, manufacturer="LinkSys",
                       type='Accessories', model="LS-TB-G4", store_id=store1.id) # NO DISCOUNT
    product5 = Product(name="Portable SSD 2TB", description="Rugged external SSD with 1050MB/s read speeds, water and dust resistant.",
                       buy_price=110, sell_price=220, stock=40, manufacturer="DataSwift",
                       type='Storage', model="DS-Rugged-2T", store_id=store1.id, discount_id=s1_d8.id) # Free Shipping

    # STORE 2: Audio & Music
    product6 = Product(name="StudioRef 5 Monitors", description="Pair of near-field studio monitors with flat frequency response for mixing.",
                       buy_price=300, sell_price=499, stock=10, manufacturer="SoundWave",
                       type='Audio', model="SW-SR5-Pair", store_id=store2.id, discount_id=s2_d5.id) # Audiophile Week
    product7 = Product(name="Vinyl Classic Turntable", description="Belt-drive turntable with built-in preamp and USB output for digital archiving.",
                       buy_price=180, sell_price=279, stock=15, manufacturer="RetroSpin",
                       type='Audio', model="RS-VC-01", store_id=store2.id, discount_id=s2_d2.id) # Fall Sound Event
    product8 = Product(name="Podcaster USB Mic", description="Cardioid condenser microphone with integrated pop filter and shock mount.",
                       buy_price=90, sell_price=149, stock=35, manufacturer="VoiceClear",
                       type='Audio', model="VC-Pod-USB", store_id=store2.id, discount_id=s2_d4.id) # Music Day Special
    product9 = Product(name="BassBoom Bluetooth Speaker", description="Waterproof portable speaker with 24-hour battery life and 360-degree sound.",
                       buy_price=60, sell_price=119, stock=60, manufacturer="UrbanBeat",
                       type='Audio', model="UB-BB-360", store_id=store2.id, discount_id=s2_d8.id) # Free Shipping
    product10 = Product(name="NoiseGuard ANC Headphones", description="Premium over-ear headphones with industry-leading active noise cancellation.",
                       buy_price=200, sell_price=349, stock=25, manufacturer="SilenceTech",
                       type='Audio', model="ST-NG-ANC", store_id=store2.id) # NO DISCOUNT

    # STORE 3: Smart Home & IoT
    product11 = Product(name="SmartGuard Doorbell", description="1080p HD video doorbell with two-way talk and AI package detection.",
                       buy_price=100, sell_price=179, stock=40, manufacturer="SecureHome",
                       type='SmartHome', model="SH-DB-V2", store_id=store3.id, discount_id=s3_d5.id) # Black Friday Home
    product12 = Product(name="EcoThermostat Premium", description="Smart thermostat that learns your schedule and saves energy automatically.",
                       buy_price=140, sell_price=249, stock=30, manufacturer="EcoLive",
                       type='SmartHome', model="EL-TP-01", store_id=store3.id, discount_id=s3_d4.id) # Earth Day Sale
    product13 = Product(name="RoboClean S7", description="Robot vacuum and mop hybrid with LiDAR navigation and self-emptying base.",
                       buy_price=450, sell_price=799, stock=12, manufacturer="CleanBot",
                       type='Appliance', model="CB-S7-Plus", store_id=store3.id, discount_id=s3_d3.id) # Spring Cleaning
    product14 = Product(name="Luma Smart Bulb Kit", description="Pack of 4 color-changing LED bulbs compatible with Alexa and Google Home.",
                       buy_price=30, sell_price=69, stock=100, manufacturer="LumaLight",
                       type='SmartHome', model="LL-RGB-4PK", store_id=store3.id, discount_id=s3_d8.id) # Free Shipping
    product15 = Product(name="Smart Lock Touch", description="Fingerprint and keypad entry door lock with remote access via Wi-Fi bridge.",
                       buy_price=130, sell_price=229, stock=20, manufacturer="SecureHome",
                       type='SmartHome', model="SH-SL-Touch", store_id=store3.id) # NO DISCOUNT

    # STORE 4: Photography & Drones
    product16 = Product(name="SkyMaster Mini Drone", description="Sub-250g camera drone with 4K video, 30-min flight time, and obstacle avoidance.",
                       buy_price=350, sell_price=549, stock=18, manufacturer="SkyTech",
                       type='Drone', model="ST-Mini-3", store_id=store4.id, discount_id=s4_d7.id) # Drone Day
    product17 = Product(name="ProLens 50mm f/1.8", description="Prime portrait lens with fast aperture and silent autofocus motor.",
                       buy_price=150, sell_price=299, stock=22, manufacturer="OpticGlass",
                       type='CameraLens', model="OG-50-18", store_id=store4.id, discount_id=s4_d8.id) # Free Shipping
    product18 = Product(name="ActionCam Hero 5", description="Rugged waterproof action camera with HyperSmooth stabilization and 5.3K video.",
                       buy_price=280, sell_price=399, stock=30, manufacturer="AdventureCam",
                       type='Camera', model="AC-H5-Black", store_id=store4.id, discount_id=s4_d4.id) # World Photo Day
    product19 = Product(name="TravelTripod Carbon", description="Lightweight carbon fiber tripod with ball head, folds down to 15 inches.",
                       buy_price=90, sell_price=189, stock=25, manufacturer="SteadyShot",
                       type='Accessory', model="SS-TT-Carbon", store_id=store4.id) # NO DISCOUNT
    product20 = Product(name="Ring Light Studio 18", description="18-inch dimmable LED ring light with phone holder and tall stand for streaming.",
                       buy_price=45, sell_price=99, stock=45, manufacturer="GlowStream",
                       type='Lighting', model="GS-RL-18", store_id=store4.id, discount_id=s4_d6.id) # Creator Week

    # STORE 5: Gaming & Streaming
    product21 = Product(name="Console X Series", description="Next-gen gaming console capable of 4K 120FPS gaming with 1TB SSD.",
                       buy_price=450, sell_price=499, stock=5, manufacturer="GameBox",
                       type='Console', model="GB-XS-1TB", store_id=store5.id) # NO DISCOUNT (High Demand)
    product22 = Product(name="Handheld Deck 512", description="Portable PC gaming handheld with 7-inch touchscreen and custom APU.",
                       buy_price=550, sell_price=649, stock=8, manufacturer="ValveStream",
                       type='Console', model="VS-HD-512", store_id=store5.id, discount_id=s5_d8.id) # Free Shipping
    product23 = Product(name="StreamDeck Controller", description="15 LCD keys to trigger actions in apps and tools like OBS and Twitch.",
                       buy_price=90, sell_price=149, stock=25, manufacturer="StreamLive",
                       type='Accessory', model="SL-SD-MK2", store_id=store5.id, discount_id=s5_d4.id) # E3 Celebration
    product24 = Product(name="Racer Pro Gaming Chair", description="Ergonomic racing-style chair with lumbar support and 4D armrests.",
                       buy_price=180, sell_price=329, stock=15, manufacturer="SitZone",
                       type='Furniture', model="SZ-RP-Chair", store_id=store5.id, discount_id=s5_d1.id) # Gaming Summer
    product25 = Product(name="Curved Ultrawide 34", description="34-inch UWQHD gaming monitor with 165Hz refresh rate and 1ms response.",
                       buy_price=320, sell_price=599, stock=10, manufacturer="ViewMaster",
                       type='Monitor', model="VM-34-UW", store_id=store5.id, discount_id=s5_d5.id) # Black Friday Gaming

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
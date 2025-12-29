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

    # ... [Previous User/Admin/Store logic remains the same] ...
    # (Assuming admin, stores, owners, customers, and discounts are defined as above)

    # --- UNIQUE PRODUCT GENERATION ---

    # STORE 1: High-End Computing
    product1 = Product(name="Zenith X1 Carbon", description="Ultralight business laptop with carbon fiber chassis and AI-powered noise cancellation.",
                       buy_price=1100, sell_price=1450, stock=15, manufacturer="ZenithComp",
                       type='Laptop', model="ZC-X1-2024", store_id=store1.id)
    product2 = Product(name="MechMaster Pro Keyboard", description="Wireless mechanical keyboard with hot-swappable switches and PBT keycaps.",
                       buy_price=80, sell_price=150, stock=50, manufacturer="KeyFlow",
                       type='Peripherals', model="KF-MM-PRO", store_id=store1.id)
    product3 = Product(name="ErgoLift Vertical Mouse", description="Ergonomic vertical mouse designed to reduce wrist strain during long sessions.",
                       buy_price=40, sell_price=89, stock=30, manufacturer="ErgoTech",
                       type='Peripherals', model="ET-VM-02", store_id=store1.id)
    product4 = Product(name="ThunderBolt Dock G4", description="12-in-1 docking station supporting dual 4K monitors and 100W PD charging.",
                       buy_price=150, sell_price=299, stock=20, manufacturer="LinkSys",
                       type='Accessories', model="LS-TB-G4", store_id=store1.id)
    product5 = Product(name="Portable SSD 2TB", description="Rugged external SSD with 1050MB/s read speeds, water and dust resistant.",
                       buy_price=110, sell_price=220, stock=40, manufacturer="DataSwift",
                       type='Storage', model="DS-Rugged-2T", store_id=store1.id)

    # STORE 2: Audio & Music
    product6 = Product(name="StudioRef 5 Monitors", description="Pair of near-field studio monitors with flat frequency response for mixing.",
                       buy_price=300, sell_price=499, stock=10, manufacturer="SoundWave",
                       type='Audio', model="SW-SR5-Pair", store_id=store2.id)
    product7 = Product(name="Vinyl Classic Turntable", description="Belt-drive turntable with built-in preamp and USB output for digital archiving.",
                       buy_price=180, sell_price=279, stock=15, manufacturer="RetroSpin",
                       type='Audio', model="RS-VC-01", store_id=store2.id)
    product8 = Product(name="Podcaster USB Mic", description="Cardioid condenser microphone with integrated pop filter and shock mount.",
                       buy_price=90, sell_price=149, stock=35, manufacturer="VoiceClear",
                       type='Audio', model="VC-Pod-USB", store_id=store2.id)
    product9 = Product(name="BassBoom Bluetooth Speaker", description="Waterproof portable speaker with 24-hour battery life and 360-degree sound.",
                       buy_price=60, sell_price=119, stock=60, manufacturer="UrbanBeat",
                       type='Audio', model="UB-BB-360", store_id=store2.id)
    product10 = Product(name="NoiseGuard ANC Headphones", description="Premium over-ear headphones with industry-leading active noise cancellation.",
                       buy_price=200, sell_price=349, stock=25, manufacturer="SilenceTech",
                       type='Audio', model="ST-NG-ANC", store_id=store2.id)

    # STORE 3: Smart Home & IoT
    product11 = Product(name="SmartGuard Doorbell", description="1080p HD video doorbell with two-way talk and AI package detection.",
                       buy_price=100, sell_price=179, stock=40, manufacturer="SecureHome",
                       type='SmartHome', model="SH-DB-V2", is_active=True, is_deleted=False, store_id=store3.id)
    product12 = Product(name="EcoThermostat Premium", description="Smart thermostat that learns your schedule and saves energy automatically.",
                       buy_price=140, sell_price=249, stock=30, manufacturer="EcoLive",
                       type='SmartHome', model="EL-TP-01", is_active=True, is_deleted=False, store_id=store3.id)
    product13 = Product(name="RoboClean S7", description="Robot vacuum and mop hybrid with LiDAR navigation and self-emptying base.",
                       buy_price=450, sell_price=799, stock=12, manufacturer="CleanBot",
                       type='Appliance', model="CB-S7-Plus", is_active=True, is_deleted=False, store_id=store3.id)
    product14 = Product(name="Luma Smart Bulb Kit", description="Pack of 4 color-changing LED bulbs compatible with Alexa and Google Home.",
                       buy_price=30, sell_price=69, stock=100, manufacturer="LumaLight",
                       type='SmartHome', model="LL-RGB-4PK", is_active=True, is_deleted=False, store_id=store3.id)
    product15 = Product(name="Smart Lock Touch", description="Fingerprint and keypad entry door lock with remote access via Wi-Fi bridge.",
                       buy_price=130, sell_price=229, stock=20, manufacturer="SecureHome",
                       type='SmartHome', model="SH-SL-Touch", is_active=True, is_deleted=False, store_id=store3.id)

    # STORE 4: Photography & Drones
    product16 = Product(name="SkyMaster Mini Drone", description="Sub-250g camera drone with 4K video, 30-min flight time, and obstacle avoidance.",
                       buy_price=350, sell_price=549, stock=18, manufacturer="SkyTech",
                       type='Drone', model="ST-Mini-3", is_active=True, is_deleted=False, store_id=store4.id)
    product17 = Product(name="ProLens 50mm f/1.8", description="Prime portrait lens with fast aperture and silent autofocus motor.",
                       buy_price=150, sell_price=299, stock=22, manufacturer="OpticGlass",
                       type='CameraLens', model="OG-50-18", is_active=True, is_deleted=False, store_id=store4.id)
    product18 = Product(name="ActionCam Hero 5", description="Rugged waterproof action camera with HyperSmooth stabilization and 5.3K video.",
                       buy_price=280, sell_price=399, stock=30, manufacturer="AdventureCam",
                       type='Camera', model="AC-H5-Black", is_active=True, is_deleted=False, store_id=store4.id)
    product19 = Product(name="TravelTripod Carbon", description="Lightweight carbon fiber tripod with ball head, folds down to 15 inches.",
                       buy_price=90, sell_price=189, stock=25, manufacturer="SteadyShot",
                       type='Accessory', model="SS-TT-Carbon", is_active=True, is_deleted=False, store_id=store4.id)
    product20 = Product(name="Ring Light Studio 18", description="18-inch dimmable LED ring light with phone holder and tall stand for streaming.",
                       buy_price=45, sell_price=99, stock=45, manufacturer="GlowStream",
                       type='Lighting', model="GS-RL-18", is_active=True, is_deleted=False, store_id=store4.id)

    # STORE 5: Gaming & Streaming
    product21 = Product(name="Console X Series", description="Next-gen gaming console capable of 4K 120FPS gaming with 1TB SSD.",
                       buy_price=450, sell_price=499, stock=5, manufacturer="GameBox",
                       type='Console', model="GB-XS-1TB", is_active=True, is_deleted=False, store_id=store5.id)
    product22 = Product(name="Handheld Deck 512", description="Portable PC gaming handheld with 7-inch touchscreen and custom APU.",
                       buy_price=550, sell_price=649, stock=8, manufacturer="ValveStream",
                       type='Console', model="VS-HD-512", is_active=True, is_deleted=False, store_id=store5.id)
    product23 = Product(name="StreamDeck Controller", description="15 LCD keys to trigger actions in apps and tools like OBS and Twitch.",
                       buy_price=90, sell_price=149, stock=25, manufacturer="StreamLive",
                       type='Accessory', model="SL-SD-MK2", is_active=True, is_deleted=False, store_id=store5.id)
    product24 = Product(name="Racer Pro Gaming Chair", description="Ergonomic racing-style chair with lumbar support and 4D armrests.",
                       buy_price=180, sell_price=329, stock=15, manufacturer="SitZone",
                       type='Furniture', model="SZ-RP-Chair", is_active=True, is_deleted=False, store_id=store5.id)
    product25 = Product(name="Curved Ultrawide 34", description="34-inch UWQHD gaming monitor with 165Hz refresh rate and 1ms response.",
                       buy_price=320, sell_price=599, stock=10, manufacturer="ViewMaster",
                       type='Monitor', model="VM-34-UW", is_active=True, is_deleted=False, store_id=store5.id)

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
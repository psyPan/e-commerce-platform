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
   'password':'test',
   'db':'mystore',
   'host':'localhost',
   'port':'5432',
}

app = create_app(POSTGRES)

with app.app_context():
    # 1. Clear existing data to start fresh
    db.drop_all()
    db.create_all()

    admin = User(f_name='John', l_name='Doe', email='admin@email.com',
                 password=bcrypt.generate_password_hash('adminpass').decode('utf-8'),
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
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223345', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store1.id)
    owner2 = User(f_name='Bruce', l_name='Wayne', email='owner2@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223346', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store1.id)
    owner3 = User(f_name='Bruce', l_name='Banner', email='owner3@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223347', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store2.id)
    owner4 = User(f_name='Tony', l_name='Stark', email='owner4@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223348', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store2.id)
    owner5 = User(f_name='Harry', l_name='Potter', email='owner5@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223349', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store3.id)
    owner6 = User(f_name='Ronald', l_name='Wesley', email='owner6@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223350', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store3.id)
    owner7 = User(f_name='Johnny', l_name='Depp', email='owner7@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223351', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store4.id)
    owner8 = User(f_name='Justin', l_name='Bieber', email='owner8@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223352', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store4.id)
    owner9 = User(f_name='John', l_name='Cena', email='owner9@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223353', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store5.id)
    owner10 = User(f_name='Justin', l_name='Timberlake', email='owner10@email.com',
                 password=bcrypt.generate_password_hash('ownerpass').decode('utf-8'),
                 phone='0911223354', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=True, c_flag=False, store_id=store5.id)
    db.session.add_all([owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8, owner9, owner10])

    cust1 = User(f_name='Liam', l_name='Allen', email='cust1@email.com',
                 password=bcrypt.generate_password_hash('customerpass').decode('utf-8'),
                 phone='0933445566', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust2 = User(f_name='Sophia', l_name='Rossi', email='cust2@email.com',
                 password=bcrypt.generate_password_hash('customerpass').decode('utf-8'),
                 phone='0933445567', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust3 = User(f_name='Noah', l_name='Sato', email='cust3@email.com',
                 password=bcrypt.generate_password_hash('customerpass').decode('utf-8'),
                 phone='0933445568', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust4 = User(f_name='Ava', l_name='Patel', email='cust4@email.com',
                 password=bcrypt.generate_password_hash('customerpass').decode('utf-8'),
                 phone='0933445569', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust5 = User(f_name='Elijah', l_name='Bennett', email='cust5@email.com',
                 password=bcrypt.generate_password_hash('customerpass').decode('utf-8'),
                 phone='0933445570', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust6 = User(f_name='Isabella', l_name='Morales', email='cust6@email.com',
                 password=bcrypt.generate_password_hash('customerpass').decode('utf-8'),
                 phone='0933445571', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust7 = User(f_name='Jameson', l_name='Hughes', email='cust7@email.com',
                 password=bcrypt.generate_password_hash('customerpass').decode('utf-8'),
                 phone='0933445572', birth=date(2000, 1, 1), address='taipei',
                 a_flag=False, o_flag=False, c_flag=True)
    cust8 = User(f_name='Mia', l_name='Chen', email='cust8@email.com',
                 password=bcrypt.generate_password_hash('customerpass').decode('utf-8'),
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

    # STORE 1: 5 Laptops
    product1 = Product(name="Dell XPS 15", description="15.6-inch premium laptop with Intel i7, 16GB RAM, 512GB SSD, and stunning 4K OLED display.",
                    buy_price=1200, sell_price=1599, stock=12, manufacturer="Dell", image='product1.webp',
                    type='Laptop', model="XPS-15-9520", store_id=store1.id, discount_id=s1_d2.id) # Tech Summer Sale

    product2 = Product(name="MacBook Air M2", description="Lightweight 13-inch laptop with Apple M2 chip, 8GB RAM, 256GB SSD, all-day battery life.",
                    buy_price=900, sell_price=1199, stock=20, manufacturer="Apple", image='product2.webp',
                    type='Laptop', model="MBA-M2-2024", store_id=store1.id, discount_id=s1_d1.id) # Welcome Discount

    product3 = Product(name="ASUS ROG Strix G16", description="Gaming powerhouse with RTX 4060, Intel i7-13650HX, 16GB DDR5 RAM, 1TB SSD, 165Hz display.",
                    buy_price=1300, sell_price=1799, stock=8, manufacturer="ASUS", image='product3.webp',
                    type='Laptop', model="G16-G614JV", store_id=store1.id, discount_id=s1_d10.id) # Member Exclusive

    product4 = Product(name="HP Pavilion 14", description="Budget-friendly 14-inch laptop with AMD Ryzen 5, 8GB RAM, 512GB SSD, perfect for students.",
                    buy_price=450, sell_price=699, stock=25, manufacturer="HP", image='product4.webp',
                    type='Laptop', model="PAV-14-EK1023", store_id=store1.id) # NO DISCOUNT

    product5 = Product(name="Lenovo ThinkPad X1 Carbon", description="Business-class ultrabook with Intel i5, 16GB RAM, 512GB SSD, military-grade durability.",
                    buy_price=1100, sell_price=1499, stock=15, manufacturer="Lenovo", image='product5.webp',
                    type='Laptop', model="X1C-Gen11", store_id=store1.id, discount_id=s1_d8.id) # Free Shipping

    # STORE 2: 5 Headphones
    product6 = Product(name="Sony WH-1000XM5", description="Industry-leading noise cancelling wireless headphones with 30-hour battery and premium sound.",
                    buy_price=280, sell_price=399, stock=18, manufacturer="Sony", image='product6.webp',
                    type='Headphones', model="WH-1000XM5", store_id=store2.id, discount_id=s2_d5.id) # Audiophile Week

    product7 = Product(name="Bose QuietComfort 45", description="Legendary comfort with world-class noise cancellation and balanced audio performance.",
                    buy_price=250, sell_price=329, stock=22, manufacturer="Bose", image='product7.webp',
                    type='Headphones', model="QC45", store_id=store2.id, discount_id=s2_d2.id) # Fall Sound Event

    product8 = Product(name="Apple AirPods Max", description="Premium over-ear headphones with spatial audio, transparency mode, and seamless Apple integration.",
                    buy_price=400, sell_price=549, stock=12, manufacturer="Apple", image='product8.webp',
                    type='Headphones', model="APM-2024", store_id=store2.id, discount_id=s2_d4.id) # Music Day Special

    product9 = Product(name="Sennheiser HD 660S2", description="Open-back audiophile headphones with natural sound reproduction for critical listening.",
                    buy_price=350, sell_price=499, stock=15, manufacturer="Sennheiser", image='product9.webp',
                    type='Headphones', model="HD660S2", store_id=store2.id, discount_id=s2_d8.id) # Free Shipping

    product10 = Product(name="Beats Studio Pro", description="Stylish wireless headphones with powerful bass, ANC, and up to 40 hours of battery life.",
                    buy_price=200, sell_price=349, stock=30, manufacturer="Beats", image='product10.webp',
                    type='Headphones', model="BSP-2024", store_id=store2.id) # NO DISCOUNT

    # STORE 3: 5 Cameras
    product11 = Product(name="Canon EOS R6 Mark II", description="Full-frame mirrorless camera with 24.2MP sensor, 40fps burst, and advanced autofocus.",
                    buy_price=1800, sell_price=2499, stock=10, manufacturer="Canon", image='product11.webp',
                    type='Camera', model="EOS-R6-II", store_id=store3.id, discount_id=s3_d5.id) # Black Friday Home

    product12 = Product(name="Sony A7 IV", description="Versatile hybrid camera with 33MP sensor, 4K 60p video, and exceptional low-light performance.",
                    buy_price=1900, sell_price=2599, stock=8, manufacturer="Sony", image='product12.webp',
                    type='Camera', model="ILCE-7M4", store_id=store3.id, discount_id=s3_d4.id) # Earth Day Sale

    product13 = Product(name="Fujifilm X-T5", description="Retro-styled APS-C camera with 40MP sensor, in-body stabilization, and film simulations.",
                    buy_price=1200, sell_price=1699, stock=15, manufacturer="Fujifilm", image='product13.webp',
                    type='Camera', model="X-T5", store_id=store3.id, discount_id=s3_d3.id) # Spring Cleaning

    product14 = Product(name="Nikon Z6 III", description="Hybrid shooter with 24MP sensor, partially stacked sensor for fast readout, and N-RAW video.",
                    buy_price=1700, sell_price=2399, stock=12, manufacturer="Nikon", image='product14.webp',
                    type='Camera', model="Z6-III", store_id=store3.id, discount_id=s3_d8.id) # Free Shipping

    product15 = Product(name="Panasonic Lumix S5 II", description="Compact full-frame camera with phase-detect AF, 6K video, and weather-sealed body.",
                    buy_price=1500, sell_price=1999, stock=18, manufacturer="Panasonic", image='product15.webp',
                    type='Camera', model="DC-S5M2", store_id=store3.id) # NO DISCOUNT

    # STORE 4: 5 Monitors
    product16 = Product(name="Dell UltraSharp U2723DE", description="27-inch QHD IPS monitor with USB-C hub, 99% sRGB coverage, and height-adjustable stand.",
                    buy_price=350, sell_price=549, stock=20, manufacturer="Dell", image='product16.webp',
                    type='Monitor', model="U2723DE", store_id=store4.id, discount_id=s4_d7.id) # Drone Day

    product17 = Product(name="LG 27GN950-B", description="27-inch 4K gaming monitor with 144Hz, Nano IPS, 1ms response time, and G-Sync compatible.",
                    buy_price=500, sell_price=799, stock=15, manufacturer="LG", image='product17.webp',
                    type='Monitor', model="27GN950-B", store_id=store4.id, discount_id=s4_d8.id) # Free Shipping

    product18 = Product(name="ASUS ProArt PA278CV", description="27-inch color-accurate monitor with 100% sRGB/Rec.709, factory calibrated for creators.",
                    buy_price=250, sell_price=399, stock=25, manufacturer="ASUS", image='product18.webp',
                    type='Monitor', model="PA278CV", store_id=store4.id, discount_id=s4_d4.id) # World Photo Day

    product19 = Product(name="Samsung Odyssey G7", description="32-inch curved QHD gaming monitor with 240Hz, 1ms, HDR600, and aggressive 1000R curvature.",
                    buy_price=450, sell_price=699, stock=12, manufacturer="Samsung", image='product19.webp',
                    type='Monitor', model="G7-C32G75T", store_id=store4.id) # NO DISCOUNT

    product20 = Product(name="BenQ SW270C", description="27-inch PhotoVue monitor with hardware calibration, 99% Adobe RGB, and shading hood included.",
                    buy_price=400, sell_price=649, stock=18, manufacturer="BenQ", image='product20.webp',
                    type='Monitor', model="SW270C", store_id=store4.id, discount_id=s4_d6.id) # Creator Week

    # STORE 5: 5 Fancy Keyboards
    product21 = Product(name="Keychron Q6 Pro", description="Full-size wireless mechanical keyboard with gasket mount, hot-swappable switches, and QMK/VIA support.",
                    buy_price=150, sell_price=229, stock=20, manufacturer="Keychron", image='product21.webp',
                    type='Keyboard', model="Q6-Pro", store_id=store5.id) # NO DISCOUNT (High Demand)

    product22 = Product(name="Logitech G915 TKL", description="Low-profile wireless gaming keyboard with GL mechanical switches, LIGHTSYNC RGB, and 40-hour battery.",
                    buy_price=180, sell_price=279, stock=15, manufacturer="Logitech", image='product22.webp',
                    type='Keyboard', model="G915-TKL", store_id=store5.id, discount_id=s5_d8.id) # Free Shipping

    product23 = Product(name="Razer BlackWidow V4 Pro", description="Premium gaming keyboard with analog optical switches, command dial, and per-key Chroma RGB.",
                    buy_price=200, sell_price=299, stock=18, manufacturer="Razer", image='product23.webp',
                    type='Keyboard', model="BWV4-Pro", store_id=store5.id, discount_id=s5_d4.id) # E3 Celebration

    product24 = Product(name="Corsair K100 RGB", description="Flagship keyboard with Cherry MX Speed switches, iCUE control wheel, and PBT double-shot keycaps.",
                    buy_price=190, sell_price=279, stock=12, manufacturer="Corsair", image='product24.webp',
                    type='Keyboard', model="K100-RGB", store_id=store5.id, discount_id=s5_d1.id) # Gaming Summer

    product25 = Product(name="SteelSeries Apex Pro TKL", description="Esports-grade TKL keyboard with adjustable OmniPoint switches, OLED display, and aircraft-grade aluminum.",
                    buy_price=160, sell_price=249, stock=22, manufacturer="SteelSeries", image='product25.webp',
                    type='Keyboard', model="Apex-Pro-TKL", store_id=store5.id, discount_id=s5_d5.id) # Black Friday Gaming

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
    print("Database Created!")
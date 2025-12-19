from flask_store import db, create_app, bcrypt
from flask_store.stores.models import Store
from flask_store.products.models import Product

from flask_store.discounts.models import Discount
from flask_store.products.models import Product
from flask_store.users.models import User
from datetime import date

app = create_app()

with app.app_context():
    db.create_all()
    # 4. Create a Discount
    winter_sale = Discount(
        name="Winter Sale", 
        discount_percent=50.0, 
        code="WINTER50",
        type='seasoning'
    )
    db.session.add(winter_sale)
    db.session.commit()

    discounts = Discount.query.all()
    for discount in discounts:
        print(f'{discount.id}, {discount.code}')
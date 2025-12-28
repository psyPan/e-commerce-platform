from flask_store import create_app
from flask_store.products.models import Product

POSTGRES = {
   'user': 'postgres',
   'password': 'Keren_12345',
   'db': 'mystore',
   'host': 'localhost',
   'port': '5432',
}

app = create_app(POSTGRES)

with app.app_context():
    print(Product.query.limit(5).all())

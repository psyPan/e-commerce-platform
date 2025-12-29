from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'  # Redirect to login page if not authenticated
login_manager.login_message_category = 'info'  # Flash message category

# def create_app():
def create_app(postgres):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'YourSecretKey'  # Change this in production!
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{postgres['user']}:{postgres['password']}"
        f"@{postgres['host']}:{postgres['port']}/{postgres['db']}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        from flask_store.users.routes import users
        from flask_store.stores.routes import stores
        from flask_store.discounts.routes import discounts
        from flask_store.products.routes import products
        from flask_store.cart.routes import cart
        #from flask_store.reviews.models import reviews

        # db.create_all()
        
        # Register blueprints
        app.register_blueprint(users)
        app.register_blueprint(stores)
        app.register_blueprint(discounts)
        #app.register_blueprint(reviews)

        app.register_blueprint(cart)
        app.register_blueprint(products)
    return app
from datetime import datetime
from flask_store import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): # We need UserMixin for handling user's logged in sessions
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    reg_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    a_flag = db.Column(db.Boolean, nullable=False)
    o_flag = db.Column(db.Boolean, nullable=False)
    c_flag = db.Column(db.Boolean, nullable=False)

    # Foreign keys
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=True)

    # Relationships
    # Relationship with store
    store = db.relationship('Store', back_populates='owners')

    def get_user_type(self):
        if self.a_flag:
            return "admin"
        elif self.o_flag:
            return "owner"
        else:
            return "customer"

    def __repr__(self):
        return f"User('{self.f_name}' '{self.l_name}', '{self.email}', '{self.get_user_type()}')"
from store import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20), unique=True, nullable=False)
    l_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    phone = db.Column(db.String(10), nullable=False)
    birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    reg_date = db.Column(db.Date, nullable=False)
    a_flag = db.Column(db.Boolean, nullable=False)
    o_flag = db.Column(db.Boolean, nullable=False)
    c_flag = db.Column(db.Boolean, nullable=False)

    def get_user_type(self):
        if self.a_flag:
            return "admin"
        elif self.o_flag:
            return "owner"
        else:
            return "customer"

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.get_user_type()}')"
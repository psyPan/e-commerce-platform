from flask_store import create_app, db, bcrypt
from flask_store.users.models import User

# =========================
# POSTGRES CONFIG
# =========================
POSTGRES = {
    'user': 'postgres',
    'password': 'Keren_12345',        # sesuaikan
    'db': 'mystore',
    'host': 'localhost',
    'port': '5432',
}

app = create_app(POSTGRES)

# =========================
# PASSWORD MAPPING
# =========================
PASSWORD_MAP = {
    'admin@ecommerce.com': 'admin123',
    'owner1@electromart.com': 'ownerone123',
    'owner2@electromart.com': 'ownertwo123',
    'owner3@gadgetworld.com': 'owner12345',
    'customer1@gmail.com': 'custone123',
    'customer2@gmail.com': 'custtwo123',
}

# =========================
# UPDATE PASSWORDS
# =========================
with app.app_context():
    for email, plain_password in PASSWORD_MAP.items():
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = bcrypt.generate_password_hash(
                plain_password
            ).decode('utf-8')
            print(f"[OK] Password updated for {email}")
        else:
            print(f"[SKIP] User not found: {email}")

    db.session.commit()
    print("=== ALL USER PASSWORDS UPDATED ===")

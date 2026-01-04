# E-Commerce Platform

A full-featured e-commerce web application built with Flask and PostgreSQL.

## Features

- User authentication (Admin, Store Owner, Customer roles)
- Multiple stores with independent inventories
- Product management with images
- Shopping cart functionality
- Discount system (Seasonal, Special Event, Shipping discounts)
- Order processing
- Product reviews
- Search and filtering

## Tech Stack

- **Backend:** Flask 3.1.2
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login, Flask-Bcrypt
- **Forms:** Flask-WTF, WTForms
- **Frontend:** HTML, CSS, Jinja2 templates

## Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running
- pgAdmin 4 (recommended for database management)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/psyPan/e-commerce-platform.git
cd e-commerce-platform
```

### 2. Create Virtual Environment
- On Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

- On Window
```bash
python3 -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

1. Open pgAdmin 4
2. Create a new database:
   - Right-click on "Databases" → "Create" → "Database"
   - Database name: `mystore`
   - Click "Save"

### 5. Configure Database Connection

Edit the `POSTGRES` dictionary in both `seed_data.py` and `run.py` with your PostgreSQL credentials:

```python
POSTGRES = {
   'user': 'postgres',        # Your PostgreSQL username
   'password': 'your_password',  # Your PostgreSQL password
   'db': 'mystore',
   'host': 'localhost',
   'port': '5432',
}
```

### 6. Initialize Database

Run the seed script to create tables and populate with sample data:

```bash
python3 seed_data.py
```

This will create:
- 1 Admin account
- 5 Stores with 2 owners each
- 8 Customer accounts
- 25 Products (5 per store)
- 50 Discount codes
- Shopping carts for all customers

## Running the Application

Start the Flask development server:

```bash
python3 run.py
```

The application will be available at: `http://127.0.0.1:5000`

## Sample Login Credentials

### Admin Account
- Email: `admin@email.com`
- Password: `adminpass`

### Store Owner Accounts
- Email: `owner1@email.com` to `owner10@email.com`
- Password: `ownerpass`

### Customer Accounts
- Email: `cust1@email.com` to `cust8@email.com`
- Password: `customerpass`

## Store Categories

- **Store 1:** Laptops (Dell, Apple, ASUS, HP, Lenovo)
- **Store 2:** Headphones (Sony, Bose, Apple, Sennheiser, Beats)
- **Store 3:** Cameras (Canon, Sony, Fujifilm, Nikon, Panasonic)
- **Store 4:** Monitors (Dell, LG, ASUS, Samsung, BenQ)
- **Store 5:** Gaming Keyboards (Keychron, Logitech, Razer, Corsair, SteelSeries)

## Project Structure

```
e-commerce-platform/
├── flask_store/
│   ├── __init__.py           # App factory
│   ├── users/                # User authentication & management
│   ├── credit_card/          # User's credit card
│   ├── stores/               # Store management
│   ├── products/             # Product CRUD operations
│   ├── discounts/            # Discount system
│   ├── cart/                 # Shopping cart
│   ├── line_items/           # Line item
│   ├── orders/               # Order processing
│   ├── reviews/              # Product reviews
│   ├── static/               # CSS, JS, images
│   └── templates/            # HTML templates
├── seed_data.py              # Database initialization script
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Database Schema

The application uses the following main tables:
- `users` - User accounts with role flags (admin, owner, customer)
- `stores` - Store information
- `products` - Product catalog
- `line item` - Line item
- `discounts` - Discount codes with inheritance (Seasoning, SpecialEvent, Shipping)
- `carts` - Shopping cart items
- `orders` - Order records
- `reviews` - Product reviews
- `credit card` - User's credit card

## Development Notes

- The application uses Flask's development server (not for production use)
- Debug mode is enabled by default in `run.py`
- Product images are stored locally in `static/product_pics/`
- Passwords are hashed using bcrypt

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in `POSTGRES` configuration
- Ensure database `mystore` exists in pgAdmin

### Import Errors
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Product Images Not Showing
- Place image files (product1.png - product25.png) in `flask_store/static/product_pics/`
- Ensure filenames match exactly (case-sensitive)
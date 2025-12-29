CREATE TYPE discount_type AS ENUM ('shipping', 'seasoning', 'special_event');
CREATE TYPE lineitem_type AS ENUM ('cart', 'order');
CREATE TYPE order_status AS ENUM ('received', 'processed', 'shipped', 'closed');

CREATE TABLE store (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(10) NOT NULL,
    reg_date DATE NOT NULL DEFAULT CURRENT_DATE,
    balance INTEGER
);

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    f_name VARCHAR(20) NOT NULL,
    l_name VARCHAR(20) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL,
    phone VARCHAR(10) NOT NULL,
    birth DATE,
    address VARCHAR(200),
    reg_date DATE NOT NULL DEFAULT CURRENT_DATE,
    a_flag BOOLEAN NOT NULL,
    o_flag BOOLEAN NOT NULL,
    c_flag BOOLEAN NOT NULL,
    store_id INTEGER,

    CONSTRAINT fk_user_store
        FOREIGN KEY (store_id)
        REFERENCES store(id)
        ON UPDATE SET NULL
        ON DELETE SET NULL
);

CREATE TABLE discount (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    discount_percent FLOAT,
    is_active BOOLEAN DEFAULT FALSE,
    code VARCHAR(50) UNIQUE,
    type discount_type NOT NULL,
    creator_id INTEGER,

    CONSTRAINT fk_discount_creator
        FOREIGN KEY (creator_id)
        REFERENCES "user"(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE shipping (
    discount_id INTEGER PRIMARY KEY,
    min_purchase INTEGER,

    CONSTRAINT fk_shipping_discount
        FOREIGN KEY (discount_id)
        REFERENCES discount(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE seasoning (
    discount_id INTEGER PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,

    CONSTRAINT seasoning_valid_date_range
        CHECK (end_date >= start_date),

    CONSTRAINT fk_seasoning_discount
        FOREIGN KEY (discount_id)
        REFERENCES discount(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE special_event (
    discount_id INTEGER PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,

    CONSTRAINT special_event_valid_date_range
        CHECK (end_date >= start_date),

    CONSTRAINT fk_special_event_discount
        FOREIGN KEY (discount_id)
        REFERENCES discount(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image VARCHAR(200),
    buy_price INTEGER NOT NULL,
    sell_price INTEGER NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    manufacturer VARCHAR(100),
    type VARCHAR(50),
    model VARCHAR(100),
    store_id INTEGER NOT NULL,
    discount_id INTEGER,

    CONSTRAINT fk_product_store
        FOREIGN KEY (store_id)
        REFERENCES store(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_product_discount
        FOREIGN KEY (discount_id)
        REFERENCES discount(id)
        ON DELETE SET NULL
);

CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    quantity INTEGER NOT NULL DEFAULT 1,
    date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,

    CONSTRAINT fk_cart_user
        FOREIGN KEY (user_id)
        REFERENCES "user"(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_cart_product
        FOREIGN KEY (product_id)
        REFERENCES product(id)
        ON DELETE CASCADE
);

CREATE TABLE "order" (
    id SERIAL PRIMARY KEY,
    status order_status NOT NULL,
    total_amount INTEGER NOT NULL,
    shipping_cost INTEGER NOT NULL,
    cust_address TEXT NOT NULL,
    estimated_delivery_date DATE NOT NULL,
    order_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completion_time TIMESTAMP,

    order_manager_id INTEGER,
    customer_id INTEGER,
    shipping_discount_id INTEGER,
    cart_id INTEGER,

    CONSTRAINT fk_order_manager
        FOREIGN KEY (order_manager_id)
        REFERENCES "user"(id),

    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES "user"(id),

    CONSTRAINT fk_order_discount
        FOREIGN KEY (shipping_discount_id)
        REFERENCES discount(id),

    CONSTRAINT fk_order_cart
        FOREIGN KEY (cart_id)
        REFERENCES cart(id)
);

CREATE TABLE line_item (
    id SERIAL PRIMARY KEY,
    quantity INTEGER NOT NULL,
    type lineitem_type NOT NULL,
    total_price FLOAT NOT NULL,

    product_id INTEGER NOT NULL,
    order_id INTEGER,
    cart_id INTEGER,

    CONSTRAINT fk_lineitem_product
        FOREIGN KEY (product_id)
        REFERENCES product(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_lineitem_order
        FOREIGN KEY (order_id)
        REFERENCES "order"(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_lineitem_cart
        FOREIGN KEY (cart_id)
        REFERENCES cart(id)
        ON DELETE CASCADE
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    stars INTEGER NOT NULL,
    description TEXT,
    review_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,

    CONSTRAINT fk_review_user
        FOREIGN KEY (user_id)
        REFERENCES "user"(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_review_order
        FOREIGN KEY (order_id)
        REFERENCES "order"(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_review_product
        FOREIGN KEY (product_id)
        REFERENCES product(id)
        ON DELETE CASCADE
);
/* =====================================================
   CLEAN START
   ===================================================== */
TRUNCATE
reviews,
line_item,
"order",
cart,
product,
special_event,
seasoning,
shipping,
discount,
"user",
store
RESTART IDENTITY CASCADE;


/* =====================================================
   1. STORE (Electronics Shops)
   ===================================================== */
INSERT INTO store (name, email, phone, balance) VALUES
('ElectroMart', 'support@electromart.com', '0912345678', 150000),
('Gadget World', 'contact@gadgetworld.com', '0923456789', 98000);


/* =====================================================
   2. USER
   ===================================================== */
INSERT INTO "user"
(f_name, l_name, email, password, phone, birth, address,
 a_flag, o_flag, c_flag, store_id)
VALUES
-- Admin
('Harrison', 'Mckinney', 'admin@ecommerce.com', 'admin123', '0910000001',
 '1990-01-15', 'Taipei', TRUE, FALSE, FALSE, NULL),

-- Store Owners (STORE 1 → ElectroMart)
('Hudson', 'Smith', 'owner1@electromart.com', 'ownerone123', '0920000002',
 '1988-05-20', 'Taichung', FALSE, TRUE, FALSE, 1),

-- SECOND OWNER FOR SAME STORE (ElectroMart)
('Daniel', 'Tan', 'owner2@electromart.com', 'ownertwo123', '0968888888',
 '1992-08-12', 'Taipei', FALSE, TRUE, FALSE, 1),

-- Store Owner (STORE 2 → Gadget World)
('Sophia', 'Wilson', 'owner3@gadgetworld.com', 'owner12345', '0930000003',
 '1991-05-17', 'Kaohsiung', FALSE, TRUE, FALSE, 2),

-- Customers
('Chris', 'Lee', 'customer1@gmail.com', 'custone123', '0940000004',
 '1995-03-10', 'Tainan', FALSE, FALSE, TRUE, NULL),

('Emily', 'Davis', 'customer2@gmail.com', 'custtwo123', '0950000005',
 '1999-02-14', 'Taipei', FALSE, FALSE, TRUE, NULL);


/* =====================================================
   3. DISCOUNT
   ===================================================== */
INSERT INTO discount
(name, description, discount_percent, is_active, code, type, creator_id)
VALUES
('Free Shipping Over 1000', 'Free shipping for orders above NT$1000',
 0.00, TRUE, 'SHIP1000', 'shipping', 1),

('Accessory Sale', '10% discount on accessories',
 0.10, TRUE, 'ACC10', 'seasoning', 1),

('Flash Sale Event', '50% off selected electronics',
 0.50, TRUE, 'FLASH50', 'special_event', 1);


/* =====================================================
   4. SHIPPING / SEASONING / SPECIAL EVENT
   ===================================================== */
INSERT INTO shipping (discount_id, min_purchase)
VALUES (1, 1000);

INSERT INTO seasoning (discount_id, start_date, end_date)
VALUES (2, '2024-11-01', '2024-11-30');

INSERT INTO special_event (discount_id, start_date, end_date)
VALUES (3, '2024-12-01', '2024-12-31');


/* =====================================================
   5. PRODUCT (Electronics)
   ===================================================== */
INSERT INTO product
(name, description, buy_price, sell_price, stock,
 manufacturer, type, model, store_id, discount_id)
VALUES
('iPhone 14', 'Apple smartphone 128GB',
 20000, 28900, 15, 'Apple', 'Smartphone', 'iPhone14', 1, 3),

('Samsung Galaxy S23', 'Android smartphone flagship',
 18000, 25900, 20, 'Samsung', 'Smartphone', 'S23', 1, NULL),

('MacBook Air M2', 'Apple laptop M2 chip',
 30000, 38900, 10, 'Apple', 'Laptop', 'MBA-M2', 2, 3),

('Dell XPS 13', 'Ultrabook laptop',
 28000, 36500, 8, 'Dell', 'Laptop', 'XPS13', 2, NULL),

('Wireless Mouse', 'Bluetooth mouse',
 300, 690, 50, 'Logitech', 'Accessory', 'M185', 1, 2),

('USB-C Charger', '65W fast charger',
 500, 1200, 40, 'Anker', 'Accessory', 'ANK-65W', 2, 2);


/* =====================================================
   6. CART
   ===================================================== */
INSERT INTO cart (quantity, user_id, product_id)
VALUES
(1, 5, 1),  -- Chris buys iPhone
(2, 5, 5),  -- Chris buys Mouse
(1, 6, 3);  -- Emily buys MacBook


/* =====================================================
   7. ORDER
   ===================================================== */
INSERT INTO "order"
(status, total_amount, shipping_cost, cust_address,
 estimated_delivery_date, customer_id, shipping_discount_id, cart_id)
VALUES
('received', 30300, 0, 'No.123 Zhongshan Rd, Taipei',
 CURRENT_DATE + 5, 5, 1, 1),

('shipped', 40100, 80, 'No.456 Minsheng Rd, Taichung',
 CURRENT_DATE + 3, 6, NULL, 3);


/* =====================================================
   8. LINE ITEM
   ===================================================== */
-- Order items
INSERT INTO line_item
(quantity, type, total_price, product_id, order_id)
VALUES
(1, 'order', 28900, 1, 1),
(2, 'order', 1380, 5, 1),
(1, 'order', 38900, 3, 2);

-- Cart items
INSERT INTO line_item
(quantity, type, total_price, product_id, cart_id)
VALUES
(1, 'cart', 28900, 1, 1),
(2, 'cart', 1380, 5, 2);


/* =====================================================
   9. REVIEW
   ===================================================== */
INSERT INTO reviews
(stars, description, user_id, order_id, product_id)
VALUES
(5, 'Fast delivery and excellent phone quality.', 5, 1, 1),
(4, 'Laptop performance is great, but packaging could improve.', 6, 2, 3);

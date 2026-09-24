-- =====================================================================
-- MysticML Journey · Week 2 · Module 5 – MySQL Keys
-- File: 02_keys_complete.sql
-- Covers: UNIQUE key (single + multi-column), PRIMARY key (inline, named,
--         added with ALTER), COMPOSITE key, FOREIGN key (ON DELETE /
--         ON UPDATE actions), adding/dropping keys, inspecting keys, and
--         what errors each key prevents.
-- Run:   mysql -u root -p < 02_keys_complete.sql
--        (statements that INTENTIONALLY fail are commented out – paste
--         them into the mysql client one at a time to see each error.)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_keys;
USE mysticml_keys;

DROP TABLE IF EXISTS order_items, orders, products, customers;

-- ---------------------------------------------------------------------
-- 1) PRIMARY KEY  – uniquely identifies each row; NOT NULL + UNIQUE;
--                   only ONE per table (can span several columns)
-- ---------------------------------------------------------------------
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT,
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL,
    phone       VARCHAR(20),
    CONSTRAINT pk_customers PRIMARY KEY (customer_id),   -- named primary key
    -- -----------------------------------------------------------------
    -- 2) UNIQUE KEY – no duplicates, but NULL is allowed (many NULLs OK);
    --                 a table can have MANY unique keys
    -- -----------------------------------------------------------------
    CONSTRAINT uq_customers_email UNIQUE (email),
    CONSTRAINT uq_customers_phone UNIQUE (phone)
);

-- PRIMARY KEY added AFTER creation with ALTER TABLE
CREATE TABLE products (
    sku          VARCHAR(20) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    brand        VARCHAR(50)  NOT NULL,
    model        VARCHAR(50)  NOT NULL,
    price        DECIMAL(10, 2) NOT NULL
);
ALTER TABLE products ADD PRIMARY KEY (sku);
-- Multi-column UNIQUE key: the PAIR (brand, model) must be unique
ALTER TABLE products ADD CONSTRAINT uq_brand_model UNIQUE (brand, model);

-- ---------------------------------------------------------------------
-- 4) FOREIGN KEY – a column that must match a key in a parent table
-- ---------------------------------------------------------------------
CREATE TABLE orders (
    order_id    INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date  DATE NOT NULL,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        ON DELETE CASCADE        -- delete a customer -> delete their orders
        ON UPDATE CASCADE        -- change a customer_id -> update here too
);

-- ---------------------------------------------------------------------
-- 3) COMPOSITE KEY – a primary key made of 2+ columns.
--    Here one order can contain a product only once.
-- ---------------------------------------------------------------------
CREATE TABLE order_items (
    order_id INT         NOT NULL,
    sku      VARCHAR(20) NOT NULL,
    quantity INT         NOT NULL DEFAULT 1,
    PRIMARY KEY (order_id, sku),                          -- composite key
    CONSTRAINT fk_items_order FOREIGN KEY (order_id)
        REFERENCES orders (order_id) ON DELETE CASCADE,
    CONSTRAINT fk_items_product FOREIGN KEY (sku)
        REFERENCES products (sku) ON DELETE RESTRICT      -- can't delete a product that was sold
);

-- ---------------------------------------------------------------------
-- Sample data
-- ---------------------------------------------------------------------
INSERT INTO customers (full_name, email, phone) VALUES
('Aadil Khan',   'aadil@example.com', '+91-90000-00001'),
('Emily Carter', 'emily@example.com', NULL),              -- NULL phone is fine
('Sama Iqbal',   'sama@example.com',  NULL);              -- another NULL is fine too

INSERT INTO products VALUES
('LP-14',  'Laptop Pro 14',  'Mystic', 'LP14', 1200.00),
('SP-X',   'Smartphone X',   'Mystic', 'SPX',   800.00),
('MS-01',  'Wireless Mouse', 'Clicko', 'M1',     25.00);

INSERT INTO orders (customer_id, order_date) VALUES (1, '2025-01-10'), (1, '2025-02-01'), (2, '2025-02-03');

INSERT INTO order_items VALUES
(1, 'LP-14', 1), (1, 'MS-01', 2),
(2, 'SP-X',  1),
(3, 'MS-01', 5);

-- ---------------------------------------------------------------------
-- What each key PREVENTS (uncomment one at a time to see the error)
-- ---------------------------------------------------------------------
-- Duplicate PRIMARY KEY  -> ERROR 1062 Duplicate entry 'LP-14' for key 'products.PRIMARY'
-- INSERT INTO products VALUES ('LP-14', 'Copy', 'X', 'Y', 1.00);

-- Duplicate UNIQUE email -> ERROR 1062 Duplicate entry ... for key 'customers.uq_customers_email'
-- INSERT INTO customers (full_name, email) VALUES ('Fake', 'aadil@example.com');

-- Duplicate COMPOSITE key (same order + same sku) -> ERROR 1062
-- INSERT INTO order_items VALUES (1, 'LP-14', 3);

-- FOREIGN KEY: parent row does not exist -> ERROR 1452 Cannot add or update a child row
-- INSERT INTO orders (customer_id, order_date) VALUES (999, '2025-03-01');

-- FOREIGN KEY RESTRICT: product is referenced -> ERROR 1451 Cannot delete a parent row
-- DELETE FROM products WHERE sku = 'MS-01';

-- ---------------------------------------------------------------------
-- ON DELETE CASCADE in action
-- ---------------------------------------------------------------------
SELECT o.order_id, c.full_name, oi.sku, oi.quantity
FROM orders o
JOIN customers c    ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id   = o.order_id
ORDER BY o.order_id;

DELETE FROM customers WHERE full_name = 'Emily Carter';   -- cascades to orders -> order_items

SELECT COUNT(*) AS orders_left FROM orders;               -- 2 (Emily's order is gone)
SELECT COUNT(*) AS items_left  FROM order_items;          -- 3

-- ---------------------------------------------------------------------
-- Inspecting keys
-- ---------------------------------------------------------------------
SHOW KEYS FROM order_items;

SELECT table_name, constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_schema = 'mysticml_keys'
ORDER BY table_name, constraint_type;

-- Foreign keys and the tables they point to
SELECT table_name, column_name, constraint_name,
       referenced_table_name, referenced_column_name
FROM information_schema.key_column_usage
WHERE table_schema = 'mysticml_keys' AND referenced_table_name IS NOT NULL;

-- ---------------------------------------------------------------------
-- Dropping keys
-- ---------------------------------------------------------------------
ALTER TABLE customers DROP INDEX uq_customers_phone;       -- a UNIQUE key is an index
ALTER TABLE order_items DROP FOREIGN KEY fk_items_product; -- drop FK by constraint name
-- (Dropping a PRIMARY KEY: ALTER TABLE t DROP PRIMARY KEY; — not allowed while
--  the column is AUTO_INCREMENT or referenced by a foreign key.)
SHOW KEYS FROM customers;

-- Optional cleanup:
-- DROP DATABASE IF EXISTS mysticml_keys;

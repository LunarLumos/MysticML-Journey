-- =====================================================================
-- MysticML Journey · Week 2 · SHARED SAMPLE DATASET  (mysticml_sales)
-- =====================================================================
-- A small, realistic (but SYNTHETIC, hand-written) retail sales dataset
-- used by:
--   * Module 7  – 02_clauses_complete.sql         (WHERE, HAVING, GROUP BY ...)
--   * Module 10 – 01_aggregate_functions.sql       (COUNT, SUM, AVG ...)
--
-- Re-running this script is safe: it drops and re-creates the three tables.
--
-- Run (from this folder):
--     mysql -u root -p < sample_sales_dataset.sql
--
-- Schema
--   customers (customer_id PK, customer_name, city, segment, signup_date)
--   products  (product_id  PK, product_name, category, unit_price)
--   sales     (sale_id PK, sale_date, customer_id FK, product_id FK,
--              sales_rep, region, quantity, unit_price, discount_pct)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_sales;
USE mysticml_sales;

-- Drop children first (sales references customers & products)
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

-- ---------------------------------------------------------------------
-- 1) customers
-- ---------------------------------------------------------------------
CREATE TABLE customers (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city          VARCHAR(50)  NOT NULL,
    segment       ENUM('Consumer', 'Corporate', 'Small Business') NOT NULL,
    signup_date   DATE NOT NULL
);

INSERT INTO customers (customer_name, city, segment, signup_date) VALUES
('Aadil Khan',      'Mumbai',    'Consumer',       '2024-03-12'),
('Emily Carter',    'Bengaluru', 'Corporate',      '2024-05-02'),
('Sama Iqbal',      'Delhi',     'Consumer',       '2024-06-18'),
('Rohan Mehta',     'Mumbai',    'Small Business', '2024-07-01'),
('Giya Thomas',     'Chennai',   'Consumer',       '2024-08-21'),
('Aayan Shaikh',    'Pune',      'Corporate',      '2024-09-09'),
('Priya Nair',      'Bengaluru', 'Small Business', '2024-10-14'),
('Zara Ali',        'Delhi',     'Consumer',       '2024-11-30');   -- has no sales yet (useful for joins)

-- ---------------------------------------------------------------------
-- 2) products
-- ---------------------------------------------------------------------
CREATE TABLE products (
    product_id   INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL UNIQUE,
    category     VARCHAR(50)  NOT NULL,
    unit_price   DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0)
);

INSERT INTO products (product_name, category, unit_price) VALUES
('Laptop Pro 14',      'Electronics', 1200.00),
('Smartphone X',       'Electronics',  800.00),
('Tablet Mini',        'Electronics',  450.00),
('Wireless Mouse',     'Accessories',   25.00),
('Mechanical Keyboard','Accessories',   90.00),
('27in Monitor',       'Electronics',  300.00),
('Office Chair',       'Furniture',    220.00),
('Standing Desk',      'Furniture',    540.00);

-- ---------------------------------------------------------------------
-- 3) sales  (one row = one order line)
-- ---------------------------------------------------------------------
CREATE TABLE sales (
    sale_id      INT AUTO_INCREMENT PRIMARY KEY,
    sale_date    DATE NOT NULL,
    customer_id  INT  NOT NULL,
    product_id   INT  NOT NULL,
    sales_rep    VARCHAR(50) NOT NULL,
    region       VARCHAR(20) NOT NULL,
    quantity     INT NOT NULL CHECK (quantity > 0),
    unit_price   DECIMAL(10, 2) NOT NULL,          -- price at time of sale
    discount_pct DECIMAL(4, 2)  NULL,              -- NULL = no discount info
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);

INSERT INTO sales (sale_date, customer_id, product_id, sales_rep, region, quantity, unit_price, discount_pct) VALUES
('2025-01-03', 1, 1, 'Neha',   'West',  1, 1200.00, 0.00),
('2025-01-05', 2, 2, 'Arjun',  'South', 5,  800.00, 10.00),
('2025-01-08', 3, 4, 'Kabir',  'North', 3,   25.00, NULL),
('2025-01-12', 4, 6, 'Neha',   'West',  2,  300.00, 5.00),
('2025-01-15', 5, 3, 'Arjun',  'South', 1,  450.00, 0.00),
('2025-01-20', 6, 8, 'Neha',   'West',  4,  540.00, 12.50),
('2025-01-27', 7, 5, 'Arjun',  'South', 6,   90.00, 5.00),
('2025-02-02', 1, 4, 'Neha',   'West',  2,   25.00, NULL),
('2025-02-04', 2, 1, 'Arjun',  'South', 3, 1150.00, 8.00),
('2025-02-09', 3, 2, 'Kabir',  'North', 1,  800.00, 0.00),
('2025-02-11', 4, 7, 'Neha',   'West',  8,  220.00, 15.00),
('2025-02-16', 5, 5, 'Arjun',  'South', 1,   90.00, NULL),
('2025-02-21', 6, 6, 'Neha',   'West',  10, 290.00, 10.00),
('2025-02-25', 3, 3, 'Kabir',  'North', 2,  450.00, 5.00),
('2025-03-01', 7, 1, 'Arjun',  'South', 2, 1200.00, 5.00),
('2025-03-04', 1, 2, 'Neha',   'West',  1,  799.00, 0.00),
('2025-03-10', 4, 8, 'Neha',   'West',  1,  540.00, NULL),
('2025-03-14', 2, 7, 'Arjun',  'South', 12, 210.00, 20.00),
('2025-03-18', 3, 5, 'Kabir',  'North', 2,   90.00, 0.00),
('2025-03-22', 6, 2, 'Neha',   'West',  6,  780.00, 10.00),
('2025-03-27', 5, 4, 'Arjun',  'South', 4,   25.00, 0.00),
('2025-04-02', 7, 6, 'Arjun',  'South', 3,  300.00, 5.00),
('2025-04-06', 1, 3, 'Neha',   'West',  1,  440.00, 0.00),
('2025-04-11', 3, 1, 'Kabir',  'North', 1, 1250.00, 0.00);

-- Quick sanity check
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'sales',    COUNT(*) FROM sales;

-- Optional cleanup (other modules depend on this DB, so drop it only when done):
-- DROP DATABASE IF EXISTS mysticml_sales;

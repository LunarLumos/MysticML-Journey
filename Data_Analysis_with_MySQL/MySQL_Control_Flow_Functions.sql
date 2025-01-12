-- Create the database
CREATE DATABASE control_flow_demo;
USE control_flow_demo;

-- Create the `orders` table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    product VARCHAR(50),
    quantity INT,
    price_per_unit DECIMAL(10, 2),
    status VARCHAR(20)
);

-- Insert sample data into `orders` table
INSERT INTO orders (customer_name, product, quantity, price_per_unit, status) VALUES
('Aadil', 'Laptop', 2, 1200.00, 'Shipped'),
('Emily', 'Tablet', 1, 500.00, NULL),
('Sama', 'Smartphone', 3, 800.00, 'Pending'),
('Aadil', 'Laptop', 1, 1500.00, 'Cancelled'),
('Emily', 'Tablet', 4, 450.00, 'Shipped');

-- Query 1: Use IF() to determine discount status for bulk orders
SELECT
    order_id,
    customer_name,
    product,
    IF(quantity > 2, 'Discounted', 'No Discount') AS discount_status
FROM orders;

--  Use CASE to create a status message
SELECT
    order_id,
    customer_name,
    product,
    CASE
        WHEN status = 'Shipped' THEN 'Order has been shipped'
        WHEN status = 'Pending' THEN 'Order is pending'
        WHEN status = 'Cancelled' THEN 'Order was cancelled'
        ELSE 'Status unknown'
    END AS status_message
FROM orders;

--  Use IFNULL() to replace NULL in the `status` column
SELECT
    order_id,
    customer_name,
    product,
    IFNULL(status, 'Not Provided') AS status_updated
FROM orders;

-- Use NULLIF() to handle special cases where price_per_unit might be 0
SELECT
    order_id,
    customer_name,
    product,
    NULLIF(price_per_unit, 0) AS price_per_unit_checked
FROM orders;

-- Combine all control flow functions for a full report
SELECT
    order_id,
    customer_name,
    product,
    quantity,
    price_per_unit,
    IFNULL(status, 'Not Provided') AS status_updated,
    CASE
        WHEN quantity > 2 THEN 'Bulk Order'
        ELSE 'Regular Order'
    END AS order_type,
    IF(price_per_unit > 1000, 'High Value', 'Standard Value') AS value_category
FROM orders;

-- Create the database
CREATE DATABASE sales_management;
USE sales_management;

-- Create the `sales` table
CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(100),
    product VARCHAR(50),
    amount DECIMAL(10, 2),
    sale_date DATE
);

-- Insert sample data into `sales` table
INSERT INTO sales (employee_name, product, amount, sale_date) VALUES
('Aadil', 'Laptop', 1200.00, '2025-01-01'),
('Emily', 'Smartphone', 800.00, '2025-01-02'),
('Sama', 'Tablet', 500.00, '2025-01-03'),
('Aadil', 'Laptop', 1500.00, '2025-01-05'),
('Emily', 'Smartphone', 900.00, '2025-01-06');

-- Use WHERE to filter sales by Aadil
SELECT * FROM sales WHERE employee_name = 'Aadil';

-- Use GROUP BY to calculate total sales amount by employee
SELECT employee_name, SUM(amount) AS total_sales
FROM sales
GROUP BY employee_name;

-- Use HAVING to filter employees with total sales > 1000
SELECT employee_name, SUM(amount) AS total_sales
FROM sales
GROUP BY employee_name
HAVING total_sales > 1000;

-- Use ORDER BY to sort sales by amount in descending order
SELECT * FROM sales ORDER BY amount DESC;

--Use LIMIT to display the top 3 sales
SELECT * FROM sales ORDER BY amount DESC LIMIT 3;

--  Use DISTINCT to list unique products sold
SELECT DISTINCT product FROM sales;

--  Combine clauses - Employees with sales > 1000, sorted by total sales
SELECT employee_name, SUM(amount) AS total_sales
FROM sales
GROUP BY employee_name
HAVING total_sales > 1000
ORDER BY total_sales DESC;

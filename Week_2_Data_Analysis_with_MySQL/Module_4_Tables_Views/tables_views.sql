-- =====================================================================
-- MysticML Journey · Week 2 · Module 4 – Tables & Views
-- Original practice file (learner's own work). The fuller companion
-- script in this folder is 02_*_complete.sql – see README.md.
-- Note: Has no CREATE DATABASE/USE: run `USE <some_db>;` first (e.g. USE mysticml_tables_views;).
-- =====================================================================

-- Create the 'employees' table with ID, name, and department.
CREATE TABLE employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_name VARCHAR(100),
    department VARCHAR(50)
);

-- Add a 'salary' column to the 'employees' table.
ALTER TABLE employees ADD salary DECIMAL(10, 2);

-- Insert employee records.
INSERT INTO employees (emp_name, department, salary)
VALUES ('Aayan', 'HR', 50000.00),
       ('Giya', 'IT', 65000.00);

-- View all records in the 'employees' table.
SELECT * FROM employees;

-- Create a view for HR employees with their name and salary.
CREATE VIEW hr_employees AS
SELECT emp_name, salary FROM employees WHERE department = 'HR';

-- View all records in the 'hr_employees' view.
SELECT * FROM hr_employees;

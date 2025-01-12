-- Create the database
CREATE DATABASE company_management;
USE company_management;

-- Create the `employees` table with constraints
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,  -- Primary Key
    name VARCHAR(100) NOT NULL,                  -- NOT NULL Constraint
    email VARCHAR(100) UNIQUE,                   -- UNIQUE Constraint
    age INT CHECK (age >= 18),                   -- CHECK Constraint
    salary DECIMAL(10, 2) DEFAULT 30000.00,      -- DEFAULT Constraint
    department VARCHAR(50) NOT NULL             -- NOT NULL Constraint
);

-- Create the `projects` table with constraints
CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,   -- Primary Key
    project_name VARCHAR(100) UNIQUE NOT NULL,   -- UNIQUE Constraint
    budget DECIMAL(10, 2) DEFAULT 50000.00       -- DEFAULT Constraint
);

-- Create the `assignments` table with Foreign Keys
CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,  -- Primary Key
    employee_id INT,                                -- Foreign Key
    project_id INT,                                 -- Foreign Key
    start_date DATE NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),  -- Foreign Key Constraint
    FOREIGN KEY (project_id) REFERENCES projects(project_id)      -- Foreign Key Constraint
);

-- Insert data into the `employees` table
INSERT INTO employees (name, email, age, salary, department) VALUES
('Aadil', 'aadil@example.com', 28, 55000.00, 'Finance'),
('Emily', 'emily@example.com', 25, 60000.00, 'HR'),
('Sama', 'sama@example.com', 30, 75000.00, 'IT');

-- Insert data into the `projects` table
INSERT INTO projects (project_name, budget) VALUES
('System Upgrade', 120000.00),
('Cloud Migration', 80000.00),
('Cybersecurity Enhancement', 100000.00);

-- Insert data into the `assignments` table
INSERT INTO assignments (employee_id, project_id, start_date) VALUES
(1, 1, '2025-01-01'),  -- Aadil assigned to System Upgrade
(2, 2, '2025-01-05'),  -- Emily assigned to Cloud Migration
(3, 3, '2025-01-10');  -- Sama assigned to Cybersecurity Enhancement

-- Query to view all employee data
SELECT * FROM employees;

-- Query to view all project data
SELECT * FROM projects;

-- Query to view assignments with employee and project details
SELECT
    a.assignment_id,
    e.name AS employee_name,
    p.project_name,
    a.start_date
FROM
    assignments a
JOIN
    employees e ON a.employee_id = e.employee_id
JOIN
    projects p ON a.project_id = p.project_id;

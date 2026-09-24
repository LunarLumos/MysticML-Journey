-- =====================================================================
-- MysticML Journey · Week 2 · Module 6 – MySQL Queries & Constraints
-- File: 02_queries_constraints_complete.sql
-- Covers: SELECT, INSERT (single / multi / INSERT IGNORE / ON DUPLICATE
--         KEY UPDATE), UPDATE, DELETE, ALTER, TRUNCATE, DROP, REPLACE,
--         INSERT INTO ... SELECT, and every constraint: NOT NULL, UNIQUE,
--         PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT (+ AUTO_INCREMENT).
-- Run:   mysql -u root -p < 02_queries_constraints_complete.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_queries;
USE mysticml_queries;

DROP TABLE IF EXISTS high_earners, employees, departments;

-- =====================================================================
-- PART A – CONSTRAINTS (rules the database enforces for you)
-- =====================================================================
CREATE TABLE departments (
    dept_id   INT AUTO_INCREMENT PRIMARY KEY,        -- PRIMARY KEY (+ AUTO_INCREMENT)
    dept_name VARCHAR(50) NOT NULL UNIQUE            -- NOT NULL + UNIQUE
);

CREATE TABLE employees (
    emp_id     INT AUTO_INCREMENT,
    emp_name   VARCHAR(100) NOT NULL,                              -- NOT NULL
    email      VARCHAR(100) NOT NULL,
    age        INT,
    salary     DECIMAL(10, 2) NOT NULL DEFAULT 30000.00,          -- DEFAULT
    status     VARCHAR(10)   NOT NULL DEFAULT 'active',            -- DEFAULT
    joined_on  DATE          NOT NULL DEFAULT (CURRENT_DATE),      -- DEFAULT (expression)
    dept_id    INT,
    CONSTRAINT pk_emp        PRIMARY KEY (emp_id),                 -- PRIMARY KEY
    CONSTRAINT uq_emp_email  UNIQUE (email),                       -- UNIQUE
    CONSTRAINT chk_emp_age   CHECK (age BETWEEN 18 AND 70),        -- CHECK (enforced in 8.0.16+)
    CONSTRAINT chk_emp_sal   CHECK (salary > 0),
    CONSTRAINT chk_status    CHECK (status IN ('active', 'on_leave', 'left')),
    CONSTRAINT fk_emp_dept   FOREIGN KEY (dept_id)                 -- FOREIGN KEY
        REFERENCES departments (dept_id) ON DELETE SET NULL
);

-- List every constraint we defined
SELECT table_name, constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_schema = 'mysticml_queries'
ORDER BY table_name, constraint_type;

-- Violations (uncomment one at a time to see the error):
-- NOT NULL    -> ERROR 1048 Column 'emp_name' cannot be null
-- INSERT INTO employees (emp_name, email) VALUES (NULL, 'x@example.com');
-- UNIQUE      -> ERROR 1062 Duplicate entry
-- INSERT INTO departments (dept_name) VALUES ('IT'), ('IT');
-- CHECK       -> ERROR 3819 Check constraint 'chk_emp_age' is violated
-- INSERT INTO employees (emp_name, email, age) VALUES ('Kid', 'kid@example.com', 12);
-- FOREIGN KEY -> ERROR 1452 Cannot add or update a child row
-- INSERT INTO employees (emp_name, email, dept_id) VALUES ('Ghost', 'g@example.com', 99);

-- =====================================================================
-- PART B – QUERIES
-- =====================================================================

-- 1) INSERT – single row, multiple rows, relying on DEFAULTs
INSERT INTO departments (dept_name) VALUES ('IT'), ('HR'), ('Finance');

INSERT INTO employees (emp_name, email, age, salary, dept_id)
VALUES ('Aadil', 'aadil@example.com', 28, 55000.00, 1);

INSERT INTO employees (emp_name, email, age, salary, dept_id) VALUES
('Emily', 'emily@example.com', 25, 60000.00, 2),
('Sama',  'sama@example.com',  30, 75000.00, 1),
('Rohan', 'rohan@example.com', 41, 82000.00, 3);

-- Only required columns: salary, status, joined_on come from DEFAULT
INSERT INTO employees (emp_name, email) VALUES ('Giya', 'giya@example.com');

-- 2) SELECT
SELECT * FROM employees;
SELECT emp_name, salary FROM employees WHERE salary > 58000 ORDER BY salary DESC;

-- 3) UPDATE (always use WHERE, or every row changes!)
UPDATE employees SET salary = salary * 1.05 WHERE dept_id = 1;
UPDATE employees SET status = 'on_leave', age = 26 WHERE emp_name = 'Emily';
SELECT emp_name, salary, status FROM employees;

-- 4) REPLACE – like INSERT, but if the PRIMARY KEY / UNIQUE value already
--    exists, the old row is DELETED and the new one INSERTED.
--    ⚠ Columns you don't list get their DEFAULT again (data can be lost).
REPLACE INTO employees (emp_id, emp_name, email, age, salary, dept_id)
VALUES (5, 'Giya', 'giya@example.com', 24, 48000.00, 2);       -- replaces emp_id 5
REPLACE INTO employees (emp_name, email, age, salary, dept_id)
VALUES ('Zara', 'zara@example.com', 29, 51000.00, 3);          -- no conflict -> plain insert
SELECT emp_id, emp_name, age, salary, dept_id FROM employees;

-- Related "upsert" alternatives
INSERT IGNORE INTO employees (emp_name, email) VALUES ('Dup', 'aadil@example.com'); -- skipped, warning only
INSERT INTO employees (emp_name, email, salary)
VALUES ('Aadil', 'aadil@example.com', 99999.00) AS new_row
ON DUPLICATE KEY UPDATE salary = new_row.salary;               -- update in place, keeps emp_id
SELECT emp_id, emp_name, salary FROM employees WHERE email = 'aadil@example.com';

-- 5) INSERT INTO ... SELECT – copy rows from a query into another table
CREATE TABLE high_earners (
    emp_id    INT PRIMARY KEY,
    emp_name  VARCHAR(100) NOT NULL,
    dept_name VARCHAR(50),
    salary    DECIMAL(10, 2) NOT NULL
);

INSERT INTO high_earners (emp_id, emp_name, dept_name, salary)
SELECT e.emp_id, e.emp_name, d.dept_name, e.salary
FROM employees e
LEFT JOIN departments d ON d.dept_id = e.dept_id
WHERE e.salary >= 60000;

SELECT * FROM high_earners ORDER BY salary DESC;

-- 6) DELETE – remove specific rows
DELETE FROM employees WHERE status = 'on_leave';
-- FOREIGN KEY ON DELETE SET NULL: deleting a department un-assigns its staff
DELETE FROM departments WHERE dept_name = 'Finance';
SELECT emp_name, dept_id FROM employees;

-- 7) ALTER – change structure (add a column + a new constraint)
ALTER TABLE employees ADD COLUMN phone VARCHAR(20) NULL;
ALTER TABLE employees ADD CONSTRAINT uq_emp_phone UNIQUE (phone);
ALTER TABLE employees ALTER COLUMN status SET DEFAULT 'active';   -- change a DEFAULT
ALTER TABLE employees DROP CHECK chk_emp_sal;                     -- remove a CHECK
DESCRIBE employees;

-- 8) TRUNCATE – delete ALL rows quickly and reset AUTO_INCREMENT
TRUNCATE TABLE high_earners;
SELECT COUNT(*) AS high_earners_after_truncate FROM high_earners;

-- 9) DROP – remove the table entirely
DROP TABLE high_earners;
SHOW TABLES;

-- Optional cleanup:
-- DROP DATABASE IF EXISTS mysticml_queries;

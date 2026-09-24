-- =====================================================================
-- MysticML Journey · Week 2 · Module 4 – Tables & Views
-- File: 02_tables_views_complete.sql
-- Covers: CREATE TABLE, ALTER TABLE (ADD / DROP / MODIFY / CHANGE / RENAME
--         COLUMN), SHOW TABLES, DESCRIBE, RENAME TABLE, copy a table,
--         TRUNCATE, DROP TABLE, and views: CREATE / SELECT / UPDATE
--         (CREATE OR REPLACE, ALTER VIEW, updatable views) / DROP.
-- Run:   mysql -u root -p < 02_tables_views_complete.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_tables_views;
USE mysticml_tables_views;

-- Start clean so the script can be re-run
DROP VIEW  IF EXISTS v_it_staff, v_dept_summary;
DROP TABLE IF EXISTS employees, staff, staff_backup, staff_structure_only, staff_it_only;

-- =====================================================================
-- PART A – TABLES
-- =====================================================================

-- 1) CREATE TABLE
CREATE TABLE employees (
    emp_id     INT AUTO_INCREMENT PRIMARY KEY,
    emp_name   VARCHAR(50) NOT NULL,
    department VARCHAR(30) NOT NULL,
    salary     DECIMAL(10, 2)
);

INSERT INTO employees (emp_name, department, salary) VALUES
('Aayan', 'HR',      50000.00),
('Giya',  'IT',      65000.00),
('Aadil', 'IT',      72000.00),
('Emily', 'Finance', 58000.00),
('Sama',  'IT',      61000.00);

-- 2) SHOW TABLES / DESCRIBE
SHOW TABLES;
DESCRIBE employees;               -- same as: SHOW COLUMNS FROM employees;
SHOW CREATE TABLE employees;      -- full DDL including keys and engine

-- 3) ALTER TABLE – ADD a column (optionally choose its position)
ALTER TABLE employees ADD COLUMN email VARCHAR(100) AFTER emp_name;
ALTER TABLE employees ADD COLUMN hired_on DATE DEFAULT (CURRENT_DATE);

-- ... MODIFY a column's definition (type / NULL-ability / default)
ALTER TABLE employees MODIFY COLUMN emp_name VARCHAR(100) NOT NULL;

-- ... CHANGE = rename + redefine in one go
ALTER TABLE employees CHANGE COLUMN salary monthly_salary DECIMAL(12, 2);

-- ... RENAME COLUMN (MySQL 8+), keeps the definition
ALTER TABLE employees RENAME COLUMN department TO dept;

-- ... DROP (delete) a column
ALTER TABLE employees DROP COLUMN email;

DESCRIBE employees;

-- 4) RENAME TABLE
RENAME TABLE employees TO staff;          -- or: ALTER TABLE employees RENAME TO staff;
SHOW TABLES;

-- 5) COPY TABLE
-- 5a) structure + data in one step (keys/AUTO_INCREMENT are NOT copied)
CREATE TABLE staff_backup AS SELECT * FROM staff;

-- 5b) structure only, including indexes & primary key
CREATE TABLE staff_structure_only LIKE staff;

-- 5c) faithful copy = LIKE + INSERT ... SELECT, optionally filtered
CREATE TABLE staff_it_only LIKE staff;
INSERT INTO staff_it_only SELECT * FROM staff WHERE dept = 'IT';

SELECT 'staff' AS tbl, COUNT(*) AS rows_ FROM staff
UNION ALL SELECT 'staff_backup',         COUNT(*) FROM staff_backup
UNION ALL SELECT 'staff_structure_only', COUNT(*) FROM staff_structure_only
UNION ALL SELECT 'staff_it_only',        COUNT(*) FROM staff_it_only;

-- 6) TRUNCATE – remove ALL rows fast, keep the structure, reset AUTO_INCREMENT
TRUNCATE TABLE staff_backup;
SELECT COUNT(*) AS rows_after_truncate FROM staff_backup;

-- 7) DROP TABLE – remove the table completely (structure + data)
DROP TABLE IF EXISTS staff_backup, staff_structure_only;
SHOW TABLES;

-- =====================================================================
-- PART B – VIEWS  (a view is a saved SELECT that behaves like a table)
-- =====================================================================

-- 1) CREATE VIEW
CREATE VIEW v_it_staff AS
SELECT emp_id, emp_name, monthly_salary
FROM staff
WHERE dept = 'IT';

-- 2) SELECT from a view exactly like a table
SELECT * FROM v_it_staff ORDER BY monthly_salary DESC;

-- A view with aggregation (read-only because of GROUP BY)
CREATE VIEW v_dept_summary AS
SELECT dept, COUNT(*) AS headcount, ROUND(AVG(monthly_salary), 2) AS avg_salary
FROM staff
GROUP BY dept;

SELECT * FROM v_dept_summary;

-- List views in this database
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SHOW CREATE VIEW v_it_staff;

-- 3) UPDATE a view DEFINITION
-- 3a) CREATE OR REPLACE VIEW – redefine (or create if missing)
CREATE OR REPLACE VIEW v_it_staff AS
SELECT emp_id, emp_name, dept, monthly_salary
FROM staff
WHERE dept = 'IT';

-- 3b) ALTER VIEW – redefine an existing view; WITH CHECK OPTION blocks
--     inserts/updates through the view that would fall outside its WHERE
ALTER VIEW v_it_staff AS
SELECT emp_id, emp_name, dept, monthly_salary
FROM staff
WHERE dept = 'IT'
WITH CHECK OPTION;

-- 4) UPDATE DATA THROUGH a view (simple views are "updatable")
UPDATE v_it_staff SET monthly_salary = monthly_salary * 1.10 WHERE emp_name = 'Giya';
SELECT emp_name, monthly_salary FROM staff WHERE emp_name = 'Giya';  -- base table changed

-- Because of WITH CHECK OPTION this would FAIL (moves the row out of the view):
-- UPDATE v_it_staff SET dept = 'HR' WHERE emp_name = 'Giya';

-- Views stay in sync with their base table automatically
INSERT INTO staff (emp_name, dept, monthly_salary) VALUES ('Rohan', 'IT', 59000.00);
SELECT * FROM v_it_staff;
SELECT * FROM v_dept_summary;

-- 5) DROP VIEW (the base table is not affected)
DROP VIEW IF EXISTS v_dept_summary;
SHOW FULL TABLES;

-- Optional cleanup:
-- DROP DATABASE IF EXISTS mysticml_tables_views;

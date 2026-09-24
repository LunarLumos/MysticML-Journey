-- =====================================================================
-- MysticML Journey · Week 2 · Module 9 – MySQL Joins
-- File: 02_joins_complete.sql
-- Covers: INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN emulation,
--         CROSS JOIN, SELF JOIN (hierarchy), anti-join, joining 3 tables,
--         USING vs ON, DELETE JOIN and UPDATE JOIN.
-- Run:   mysql -u root -p < 02_joins_complete.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_joins;
USE mysticml_joins;

DROP TABLE IF EXISTS project_assignments, projects, employees, departments, shifts;

-- ---------------------------------------------------------------------
-- Sample schema
-- ---------------------------------------------------------------------
CREATE TABLE departments (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(30) NOT NULL,
    budget_k  INT NOT NULL                 -- budget in thousands
);

CREATE TABLE employees (
    emp_id     INT PRIMARY KEY,
    emp_name   VARCHAR(30) NOT NULL,
    dept_id    INT NULL,                   -- NULL = not assigned to a department
    manager_id INT NULL,                   -- points to another employee (self join)
    salary     INT NOT NULL,
    is_active  BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE projects (
    project_id   INT PRIMARY KEY,
    project_name VARCHAR(40) NOT NULL,
    dept_id      INT NULL
);

CREATE TABLE project_assignments (
    emp_id     INT,
    project_id INT,
    hours      INT NOT NULL,
    PRIMARY KEY (emp_id, project_id)
);

CREATE TABLE shifts (shift_name VARCHAR(10) PRIMARY KEY);

INSERT INTO departments VALUES
(10, 'Engineering', 500), (20, 'Marketing', 200), (30, 'Finance', 150), (40, 'Legal', 80);  -- Legal has no staff

INSERT INTO employees VALUES
(1, 'Aadil',  10, NULL, 120000, TRUE),   -- CTO, no manager
(2, 'Emily',  10, 1,     95000, TRUE),
(3, 'Sama',   10, 2,     70000, TRUE),
(4, 'Rohan',  20, 1,     80000, TRUE),
(5, 'Giya',   20, 4,     60000, FALSE),  -- inactive
(6, 'Aayan',  30, 1,     75000, TRUE),
(7, 'Zara',   NULL, 1,   50000, TRUE);   -- no department

INSERT INTO projects VALUES
(100, 'Recommendation Engine', 10),
(101, 'Brand Campaign',        20),
(102, 'Budget Forecast',       30),
(103, 'Data Platform',         NULL),    -- no owning department
(104, 'Office Relocation',     40);      -- nobody assigned yet

INSERT INTO project_assignments VALUES
(1, 100, 10), (2, 100, 30), (3, 100, 40), (3, 103, 20),
(4, 101, 35), (5, 101, 15), (6, 102, 25);

INSERT INTO shifts VALUES ('Morning'), ('Evening');

-- ---------------------------------------------------------------------
-- 1) INNER JOIN – only rows that match in BOTH tables
--    (Zara has no dept, Legal has no staff -> both disappear)
-- ---------------------------------------------------------------------
SELECT e.emp_name, d.dept_name
FROM employees e
INNER JOIN departments d ON d.dept_id = e.dept_id
ORDER BY e.emp_id;

-- USING(col) is shorthand when the column has the same name in both tables
SELECT emp_name, dept_name FROM employees JOIN departments USING (dept_id) LIMIT 3;

-- ---------------------------------------------------------------------
-- 2) LEFT JOIN – ALL rows from the left table, NULLs where no match
-- ---------------------------------------------------------------------
SELECT e.emp_name, d.dept_name
FROM employees e
LEFT JOIN departments d ON d.dept_id = e.dept_id
ORDER BY e.emp_id;                      -- Zara appears with dept_name NULL

-- Anti-join: rows in LEFT with NO match (departments without employees)
SELECT d.dept_name
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
WHERE e.emp_id IS NULL;                 -- Legal

-- ---------------------------------------------------------------------
-- 3) RIGHT JOIN – ALL rows from the right table
-- ---------------------------------------------------------------------
SELECT e.emp_name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON d.dept_id = e.dept_id
ORDER BY d.dept_id;                     -- Legal appears with emp_name NULL

-- FULL OUTER JOIN does not exist in MySQL: LEFT JOIN  UNION  RIGHT JOIN
SELECT e.emp_name, d.dept_name
FROM employees e LEFT JOIN departments d ON d.dept_id = e.dept_id
UNION
SELECT e.emp_name, d.dept_name
FROM employees e RIGHT JOIN departments d ON d.dept_id = e.dept_id;

-- ---------------------------------------------------------------------
-- 4) CROSS JOIN – every combination (Cartesian product): 7 x 2 = 14 rows
-- ---------------------------------------------------------------------
SELECT e.emp_name, s.shift_name
FROM employees e
CROSS JOIN shifts s
WHERE e.is_active
ORDER BY e.emp_name, s.shift_name;

SELECT COUNT(*) AS combinations FROM employees CROSS JOIN shifts;

-- ---------------------------------------------------------------------
-- 5) SELF JOIN – a table joined to itself (needs two aliases)
-- ---------------------------------------------------------------------
-- Employee -> manager
SELECT e.emp_name AS employee,
       IFNULL(m.emp_name, '(top)') AS manager
FROM employees e
LEFT JOIN employees m ON m.emp_id = e.manager_id
ORDER BY e.emp_id;

-- Employees earning more than their manager? (none – sanity check)
SELECT e.emp_name, e.salary, m.emp_name AS manager, m.salary AS manager_salary
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
WHERE e.salary > m.salary;

-- Pairs of colleagues in the same department (e1 < e2 avoids duplicates)
SELECT a.emp_name AS colleague_1, b.emp_name AS colleague_2, a.dept_id
FROM employees a
JOIN employees b ON a.dept_id = b.dept_id AND a.emp_id < b.emp_id;

-- ---------------------------------------------------------------------
-- 6) Joining THREE tables + aggregation
-- ---------------------------------------------------------------------
SELECT p.project_name,
       IFNULL(d.dept_name, '-')     AS owner_dept,
       COUNT(pa.emp_id)             AS people,
       SUM(pa.hours)                AS total_hours,
       GROUP_CONCAT(e.emp_name ORDER BY e.emp_name) AS team
FROM projects p
LEFT JOIN departments d          ON d.dept_id = p.dept_id
LEFT JOIN project_assignments pa ON pa.project_id = p.project_id
LEFT JOIN employees e            ON e.emp_id = pa.emp_id
GROUP BY p.project_id, p.project_name, d.dept_name
ORDER BY total_hours DESC;

-- ---------------------------------------------------------------------
-- 7) UPDATE JOIN – update one table using values from another
--    Give a 10% raise to everyone in departments with budget >= 200k
-- ---------------------------------------------------------------------
SELECT e.emp_name, e.salary AS salary_before, d.budget_k
FROM employees e JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.emp_id;

UPDATE employees e
INNER JOIN departments d ON d.dept_id = e.dept_id
SET e.salary = ROUND(e.salary * 1.10)
WHERE d.budget_k >= 200;

SELECT emp_name, salary AS salary_after FROM employees ORDER BY emp_id;

-- UPDATE with LEFT JOIN: flag employees with no department as inactive
UPDATE employees e
LEFT JOIN departments d ON d.dept_id = e.dept_id
SET e.is_active = FALSE
WHERE d.dept_id IS NULL;

-- ---------------------------------------------------------------------
-- 8) DELETE JOIN – delete rows based on a join
-- ---------------------------------------------------------------------
-- 8a) Delete assignments that belong to INACTIVE employees
--     (only the table(s) named after DELETE lose rows)
DELETE pa
FROM project_assignments pa
INNER JOIN employees e ON e.emp_id = pa.emp_id
WHERE e.is_active = FALSE;

-- 8b) Delete from TWO tables at once: Finance's projects and their assignments
DELETE p, pa
FROM projects p
LEFT JOIN project_assignments pa ON pa.project_id = p.project_id
WHERE p.dept_id = 30;

-- 8c) Delete with LEFT JOIN (anti-join): projects nobody works on (Office Relocation)
DELETE p
FROM projects p
LEFT JOIN project_assignments pa ON pa.project_id = p.project_id
WHERE pa.project_id IS NULL;

SELECT * FROM projects;
SELECT * FROM project_assignments ORDER BY project_id, emp_id;

-- Optional cleanup:
-- DROP DATABASE IF EXISTS mysticml_joins;

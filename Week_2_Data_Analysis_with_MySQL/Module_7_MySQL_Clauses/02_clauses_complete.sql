-- =====================================================================
-- MysticML Journey · Week 2 · Module 7 – MySQL Clauses
-- File: 02_clauses_complete.sql
-- Covers: FROM (tables, joins, subqueries), WHERE (all common operators),
--         DISTINCT, GROUP BY (incl. WITH ROLLUP), HAVING, ORDER BY, LIMIT,
--         and the logical order in which MySQL evaluates them.
-- Data:  the shared mysticml_sales dataset (sample_sales_dataset.sql).
-- Run (from this folder) – load the dataset, then this file:
--        mysql -u root -p < sample_sales_dataset.sql
--        mysql -u root -p < 02_clauses_complete.sql
--   or in one go:
--        cat sample_sales_dataset.sql 02_clauses_complete.sql | mysql -u root -p
--   (Inside an interactive mysql session you can also type:
--        SOURCE sample_sales_dataset.sql;  – note: MySQL 8.4+/9 clients
--    ignore SOURCE in piped/batch mode unless started with --commands.)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_sales;
USE mysticml_sales;

-- Helper expression used below: line revenue = quantity * unit_price * (1 - discount)
-- (discount_pct can be NULL, so IFNULL(..., 0) treats "unknown" as "no discount")

-- ---------------------------------------------------------------------
-- 1) FROM – where rows come from
-- ---------------------------------------------------------------------
SELECT * FROM products;                                    -- a table

SELECT s.sale_id, c.customer_name, p.product_name          -- several tables (a join)
FROM sales s
JOIN customers c ON c.customer_id = s.customer_id
JOIN products  p ON p.product_id  = s.product_id
LIMIT 5;

SELECT region, total                                        -- a derived table (subquery)
FROM (SELECT region, SUM(quantity * unit_price) AS total
      FROM sales GROUP BY region) AS region_totals;

-- ---------------------------------------------------------------------
-- 2) WHERE – filter ROWS (before grouping)
-- ---------------------------------------------------------------------
SELECT sale_id, sale_date, region, quantity FROM sales
WHERE region = 'West' AND quantity >= 4;                    -- comparison + AND

SELECT customer_name, city FROM customers
WHERE city IN ('Mumbai', 'Pune');                           -- IN list

SELECT sale_id, sale_date FROM sales
WHERE sale_date BETWEEN '2025-02-01' AND '2025-02-28';      -- range (inclusive)

SELECT product_name FROM products
WHERE product_name LIKE '%top%' OR product_name LIKE 'S%';  -- pattern: % any, _ one char

SELECT sale_id, discount_pct FROM sales
WHERE discount_pct IS NULL;                                 -- NULL needs IS NULL, not = NULL

SELECT customer_name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM sales);   -- subquery: customers with no sales

-- ---------------------------------------------------------------------
-- 3) DISTINCT – remove duplicate result rows
-- ---------------------------------------------------------------------
SELECT DISTINCT region FROM sales;
SELECT DISTINCT region, sales_rep FROM sales ORDER BY region;  -- unique COMBINATIONS
SELECT COUNT(DISTINCT customer_id) AS buying_customers FROM sales;

-- ---------------------------------------------------------------------
-- 4) GROUP BY – one output row per group, with aggregates
-- ---------------------------------------------------------------------
SELECT region,
       COUNT(*)                                                         AS orders,
       SUM(quantity)                                                    AS units,
       ROUND(SUM(quantity * unit_price * (1 - IFNULL(discount_pct, 0) / 100)), 2) AS revenue
FROM sales
GROUP BY region;

-- Group by several columns, and by an expression (month)
SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month, region, COUNT(*) AS orders
FROM sales
GROUP BY month, region
ORDER BY month, region;

-- WITH ROLLUP adds subtotal rows and a grand total (NULL = "all")
SELECT IFNULL(p.category, 'ALL CATEGORIES') AS category,
       SUM(s.quantity) AS units
FROM sales s JOIN products p ON p.product_id = s.product_id
GROUP BY p.category WITH ROLLUP;

-- ---------------------------------------------------------------------
-- 5) HAVING – filter GROUPS (after aggregation)
-- ---------------------------------------------------------------------
SELECT sales_rep,
       ROUND(SUM(quantity * unit_price * (1 - IFNULL(discount_pct, 0) / 100)), 2) AS revenue
FROM sales
GROUP BY sales_rep
HAVING revenue > 10000;

-- WHERE and HAVING together: only 2025-Q1 rows, then only busy customers
SELECT customer_id, COUNT(*) AS q1_orders
FROM sales
WHERE sale_date < '2025-04-01'          -- row filter
GROUP BY customer_id
HAVING COUNT(*) >= 4;                    -- group filter

-- ---------------------------------------------------------------------
-- 6) ORDER BY (+ LIMIT)
-- ---------------------------------------------------------------------
SELECT product_name, category, unit_price FROM products
ORDER BY category ASC, unit_price DESC;  -- multi-column sort

-- Top 3 order lines by value
SELECT sale_id, quantity * unit_price AS line_value FROM sales
ORDER BY line_value DESC
LIMIT 3;

-- Pagination: skip 5, take 5  (LIMIT offset, count)
SELECT sale_id, sale_date FROM sales ORDER BY sale_date LIMIT 5, 5;

-- NULLs sort FIRST in ascending order in MySQL; push them last like this:
SELECT sale_id, discount_pct FROM sales
ORDER BY discount_pct IS NULL, discount_pct, sale_id
LIMIT 8;

-- ---------------------------------------------------------------------
-- 7) Putting it all together
--    Logical order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT
--                   -> DISTINCT -> ORDER BY -> LIMIT
-- ---------------------------------------------------------------------
SELECT c.city,
       COUNT(DISTINCT s.customer_id) AS customers,
       ROUND(SUM(s.quantity * s.unit_price * (1 - IFNULL(s.discount_pct, 0) / 100)), 2) AS revenue
FROM sales s
JOIN customers c ON c.customer_id = s.customer_id
WHERE s.sale_date >= '2025-01-01'
GROUP BY c.city
HAVING revenue > 3000
ORDER BY revenue DESC
LIMIT 3;

-- Optional cleanup (Module 10 also uses this database):
-- DROP DATABASE IF EXISTS mysticml_sales;

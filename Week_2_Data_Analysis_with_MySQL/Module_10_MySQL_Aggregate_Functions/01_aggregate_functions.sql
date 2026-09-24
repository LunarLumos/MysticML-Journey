-- =====================================================================
-- MysticML Journey · Week 2 · Module 10 – MySQL Aggregate Functions
-- File: 01_aggregate_functions.sql
-- Covers: COUNT(), SUM(), AVG(), MIN(), MAX(), GROUP_CONCAT(), and
--         FIRST()/LAST() – which MySQL does NOT have – with their
--         equivalents: ORDER BY ... LIMIT 1, subqueries, and the window
--         functions FIRST_VALUE() / LAST_VALUE() / ROW_NUMBER().
-- Data:  the shared mysticml_sales dataset from Module 7.
-- Run (from this folder):
--   cat ../Module_7_MySQL_Clauses/sample_sales_dataset.sql 01_aggregate_functions.sql | mysql -u root -p
--   (or run sample_sales_dataset.sql once, then: mysql -u root -p < 01_aggregate_functions.sql)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_sales;
USE mysticml_sales;

-- A view with the revenue of each order line, reused throughout the file
CREATE OR REPLACE VIEW v_sales_lines AS
SELECT s.sale_id, s.sale_date, s.region, s.sales_rep, s.quantity, s.discount_pct,
       c.customer_name, c.city, c.segment,
       p.product_name, p.category,
       ROUND(s.quantity * s.unit_price * (1 - IFNULL(s.discount_pct, 0) / 100), 2) AS revenue
FROM sales s
JOIN customers c ON c.customer_id = s.customer_id
JOIN products  p ON p.product_id  = s.product_id;

-- ---------------------------------------------------------------------
-- 1) COUNT()
-- ---------------------------------------------------------------------
SELECT COUNT(*)                     AS all_rows,            -- counts rows, NULLs included
       COUNT(discount_pct)          AS rows_with_discount,  -- COUNT(col) skips NULLs
       COUNT(DISTINCT customer_id)  AS distinct_customers,
       COUNT(DISTINCT region)       AS distinct_regions
FROM sales;

-- Conditional count: SUM of a boolean (TRUE = 1)
SELECT SUM(discount_pct > 0) AS discounted_lines,
       COUNT(CASE WHEN quantity >= 5 THEN 1 END) AS bulk_lines
FROM sales;

-- ---------------------------------------------------------------------
-- 2) SUM()
-- ---------------------------------------------------------------------
SELECT SUM(quantity) AS units_sold,
       SUM(revenue)  AS total_revenue
FROM v_sales_lines;

SELECT category, SUM(quantity) AS units, SUM(revenue) AS revenue
FROM v_sales_lines
GROUP BY category
ORDER BY revenue DESC;

-- ---------------------------------------------------------------------
-- 3) AVG()  (NULLs are ignored – they are NOT treated as 0!)
-- ---------------------------------------------------------------------
SELECT ROUND(AVG(revenue), 2)              AS avg_line_revenue,
       ROUND(AVG(discount_pct), 2)         AS avg_known_discount,   -- over 20 non-NULL rows
       ROUND(AVG(IFNULL(discount_pct, 0)), 2) AS avg_discount_null_as_0  -- over all 24 rows
FROM v_sales_lines;

SELECT region, ROUND(AVG(revenue), 2) AS avg_order_value
FROM v_sales_lines
GROUP BY region
HAVING AVG(revenue) > 1000;

-- ---------------------------------------------------------------------
-- 4) MIN() and MAX()  (work on numbers, dates and strings)
-- ---------------------------------------------------------------------
SELECT MIN(revenue)   AS smallest_line,
       MAX(revenue)   AS largest_line,
       MIN(sale_date) AS first_sale_date,
       MAX(sale_date) AS last_sale_date,
       MIN(customer_name) AS alphabetically_first,
       DATEDIFF(MAX(sale_date), MIN(sale_date)) AS days_covered
FROM v_sales_lines;

-- All aggregates together, per sales rep
SELECT sales_rep,
       COUNT(*)               AS orders,
       SUM(revenue)           AS revenue,
       ROUND(AVG(revenue), 2) AS avg_order,
       MIN(revenue)           AS min_order,
       MAX(revenue)           AS max_order
FROM v_sales_lines
GROUP BY sales_rep
ORDER BY revenue DESC;

-- ---------------------------------------------------------------------
-- 5) GROUP_CONCAT() – join the values of a group into one string
-- ---------------------------------------------------------------------
SELECT region,
       GROUP_CONCAT(DISTINCT customer_name ORDER BY customer_name SEPARATOR ', ') AS customers
FROM v_sales_lines
GROUP BY region;

SELECT category,
       GROUP_CONCAT(product_name ORDER BY unit_price DESC) AS products_by_price
FROM products
GROUP BY category;

-- The result is truncated at group_concat_max_len bytes (default 1024):
SELECT @@group_concat_max_len AS group_concat_max_len;
-- SET SESSION group_concat_max_len = 100000;   -- raise it if you need longer lists

-- ---------------------------------------------------------------------
-- 6) FIRST() and LAST()
-- ---------------------------------------------------------------------
-- FIRST() / LAST() exist in MS Access (and some other tools) but NOT in MySQL:
--     SELECT FIRST(sale_date) FROM sales;   -- ERROR 1064 (syntax error near "(sale_date)")
-- "First" and "last" only mean something with an ORDER, so in MySQL we say
-- exactly which order we want:

-- 6a) Whole table: ORDER BY + LIMIT 1
SELECT sale_id, sale_date, customer_name, revenue       -- FIRST sale
FROM v_sales_lines ORDER BY sale_date ASC, sale_id ASC LIMIT 1;

SELECT sale_id, sale_date, customer_name, revenue       -- LAST sale
FROM v_sales_lines ORDER BY sale_date DESC, sale_id DESC LIMIT 1;

-- 6b) First value of a column (like FIRST(product_name)) via a subquery with MIN
SELECT product_name AS first_product_sold
FROM v_sales_lines
WHERE sale_date = (SELECT MIN(sale_date) FROM sales);

-- 6c) Per group with window functions (MySQL 8+):
--     FIRST_VALUE / LAST_VALUE over a window ordered by date.
--     ⚠ LAST_VALUE needs the frame to reach the END of the partition,
--       otherwise the default frame stops at the current row.
SELECT DISTINCT
       customer_name,
       FIRST_VALUE(product_name) OVER w AS first_product,
       LAST_VALUE(product_name)  OVER w AS last_product,
       FIRST_VALUE(sale_date)    OVER w AS first_purchase,
       LAST_VALUE(sale_date)     OVER w AS last_purchase
FROM v_sales_lines
WINDOW w AS (PARTITION BY customer_name
             ORDER BY sale_date, sale_id
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY customer_name;

-- Why the frame matters: LAST_VALUE with the DEFAULT frame just returns the current row
SELECT customer_name, sale_date, product_name,
       LAST_VALUE(product_name) OVER (PARTITION BY customer_name ORDER BY sale_date, sale_id)
           AS last_value_default_frame
FROM v_sales_lines
WHERE customer_name = 'Aadil Khan';

-- 6d) ROW_NUMBER(): keep the first (rn = 1) row of each group – the most
--     flexible "first per group" pattern (sort DESC for "last per group")
SELECT region, sale_id, sale_date, customer_name, revenue
FROM (
    SELECT v.*,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY sale_date DESC, sale_id DESC) AS rn
    FROM v_sales_lines v
) ranked
WHERE rn = 1
ORDER BY region;

-- ---------------------------------------------------------------------
-- 7) Aggregates as window functions (keep every row + a group total)
-- ---------------------------------------------------------------------
SELECT sale_id, region, revenue,
       SUM(revenue) OVER (PARTITION BY region)                         AS region_total,
       ROUND(100 * revenue / SUM(revenue) OVER (PARTITION BY region), 1) AS pct_of_region,
       SUM(revenue) OVER (PARTITION BY region ORDER BY sale_date, sale_id) AS running_total
FROM v_sales_lines
WHERE region = 'North'
ORDER BY sale_date;

-- Monthly summary report using every aggregate from this module
SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month,
       COUNT(*)                        AS orders,
       SUM(quantity)                   AS units,
       SUM(revenue)                    AS revenue,
       ROUND(AVG(revenue), 2)          AS avg_order,
       MIN(revenue)                    AS min_order,
       MAX(revenue)                    AS max_order,
       GROUP_CONCAT(DISTINCT category ORDER BY category) AS categories
FROM v_sales_lines
GROUP BY month WITH ROLLUP;

-- Optional cleanup (shared dataset; drop when you have finished Week 2):
-- DROP VIEW IF EXISTS v_sales_lines;
-- DROP DATABASE IF EXISTS mysticml_sales;

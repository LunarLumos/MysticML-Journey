# Module 7 – MySQL Clauses
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 6 – Queries & Constraints](../Module_6_MySQL_Queries_Constraints)  ·  Next ➡: [Module 8 – Control Flow](../Module_8_MySQL_Control_Flow_Functions)

## 🎯 Learning Objectives
- Filter rows (`WHERE`) and groups (`HAVING`) and know the difference.
- Summarise data with `GROUP BY`, remove duplicates with `DISTINCT`, sort with `ORDER BY`, page with `LIMIT`.
- Understand the logical order in which a `SELECT` is evaluated.

## ✅ Syllabus Checklist
- [x] MySQL WHERE | MySQL HAVING
- [x] MySQL DISTINCT | MySQL FROM
- [x] MySQL ORDER BY | MySQL GROUP BY

## 📖 Concepts

### Logical evaluation order
```
FROM / JOIN  →  WHERE  →  GROUP BY  →  HAVING  →  SELECT  →  DISTINCT  →  ORDER BY  →  LIMIT
```
That's why `WHERE` can't use aggregates (groups don't exist yet) but `HAVING` can. MySQL also lets `HAVING` and `ORDER BY` refer to `SELECT` aliases.

### Clause cheat-sheet
| Clause | Purpose | Example |
|--------|---------|---------|
| `FROM` | source: table, join, or subquery (derived table needs an alias) | `FROM sales s JOIN products p ON …` · `FROM (SELECT …) AS t` |
| `WHERE` | filter **rows** | `WHERE region = 'West' AND quantity >= 4` |
| `DISTINCT` | remove duplicate result rows | `SELECT DISTINCT region, sales_rep` · `COUNT(DISTINCT customer_id)` |
| `GROUP BY` | one row per group | `GROUP BY region` · `GROUP BY month, region` · `WITH ROLLUP` for totals |
| `HAVING` | filter **groups** | `HAVING SUM(amount) > 10000` |
| `ORDER BY` | sort (`ASC` default, `DESC`) | `ORDER BY category, unit_price DESC` |
| `LIMIT` | first *n* rows / paging | `LIMIT 3` · `LIMIT 5, 5` (skip 5, take 5) |

### WHERE operators
| Operator | Example |
|----------|---------|
| `=  <>  <  >  <=  >=` | `quantity >= 4` |
| `AND  OR  NOT` | `region = 'West' AND NOT quantity = 1` |
| `IN (...)` / `NOT IN` | `city IN ('Mumbai', 'Pune')` |
| `BETWEEN a AND b` (inclusive) | `sale_date BETWEEN '2025-02-01' AND '2025-02-28'` |
| `LIKE` (`%` any, `_` one char) | `product_name LIKE '%top%'` |
| `IS NULL` / `IS NOT NULL` | `discount_pct IS NULL` (never `= NULL`) |
| subquery | `customer_id NOT IN (SELECT customer_id FROM sales)` |

### WHERE vs HAVING
| | WHERE | HAVING |
|---|---|---|
| Filters | individual rows | groups |
| Runs | before `GROUP BY` | after `GROUP BY` |
| Aggregates allowed | ❌ | ✅ |

### Real results on the shared sales dataset
`GROUP BY region` with revenue = `quantity × unit_price × (1 − discount)`:

| region | orders | units | revenue |
|---|---|---|---|
| West | 10 | 36 | 13807.00 |
| South | 9 | 37 | 13078.00 |
| North | 5 | 9 | 3160.00 |

`GROUP BY category WITH ROLLUP`:

| category | units |
|---|---|
| Accessories | 18 |
| Electronics | 39 |
| Furniture | 25 |
| ALL CATEGORIES | 82 |

All clauses together (city revenue > 3000, top 3):

| city | customers | revenue |
|---|---|---|
| Bengaluru | 2 | 12438.00 |
| Pune | 1 | 8712.00 |
| Mumbai | 2 | 5095.00 |

## 🗃️ Shared sample dataset – `sample_sales_dataset.sql`
A small **synthetic** (hand-written) retail dataset in database **`mysticml_sales`**, also used by [Module 10](../Module_10_MySQL_Aggregate_Functions):

| Table | Rows | Columns |
|-------|------|---------|
| `customers` | 8 | customer_id, customer_name, city, segment, signup_date (Zara has no orders) |
| `products` | 8 | product_id, product_name, category, unit_price |
| `sales` | 24 | sale_id, sale_date (Jan–Apr 2025), customer_id, product_id, sales_rep, region, quantity, unit_price, discount_pct (4 NULLs) |

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `mysql_clauses.sql` | *Learner's original:* WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, DISTINCT on a `sales` table (DB `sales_management`) |
| `sample_sales_dataset.sql` | Creates/reloads the shared `mysticml_sales` dataset (re-runnable) |
| `02_clauses_complete.sql` | FROM (join, derived table), every WHERE operator, DISTINCT (incl. combos & `COUNT(DISTINCT)`), GROUP BY (multi-column, expression, `WITH ROLLUP`), HAVING, ORDER BY (multi-column, NULL ordering), LIMIT/paging, a combined query |

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_7_MySQL_Clauses
mysql -u root -p < sample_sales_dataset.sql          # once (re-run any time to reset)
mysql -u root -p -t < 02_clauses_complete.sql
# or together:
cat sample_sales_dataset.sql 02_clauses_complete.sql | mysql -u root -p -t
```
> Note: the MySQL 8.4+/9 command-line client ignores `SOURCE` in piped/batch mode unless started with `--commands`, which is why the dataset is loaded as a separate step.

## 🧠 Key Takeaways
- `WHERE` filters rows, `HAVING` filters groups.
- Every non-aggregated column in the `SELECT` must be in the `GROUP BY` (`ONLY_FULL_GROUP_BY` mode).
- Add a tie-breaker column to `ORDER BY` when you need a deterministic result (e.g. with `LIMIT`).
- `NULL` needs `IS NULL`; it sorts first in ascending order.

## 📝 Practice Exercises
1. List products that were never sold.
2. For each month, show the number of distinct customers who bought something.
3. Find sales reps whose **average** order quantity is above 3, sorted from highest to lowest.
4. Show page 3 of the sales list (5 rows per page) ordered by `sale_date`, `sale_id`.
5. Which city has the most customers in the `Consumer` segment?

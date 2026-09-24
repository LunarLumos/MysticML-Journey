# Module 10 – MySQL Aggregate Functions
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 9 – Joins](../Module_9_MySQL_Joins)  ·  Next ➡: [Week 3 – Data Analysis with Python](../../Week_3_Data_Analysis_with_Python)

## 🎯 Learning Objectives
- Summarise data with `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` and `GROUP_CONCAT`.
- Understand how aggregates treat `NULL`.
- Get the "first" and "last" row/value – MySQL has **no `FIRST()`/`LAST()`** – using `ORDER BY … LIMIT`, subqueries and window functions.

## ✅ Syllabus Checklist
- [x] MySQL count() | MySQL sum() | MySQL avg()
- [x] MySQL min() | MySQL max() | MySQL GROUP_CONCAT()
- [x] MySQL first() | MySQL last()  → equivalents (MySQL has no such functions)

## 📖 Concepts
An **aggregate function** turns many rows into one value – for the whole table, or per group with `GROUP BY`. All of them **ignore NULL** except `COUNT(*)`.

| Function | Returns | NULL handling | Example |
|----------|---------|---------------|---------|
| `COUNT(*)` | number of rows | counts every row | `COUNT(*)` |
| `COUNT(col)` | non-NULL values | skips NULL | `COUNT(discount_pct)` |
| `COUNT(DISTINCT col)` | distinct non-NULL values | skips NULL | `COUNT(DISTINCT customer_id)` |
| `SUM(col)` | total | skips NULL (all NULL → NULL) | `SUM(quantity)` |
| `AVG(col)` | mean $\bar{x} = \frac{1}{n}\sum x_i$ over **non-NULL** values | skips NULL | `AVG(revenue)` |
| `MIN(col)` / `MAX(col)` | smallest / largest (numbers, dates, strings) | skips NULL | `MAX(sale_date)` |
| `GROUP_CONCAT(col [ORDER BY …] [SEPARATOR …])` | values joined into one string | skips NULL | `GROUP_CONCAT(DISTINCT name ORDER BY name SEPARATOR ', ')` |

Handy tricks: `SUM(condition)` counts matches (TRUE = 1); `COUNT(CASE WHEN … THEN 1 END)` does the same; `GROUP_CONCAT` output is cut at `@@group_concat_max_len` (1024 bytes by default).

**AVG and NULL** – real output (20 of 24 rows have a discount value):

| avg_known_discount `AVG(discount_pct)` | avg_discount_null_as_0 `AVG(IFNULL(discount_pct,0))` |
|---|---|
| 5.53 | 4.60 |

Per sales rep (real output):

| sales_rep | orders | revenue | avg_order | min_order | max_order |
|---|---|---|---|---|---|
| Neha | 10 | 13807.00 | 1380.70 | 50.00 | 4212.00 |
| Arjun | 9 | 13078.00 | 1453.11 | 90.00 | 3600.00 |
| Kabir | 5 | 3160.00 | 632.00 | 75.00 | 1250.00 |

`GROUP_CONCAT` per region:

| region | customers |
|---|---|
| North | Sama Iqbal |
| South | Emily Carter, Giya Thomas, Priya Nair |
| West | Aadil Khan, Aayan Shaikh, Rohan Mehta |

### FIRST() and LAST() in MySQL
`FIRST()`/`LAST()` come from MS Access; in MySQL `SELECT FIRST(sale_date) FROM sales;` is a **syntax error (1064)**. Table rows have no built-in order, so "first" must always be defined by an `ORDER BY`:

| Need | MySQL equivalent |
|------|------------------|
| First / last row of a table | `ORDER BY sale_date, sale_id LIMIT 1` / `ORDER BY sale_date DESC, sale_id DESC LIMIT 1` |
| First / last value of a column | `MIN(sale_date)` / `MAX(sale_date)`, or `WHERE sale_date = (SELECT MIN(sale_date) FROM sales)` |
| First / last value **per group** | `FIRST_VALUE(x) OVER w` / `LAST_VALUE(x) OVER w` with `w AS (PARTITION BY g ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)` |
| Whole first / last row per group | `ROW_NUMBER() OVER (PARTITION BY g ORDER BY d [DESC]) AS rn` … `WHERE rn = 1` |

⚠ `LAST_VALUE` with the default frame (`RANGE … CURRENT ROW`) just returns the current row – you must extend the frame to `UNBOUNDED FOLLOWING`.

Real output – each customer's first and last product:

| customer_name | first_product | last_product | first_purchase | last_purchase |
|---|---|---|---|---|
| Aadil Khan | Laptop Pro 14 | Tablet Mini | 2025-01-03 | 2025-04-06 |
| Emily Carter | Smartphone X | Office Chair | 2025-01-05 | 2025-03-14 |
| Sama Iqbal | Wireless Mouse | Laptop Pro 14 | 2025-01-08 | 2025-04-11 |
| … | | | | |

### Aggregates as window functions
`SUM(revenue) OVER (PARTITION BY region)` keeps every row **and** shows the group total – used for "% of total" and running totals (`… ORDER BY sale_date`).

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `01_aggregate_functions.sql` | A revenue view over the shared dataset; COUNT variants, SUM, AVG with NULLs, MIN/MAX on numbers/dates/strings, GROUP_CONCAT options, FIRST/LAST equivalents (LIMIT, subquery, FIRST_VALUE/LAST_VALUE, ROW_NUMBER), window aggregates, a monthly `WITH ROLLUP` report |

Data: the **synthetic** `mysticml_sales` dataset from [Module 7](../Module_7_MySQL_Clauses/sample_sales_dataset.sql).

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_10_MySQL_Aggregate_Functions
cat ../Module_7_MySQL_Clauses/sample_sales_dataset.sql 01_aggregate_functions.sql | mysql -u root -p -t
# or, if the dataset is already loaded:
mysql -u root -p -t < 01_aggregate_functions.sql
```

## 🧠 Key Takeaways
- `COUNT(*)` counts rows; `COUNT(col)` counts non-NULL values – they differ when NULLs exist.
- `AVG` divides by the number of **non-NULL** values; use `IFNULL(col, 0)` if NULL should mean 0.
- "First/last" only exist relative to an `ORDER BY`; use `LIMIT`, `MIN/MAX` or window functions.
- Window functions add group statistics without collapsing rows – the bridge to pandas `groupby().transform()` in Week 3.

## 📝 Practice Exercises
1. For each product category, show number of orders, total units, and the list of products sold (`GROUP_CONCAT`).
2. Which customer has the highest average order value? (Only customers with ≥ 3 orders.)
3. For each region, show the **first** sale's customer and the **last** sale's product using window functions.
4. Compute each sale's share (%) of its customer's total spend.
5. What is the median order revenue? (Hint: `ROW_NUMBER()` and `COUNT(*) OVER ()`.)

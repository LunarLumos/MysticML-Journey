# Module 4 – Tables & Views
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 3 – Database](../Module_3_MySQL_Database)  ·  Next ➡: [Module 5 – Keys](../Module_5_MySQL_Keys)

## 🎯 Learning Objectives
- Create, inspect, alter, rename, copy, empty and drop tables.
- Create, query, redefine and drop **views**, and update data through them.

## ✅ Syllabus Checklist
- [x] Create Table | Alter Table – Add/Delete/Modify Column in Table
- [x] Show Tables | Rename Table | TRUNCATE Table | Describe Table | DROP Table | Copy Table
- [x] MySQL Views – Create | Update | Drop | Select Views

## 📖 Concepts

### Table statements
| Task | Statement |
|------|-----------|
| Create | `CREATE TABLE t (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL);` |
| List | `SHOW TABLES;` · views too: `SHOW FULL TABLES;` |
| Describe | `DESCRIBE t;` (= `SHOW COLUMNS FROM t;`) · `SHOW CREATE TABLE t;` |
| Add column | `ALTER TABLE t ADD COLUMN email VARCHAR(100) AFTER name;` |
| Modify column | `ALTER TABLE t MODIFY COLUMN name VARCHAR(100) NOT NULL;` |
| Rename + modify | `ALTER TABLE t CHANGE COLUMN salary monthly_salary DECIMAL(12,2);` |
| Rename column | `ALTER TABLE t RENAME COLUMN department TO dept;` |
| Delete column | `ALTER TABLE t DROP COLUMN email;` |
| Rename table | `RENAME TABLE t TO t2;` |
| Copy table | `CREATE TABLE t2 LIKE t; INSERT INTO t2 SELECT * FROM t;` or `CREATE TABLE t2 AS SELECT * FROM t;` |
| Empty table | `TRUNCATE TABLE t;` |
| Remove table | `DROP TABLE IF EXISTS t;` |

**DELETE vs TRUNCATE vs DROP**

| | `DELETE FROM t` | `TRUNCATE TABLE t` | `DROP TABLE t` |
|---|---|---|---|
| Removes | chosen rows (`WHERE`) | all rows | rows **and** structure |
| Speed | row by row (slow on big tables) | very fast | very fast |
| `AUTO_INCREMENT` | kept | reset to 1 | gone |
| Fires triggers / can roll back | yes | no | no |

### Views
A **view** is a stored `SELECT` with a name. It holds no data of its own; querying it re-runs the query, so it is always up to date.
Uses: simplify complex joins, hide columns (security), give analysts a stable interface.

| Task | Statement |
|------|-----------|
| Create | `CREATE VIEW v_it AS SELECT emp_id, emp_name FROM staff WHERE dept = 'IT';` |
| Select | `SELECT * FROM v_it;` |
| Update definition | `CREATE OR REPLACE VIEW v_it AS …;` or `ALTER VIEW v_it AS …;` |
| Protect inserts/updates | `… WITH CHECK OPTION` |
| Update data through it | `UPDATE v_it SET salary = salary * 1.1 WHERE …;` (simple views only) |
| Show definition | `SHOW CREATE VIEW v_it;` |
| Drop | `DROP VIEW IF EXISTS v_it;` |

A view is **updatable** only if each row maps to exactly one base-table row (no `GROUP BY`, `DISTINCT`, aggregates, `UNION`, …).

Real output of `SELECT * FROM v_dept_summary;` after adding Rohan to IT:

| dept | headcount | avg_salary |
|---|---|---|
| HR | 1 | 50000.00 |
| IT | 4 | 65875.00 |
| Finance | 1 | 58000.00 |

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `tables_views.sql` | *Learner's original:* create `employees`, add a column, insert, create & query an HR view (needs a `USE <db>;` first) |
| `02_tables_views_complete.sql` | Every table operation (ADD / MODIFY / CHANGE / RENAME / DROP column, rename, 3 ways to copy, TRUNCATE, DROP) and the full view lifecycle incl. `CREATE OR REPLACE`, `ALTER VIEW … WITH CHECK OPTION`, updating through a view (DB `mysticml_tables_views`) |

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_4_Tables_Views
mysql -u root -p -t < 02_tables_views_complete.sql
```

## 🧠 Key Takeaways
- `ALTER TABLE` changes structure without losing data; `MODIFY` keeps the name, `CHANGE` renames too.
- `CREATE TABLE … LIKE` copies structure and indexes; `… AS SELECT` does not copy keys.
- Views are saved queries: always current, and a good way to hide complexity.

## 📝 Practice Exercises
1. Add a `bonus DECIMAL(8,2) DEFAULT 0` column to `staff`, then move it right after `monthly_salary`.
2. Create a view `v_payroll` with name, dept and `monthly_salary * 12 AS annual_salary`. Is it updatable? Try it.
3. Make a filtered copy of `staff` containing only people earning over 60 000.
4. Show the difference between `DELETE FROM` and `TRUNCATE` by checking the next `AUTO_INCREMENT` value after each (`SHOW TABLE STATUS LIKE 'staff';`).

# Module 6 – MySQL Queries & Constraints
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 5 – Keys](../Module_5_MySQL_Keys)  ·  Next ➡: [Module 7 – Clauses](../Module_7_MySQL_Clauses)

## 🎯 Learning Objectives
- Write the core DML/DDL queries: SELECT, INSERT, UPDATE, DELETE, ALTER, TRUNCATE, DROP, REPLACE.
- Copy data between tables with `INSERT INTO … SELECT`.
- Enforce data quality with constraints: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT.

## ✅ Syllabus Checklist
- [x] Select | Insert | Update | Delete | Alter | Truncate | Drop | Replace Queries
- [x] Insert Into Select Query
- [x] Exploring different MySQL constraints

## 📖 Concepts

### Queries
| Query | Syntax | Note |
|-------|--------|------|
| SELECT | `SELECT col1, col2 FROM t WHERE … ORDER BY …;` | read data |
| INSERT | `INSERT INTO t (a, b) VALUES (1, 'x'), (2, 'y');` | omitted columns get their DEFAULT |
| UPDATE | `UPDATE t SET a = a + 1 WHERE id = 3;` | ⚠ no `WHERE` = every row |
| DELETE | `DELETE FROM t WHERE status = 'left';` | ⚠ no `WHERE` = every row |
| ALTER | `ALTER TABLE t ADD COLUMN phone VARCHAR(20);` | change structure |
| TRUNCATE | `TRUNCATE TABLE t;` | empty table, reset AUTO_INCREMENT |
| DROP | `DROP TABLE t;` | remove table |
| REPLACE | `REPLACE INTO t (id, a) VALUES (5, 'x');` | if PK/UNIQUE exists: **delete old row, insert new** |
| INSERT … SELECT | `INSERT INTO t2 (a, b) SELECT a, b FROM t WHERE …;` | copy query results |

**Upsert options compared**

| Statement | On duplicate key |
|-----------|------------------|
| `INSERT` | error 1062 |
| `INSERT IGNORE` | row skipped, warning only |
| `REPLACE` | old row deleted, new inserted (unlisted columns reset to DEFAULT, new trigger events) |
| `INSERT … AS new ON DUPLICATE KEY UPDATE col = new.col` | existing row updated in place (keeps its id) |

### Constraints
| Constraint | Guarantees | Example |
|------------|-----------|---------|
| `NOT NULL` | a value is always present | `emp_name VARCHAR(100) NOT NULL` |
| `UNIQUE` | no duplicates | `CONSTRAINT uq_email UNIQUE (email)` |
| `PRIMARY KEY` | NOT NULL + UNIQUE row identifier | `CONSTRAINT pk_emp PRIMARY KEY (emp_id)` |
| `FOREIGN KEY` | value exists in parent table | `FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL` |
| `CHECK` | a boolean rule holds (enforced since 8.0.16) | `CONSTRAINT chk_age CHECK (age BETWEEN 18 AND 70)` |
| `DEFAULT` | value used when none is given | `status VARCHAR(10) DEFAULT 'active'`, `joined_on DATE DEFAULT (CURRENT_DATE)` |
| `AUTO_INCREMENT` | automatic sequence number | `emp_id INT AUTO_INCREMENT` |

Real errors raised by the violations in `02_queries_constraints_complete.sql`:

| Violated | Error |
|----------|-------|
| NOT NULL | `ERROR 1048: Column 'emp_name' cannot be null` |
| UNIQUE | `ERROR 1062: Duplicate entry 'IT' for key 'departments.dept_name'` |
| CHECK | `ERROR 3819: Check constraint 'chk_emp_age' is violated.` |
| FOREIGN KEY | `ERROR 1452: Cannot add or update a child row: a foreign key constraint fails` |

`INSERT INTO high_earners … SELECT … WHERE salary >= 60000` result:

| emp_id | emp_name | dept_name | salary |
|---|---|---|---|
| 1 | Aadil | IT | 99999.00 |
| 4 | Rohan | Finance | 82000.00 |
| 3 | Sama | IT | 78750.00 |
| 2 | Emily | HR | 60000.00 |

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `mysql_queries_constraints.sql` | *Learner's original:* employees / projects / assignments with PK, NOT NULL, UNIQUE, CHECK, DEFAULT, FK; inserts and a 3-table join (DB `company_management`) |
| `02_queries_constraints_complete.sql` | All constraints (named), commented violation examples, every query type incl. `REPLACE`, `INSERT IGNORE`, `ON DUPLICATE KEY UPDATE`, `INSERT INTO … SELECT`, `ON DELETE SET NULL`, `ALTER … DROP CHECK` (DB `mysticml_queries`) |

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_6_MySQL_Queries_Constraints
mysql -u root -p -t < 02_queries_constraints_complete.sql
```

## 🧠 Key Takeaways
- Constraints push data-quality rules into the database, so every app obeys them.
- `REPLACE` is *delete + insert* – prefer `ON DUPLICATE KEY UPDATE` when you want to keep the row.
- `INSERT INTO … SELECT` is the fastest way to build summary / archive tables.
- Test `UPDATE`/`DELETE` with the same `WHERE` in a `SELECT` first.

## 📝 Practice Exercises
1. Add a CHECK so `salary` must be at least 20 000, then try to violate it.
2. Create `employee_archive` and move (copy then delete) every employee whose `dept_id` is NULL.
3. Use `ON DUPLICATE KEY UPDATE` to increment a `login_count` column for an existing email.
4. Explain why `REPLACE INTO employees (emp_id, emp_name, email) VALUES (1, 'Aadil', 'aadil@example.com')` would reset Aadil's salary.

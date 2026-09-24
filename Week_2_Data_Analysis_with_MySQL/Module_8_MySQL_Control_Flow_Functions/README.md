# Module 8 – MySQL Control Flow Functions & Conditions
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 7 – Clauses](../Module_7_MySQL_Clauses)  ·  Next ➡: [Module 9 – Joins](../Module_9_MySQL_Joins)

## 🎯 Learning Objectives
- Add if/else logic to queries with `IF()`, `CASE`, `IFNULL()`, `NULLIF()`, `COALESCE()`.
- Write the `IF … ELSEIF … ELSE … END IF` **statement** inside a stored procedure using `DELIMITER`.
- Combine conditions correctly and handle `NULL`'s three-valued logic.

## ✅ Syllabus Checklist
- [x] MySQL IF() | MySQL IFNULL()
- [x] MySQL NULLIF() | MySQL CASE
- [x] MySQL IF Statement
- [x] MySQL Conditions

## 📖 Concepts

### Control-flow functions (usable anywhere an expression is allowed)
| Function | Returns | Example → result |
|----------|---------|------------------|
| `IF(cond, a, b)` | `a` if cond is TRUE, else `b` (also when cond is NULL!) | `IF(92 >= 40, 'Pass', 'Fail')` → `Pass` |
| `IFNULL(x, y)` | `x`, or `y` when `x` is NULL | `IFNULL(NULL, 0)` → `0` |
| `COALESCE(a, b, c…)` | first non-NULL argument | `COALESCE(NULL, NULL, 7)` → `7` |
| `NULLIF(a, b)` | NULL if `a = b`, else `a` | `NULLIF(5, 5)` → `NULL` · `x / NULLIF(y, 0)` avoids ÷0 |
| `CASE WHEN c1 THEN r1 WHEN c2 THEN r2 ELSE r END` | first matching branch (searched CASE) | grade bands |
| `CASE expr WHEN v1 THEN r1 … END` | compare one value (simple CASE) | `CASE subject WHEN 'SQL' THEN 'Databases' END` |

Real output from `02_control_flow_complete.sql` — note how a naive `IF` treats an absent (NULL) score as a fail:

| student | subject | score | result (`IF(score>=40,…)`) | result_fixed (nested IF) | grade (CASE) |
|---|---|---|---|---|---|
| Aadil | SQL | 92 | Pass | Pass | A |
| Emily | Python | NULL | Fail | Absent | Absent |
| Sama | SQL | 39 | Fail | Fail | F |
| Rohan | SQL | 55 | Pass | Pass | D |

`NULLIF` against a data-entry error (`max_score = 0`): `score / NULLIF(max_score, 0)` returns `NULL` for Rohan instead of a division-by-zero problem.

### IF *function* vs IF *statement*
| | `IF()` function | `IF … END IF` statement |
|---|---|---|
| Where | inside any query | only in stored procedures / functions / triggers |
| Returns | a value | runs statements |
| Branches | 2 (nest for more) | `IF … ELSEIF … ELSE … END IF` |

```sql
DELIMITER //                         -- so the ; inside the body doesn't end CREATE PROCEDURE
CREATE PROCEDURE classify_student(IN p_student VARCHAR(50), OUT p_label VARCHAR(40))
BEGIN
    DECLARE v_avg DECIMAL(5,2);
    SELECT AVG(score) INTO v_avg FROM exam_results WHERE student = p_student;
    IF v_avg IS NULL THEN      SET p_label = 'No results';
    ELSEIF v_avg >= 80 THEN    SET p_label = 'Distinction';
    ELSEIF v_avg >= 50 THEN    SET p_label = 'Pass';
    ELSE                       SET p_label = 'Needs support';
    END IF;
END //
DELIMITER ;

CALL classify_student('Aadil', @label);  SELECT @label;   -- Distinction
```

### Conditions
| Operator | Meaning |
|----------|---------|
| `AND`, `OR`, `NOT`, `XOR` | logic (`AND` binds tighter than `OR` → use parentheses) |
| `IN`, `BETWEEN`, `LIKE` | set, range, pattern |
| `IS NULL`, `IS NOT NULL`, `<=>` | NULL tests (`<=>` = NULL-safe equals) |
| `EXISTS (subquery)` | TRUE if the subquery returns any row |

**Three-valued logic:** any comparison with NULL is *UNKNOWN* (shown as NULL) — `NULL = NULL` → NULL, `NULL IS NULL` → 1, `NULL <=> NULL` → 1. `WHERE` keeps only TRUE rows.

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `mysql_control_flow_functions.sql` | *Learner's original:* `IF()`, `CASE`, `IFNULL()`, `NULLIF()` on an `orders` table and a combined report (DB `control_flow_demo`) |
| `02_control_flow_complete.sql` | Nested `IF`, `IF` inside `SUM`, `IFNULL` vs `COALESCE`, `NULLIF` for ÷0, searched & simple `CASE` (in SELECT, ORDER BY, UPDATE), IF statement in a procedure, CASE statement in a function, all condition operators and NULL logic (DB `mysticml_control_flow`) |

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_8_MySQL_Control_Flow_Functions
mysql -u root -p -t < 02_control_flow_complete.sql
```
(`DELIMITER` is a *client* command – it works in the `mysql` CLI and Workbench, not in most programming-language drivers.)

## 🧠 Key Takeaways
- `CASE` is standard SQL and the most flexible; `IF()` is a MySQL shortcut for two branches.
- Think about NULL in every condition: `IF(NULL > 40, …)` goes to the *else* branch.
- `NULLIF(x, 0)` is the idiomatic guard against division by zero.
- Stored-program `IF` statements need `DELIMITER` when created from the CLI.

## 📝 Practice Exercises
1. Using the `mysticml_sales` dataset, label each sale `'Big'` (≥ 2000), `'Medium'` (≥ 500) or `'Small'` with `CASE`.
2. Show discount as text: `'No discount'` for 0, `'Unknown'` for NULL, otherwise e.g. `'10.00%'`.
3. Write a procedure `apply_bonus(IN p_student VARCHAR(50))` that adds 5 bonus points only if the student's average is below 60.
4. Explain the output of `SELECT NULL <> 5, NOT NULL, NULL OR 1, NULL AND 0;`.

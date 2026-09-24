# Module 9 – MySQL Joins
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 8 – Control Flow](../Module_8_MySQL_Control_Flow_Functions)  ·  Next ➡: [Module 10 – Aggregate Functions](../Module_10_MySQL_Aggregate_Functions)

## 🎯 Learning Objectives
- Combine tables with INNER, LEFT, RIGHT, CROSS and SELF joins (and emulate FULL OUTER JOIN).
- Find "missing" rows with an anti-join.
- Change data across tables with **UPDATE JOIN** and **DELETE JOIN**.

## ✅ Syllabus Checklist
- [x] MySQL Inner Join | MySQL Left Join | MySQL Right Join
- [x] MySQL CROSS JOIN - MySQL SELF JOIN - MySQL DELETE JOIN - MySQL Update Join

## 📖 Concepts

### Join types
```
 INNER JOIN        LEFT JOIN         RIGHT JOIN        FULL (LEFT ∪ RIGHT)
  A ( ▓ ) B        ( ▓▓▓ ) B          A ( ▓▓▓ )        ( ▓▓▓▓▓ )
 matches only     all A + matches    all B + matches   everything
```
| Join | Returns | Syntax |
|------|---------|--------|
| `INNER JOIN` (or just `JOIN`) | rows matching in both tables | `FROM e JOIN d ON d.dept_id = e.dept_id` |
| `LEFT JOIN` | all left rows; NULLs where no match | `FROM e LEFT JOIN d ON …` |
| `RIGHT JOIN` | all right rows; NULLs where no match | `FROM e RIGHT JOIN d ON …` |
| FULL OUTER (emulated) | all rows from both | `… LEFT JOIN … UNION … RIGHT JOIN …` |
| `CROSS JOIN` | every combination (rows A × rows B) | `FROM e CROSS JOIN shifts` |
| SELF JOIN | a table joined to itself via two aliases | `FROM employees e LEFT JOIN employees m ON m.emp_id = e.manager_id` |
| Anti-join | left rows with **no** match | `LEFT JOIN … WHERE right.id IS NULL` |
| `USING (col)` | shorthand when the column name is identical | `JOIN departments USING (dept_id)` |

### UPDATE JOIN and DELETE JOIN (MySQL multi-table syntax)
```sql
-- 10% raise for staff in departments with a budget >= 200k
UPDATE employees e
JOIN departments d ON d.dept_id = e.dept_id
SET e.salary = ROUND(e.salary * 1.10)
WHERE d.budget_k >= 200;

-- delete assignments of inactive employees (only the alias after DELETE loses rows)
DELETE pa
FROM project_assignments pa
JOIN employees e ON e.emp_id = pa.emp_id
WHERE e.is_active = FALSE;

-- delete from two tables at once
DELETE p, pa FROM projects p LEFT JOIN project_assignments pa ON pa.project_id = p.project_id
WHERE p.dept_id = 30;
```

### Real results from `02_joins_complete.sql`
Sample data: 7 employees (Zara has no department), 4 departments (Legal has no staff).

SELF JOIN (employee → manager):

| employee | manager |
|---|---|
| Aadil | (top) |
| Emily | Aadil |
| Sama | Emily |
| Rohan | Aadil |
| Giya | Rohan |
| Aayan | Aadil |
| Zara | Aadil |

Three-table LEFT JOIN + `GROUP_CONCAT`:

| project_name | owner_dept | people | total_hours | team |
|---|---|---|---|---|
| Recommendation Engine | Engineering | 3 | 80 | Aadil,Emily,Sama |
| Brand Campaign | Marketing | 2 | 50 | Giya,Rohan |
| Budget Forecast | Finance | 1 | 25 | Aayan |
| Data Platform | - | 1 | 20 | Sama |
| Office Relocation | Legal | 0 | NULL | NULL |

UPDATE JOIN (budget ≥ 200k gets +10 %): Aadil 120000 → 132000, Rohan 80000 → 88000, Aayan (Finance, 150k) unchanged at 75000.

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `mysql_joins.sql` | *Learner's original:* students/grades with INNER, LEFT, RIGHT, FULL (UNION), CROSS and SELF joins (DB `join_demo`) |
| `02_joins_complete.sql` | Employees/departments/projects schema; all join types, `USING`, anti-join, manager hierarchy self-join, 3-table join with aggregation, UPDATE JOIN (inner & left), DELETE JOIN (one table, two tables, anti-join) (DB `mysticml_joins`) |

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_9_MySQL_Joins
mysql -u root -p -t < 02_joins_complete.sql
```

## 🧠 Key Takeaways
- Choose the join by asking "which rows must **always** appear?" – both (INNER), left (LEFT), right (RIGHT).
- A condition on the right table in `WHERE` turns a LEFT JOIN into an INNER JOIN; put it in `ON` instead if you want to keep unmatched rows.
- CROSS JOIN multiplies rows – great for generating combinations, dangerous by accident.
- Run the `SELECT` version of an UPDATE/DELETE JOIN first to see which rows will change.

## 📝 Practice Exercises
1. List each department with its number of **active** employees, including departments with zero.
2. Using a self join, find employees who share a manager with Sama.
3. Write an UPDATE JOIN that moves every project owned by Marketing to Engineering.
4. With the `mysticml_sales` dataset, list customers who never bought a Furniture product.

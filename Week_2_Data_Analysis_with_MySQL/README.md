# Week 2 – Data Analysis with MySQL
> 6 Weeks Machine Learning – Zero to Hero   |   ⬅ [Week 1 – Python Programming](../Week_1_Python_Programming)  ·  ➡ [Week 3 – Data Analysis with Python](../Week_3_Data_Analysis_with_Python)

Most real-world data used in machine learning lives in **relational databases**. This week teaches you to store, organise, secure and — most importantly — **query and summarise** data with MySQL, the SQL skills every data scientist uses before a single line of pandas or scikit-learn.

## 📚 Modules
| # | Module | What you'll learn |
|---|--------|-------------------|
| 1 | [Introduction to MySQL](Module_1_Introduction_to_MySQL) | Installation, uses, architecture & features, datatypes, `@variables`, connecting from the CLI and Python |
| 2 | [User Management](Module_2_MySQL_User_Management) | `CREATE USER`, `GRANT`/`REVOKE`, `SHOW GRANTS`, listing users, changing passwords, roles, `DROP USER` |
| 3 | [MySQL Database](Module_3_MySQL_Database) | Create / show / select / alter / drop databases, copying a database (`mysqldump` vs SQL) |
| 4 | [Tables & Views](Module_4_Tables_Views) | Create / alter / rename / copy / truncate / drop tables; create, query, update and drop views |
| 5 | [MySQL Keys](Module_5_MySQL_Keys) | Unique, primary, composite and foreign keys, `ON DELETE CASCADE` |
| 6 | [Queries & Constraints](Module_6_MySQL_Queries_Constraints) | SELECT / INSERT / UPDATE / DELETE / REPLACE, `INSERT INTO … SELECT`, NOT NULL / UNIQUE / CHECK / DEFAULT / PK / FK |
| 7 | [MySQL Clauses](Module_7_MySQL_Clauses) | FROM, WHERE, DISTINCT, GROUP BY, HAVING, ORDER BY, LIMIT – plus the **shared sales dataset** |
| 8 | [Control Flow & Conditions](Module_8_MySQL_Control_Flow_Functions) | `IF()`, `IFNULL()`, `NULLIF()`, `CASE`, the IF statement in a stored procedure, NULL logic |
| 9 | [MySQL Joins](Module_9_MySQL_Joins) | Inner, left, right, cross, self joins, FULL OUTER emulation, UPDATE JOIN, DELETE JOIN |
| 10 | [Aggregate Functions](Module_10_MySQL_Aggregate_Functions) | COUNT, SUM, AVG, MIN, MAX, GROUP_CONCAT, and FIRST/LAST equivalents with window functions |

Each module folder contains the learner's original practice script plus a comprehensive companion script (`02_*_complete.sql`; Module 10: `01_aggregate_functions.sql`) and a README with concept notes, syntax tables and real example results.

## 🧰 Prerequisites
- Week 1 Python basics (for `mysql_connection.py`).
- No prior SQL knowledge needed.

## ⚙️ Setup
1. **Install MySQL 8.0+** (all scripts were tested on MySQL 9.6):
   - macOS: `brew install mysql && brew services start mysql`
   - Ubuntu: `sudo apt install mysql-server && sudo systemctl start mysql`
   - Windows: MySQL Installer from <https://dev.mysql.com/downloads/installer/>
2. Secure it: `mysql_secure_installation` (set a root password).
3. Optional GUI: MySQL Workbench, DBeaver, or VS Code + SQLTools.
4. For the Python demo: `pip install mysql-connector-python`.

## ▶️ Running the scripts
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_4_Tables_Views
mysql -u root -p -t < 02_tables_views_complete.sql     # -t = table-formatted output
```
- Every companion script creates its own database named **`mysticml_<topic>`** with `CREATE DATABASE IF NOT EXISTS`, so it is safe to re-run, and ends with a commented-out `DROP DATABASE` line for cleanup.
- Modules 7 and 10 share the **synthetic** `mysticml_sales` dataset: load it with `mysql -u root -p < Module_7_MySQL_Clauses/sample_sales_dataset.sql`.
- The learner's original scripts use other database names (`my_database`, `school_management`, `company_management`, `sales_management`, `control_flow_demo`, `join_demo`) and some lack `IF NOT EXISTS`, so they error on a second run – drop the database first or run them once.
- ⚠️ Module 2 scripts create and drop **server accounts** – run them only on your own practice server.

Clean up everything from this week:
```sql
DROP DATABASE IF EXISTS mysticml_intro;      DROP DATABASE IF EXISTS mysticml_db_demo;
DROP DATABASE IF EXISTS mysticml_tables_views; DROP DATABASE IF EXISTS mysticml_keys;
DROP DATABASE IF EXISTS mysticml_queries;    DROP DATABASE IF EXISTS mysticml_sales;
DROP DATABASE IF EXISTS mysticml_control_flow; DROP DATABASE IF EXISTS mysticml_joins;
DROP DATABASE IF EXISTS mysticml_user_mgmt;
```

## 🔗 How this connects to Week 3
In Week 3 you'll do the same kinds of analysis in Python: `WHERE` ↔ boolean indexing, `GROUP BY` + aggregates ↔ `df.groupby().agg()`, joins ↔ `pd.merge()`, window functions ↔ `groupby().transform()`. You can even load a MySQL query straight into pandas:
```python
import pandas as pd, mysql.connector
conn = mysql.connector.connect(user="root", password="...", database="mysticml_sales")
df = pd.read_sql("SELECT * FROM sales", conn)
```

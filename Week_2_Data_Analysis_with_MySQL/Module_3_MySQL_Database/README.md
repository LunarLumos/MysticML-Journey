# Module 3 – MySQL Database
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 2 – User Management](../Module_2_MySQL_User_Management)  ·  Next ➡: [Module 4 – Tables & Views](../Module_4_Tables_Views)

## 🎯 Learning Objectives
- Create, list, select, inspect, alter and drop databases.
- Back up and **copy** a database with `mysqldump`, or table-by-table in pure SQL.
- Know which copy method keeps keys and indexes.

## ✅ Syllabus Checklist
- [x] Create Database | Select | Show Database
- [x] Drop | Copy Database

## 📖 Concepts
A **database** (also called a **schema** in MySQL) is a named container of tables, views, procedures, etc. One MySQL server hosts many databases.

### Syntax cheat-sheet
| Task | Statement |
|------|-----------|
| Create | `CREATE DATABASE IF NOT EXISTS shop CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;` |
| List | `SHOW DATABASES;` · `SHOW DATABASES LIKE 'mysticml%';` |
| Inspect DDL | `SHOW CREATE DATABASE shop;` |
| Select (make current) | `USE shop;` · check with `SELECT DATABASE();` |
| Query without USE | `SELECT * FROM shop.orders;` |
| Change defaults | `ALTER DATABASE shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;` |
| Drop (irreversible!) | `DROP DATABASE IF EXISTS shop;` |
| Size in MB | `SELECT table_schema, SUM(data_length+index_length)/1024/1024 FROM information_schema.tables GROUP BY table_schema;` |

`utf8mb4` = full Unicode (incl. emoji). Collation `_ai_ci` = accent- and case-insensitive comparisons.

### Copying a database
MySQL has **no `COPY DATABASE` statement**. Options:

| Method | Command | Keeps keys / indexes / FKs? |
|--------|---------|-----------------------------|
| `mysqldump` + restore (terminal) | `mysqldump -u root -p shop > shop.sql` then `mysql -u root -p shop_copy < shop.sql` | ✅ everything (add `--routines --triggers` for procedures/triggers) |
| One-line pipe | `mysqldump -u root -p shop \| mysql -u root -p shop_copy` | ✅ |
| `CREATE TABLE … LIKE` + `INSERT … SELECT` (SQL) | `CREATE TABLE copy.t LIKE shop.t; INSERT INTO copy.t SELECT * FROM shop.t;` | ✅ structure + indexes (per table) |
| `CREATE TABLE … AS SELECT` (SQL) | `CREATE TABLE copy.t AS SELECT * FROM shop.t;` | ❌ data & column types only |

Real result from `02_database_operations_complete.sql` — `courses` was copied with `LIKE`, `enrollments` with `AS SELECT`:

| TABLE_NAME | COLUMN_NAME | COLUMN_KEY | EXTRA |
|---|---|---|---|
| courses | course_id | PRI | auto_increment |
| enrollments | course_id | | |
| enrollments | enrollment_id | | |

The `AS SELECT` copy lost its primary key and `AUTO_INCREMENT`.

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `mysql_database.sql` | *Learner's original:* `SHOW DATABASES`, `mysqldump` backup/restore commands (terminal-only, kept as comments), database sizes |
| `02_database_operations_complete.sql` | Create with charset, `SHOW DATABASES [LIKE]`, `information_schema.schemata`, `SHOW CREATE DATABASE`, `USE`, `ALTER DATABASE`, copying a database two ways with a key comparison, sizes, `DROP DATABASE` (DBs `mysticml_db_demo`, `mysticml_db_copy`) |

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_3_MySQL_Database
mysql -u root -p -t < 02_database_operations_complete.sql
# try a real dump-based copy (terminal):
mysqldump -u root -p mysticml_db_demo > mysticml_db_demo.sql
mysql -u root -p -e "CREATE DATABASE mysticml_db_clone"
mysql -u root -p mysticml_db_clone < mysticml_db_demo.sql
```

## 🧠 Key Takeaways
- Always use `IF NOT EXISTS` / `IF EXISTS` in scripts so they can be re-run.
- `USE` changes the default database; `db.table` works from anywhere.
- `mysqldump` is the reliable way to back up or copy a database.
- `DROP DATABASE` cannot be undone – back up first.

## 📝 Practice Exercises
1. Create `mysticml_library` with `utf8mb4`, then check its collation in `information_schema.schemata`.
2. Dump only the **structure** of `mysticml_db_demo` (`--no-data`) and open the file – what statements does it contain?
3. Copy `mysticml_db_demo.enrollments` so that the copy keeps its primary key.
4. Write a query that lists every `mysticml_%` database with its number of tables.

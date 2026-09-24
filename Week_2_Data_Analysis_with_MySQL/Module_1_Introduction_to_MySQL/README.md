# Module 1 – Introduction to MySQL
> Week 2 · Data Analysis with MySQL   |   Next ➡: [Module 2 – User Management](../Module_2_MySQL_User_Management)

## 🎯 Learning Objectives
- Install MySQL and connect to it from the terminal and from Python.
- Explain what MySQL is used for and how its client/server architecture works.
- Choose the right **datatype** for each column.
- Use **user-defined variables** (`@x`) and read **system variables** (`@@x`).

## ✅ Syllabus Checklist
- [x] MySQL Installation and Introduction
- [x] Use of MySQL
- [x] Working of MySQL | Features
- [x] MySQL Datatypes | Variables
- [x] MySQL Connection

## 📖 Concepts

### Installation
| OS | Command |
|----|---------|
| macOS (Homebrew) | `brew install mysql` → `brew services start mysql` → `mysql_secure_installation` |
| Ubuntu / Debian | `sudo apt install mysql-server` → `sudo systemctl start mysql` → `sudo mysql_secure_installation` |
| Windows | Download the **MySQL Installer** from dev.mysql.com (includes Server + Workbench + Shell) |

Check it works: `mysql --version` and `mysql -u root -p -e "SELECT VERSION();"`.
A GUI such as **MySQL Workbench**, DBeaver or the VS Code "SQLTools" extension is optional but handy.

### What is MySQL and where is it used?
MySQL is an open-source **relational database management system (RDBMS)**: data is stored in **tables** (rows × columns) that can be related to each other through keys, and queried with **SQL** (Structured Query Language).
Typical uses: back-end of web apps (WordPress, e-commerce), analytics/reporting, logging, and as the data source for data-science and ML pipelines (Week 3 reads SQL data into pandas).

### How MySQL works
```
 ┌──────────────┐   SQL over TCP 3306   ┌────────────────────────── mysqld (server) ──────────────────────────┐
 │ client        │ ────────────────────▶ │ connection & auth → parser → optimizer → executor → storage engine │
 │ mysql CLI,    │ ◀──────────────────── │                                               (InnoDB by default)   │
 │ Workbench,    │     result rows        └─────────────────────────────────────────────────────────┬──────────┘
 │ Python app    │                                                                                    ▼
 └──────────────┘                                                                            data files on disk
```
1. The **client** opens a connection and authenticates (`user@host` + password).
2. The server **parses** the SQL, the **optimizer** picks an execution plan (which index, which join order).
3. The **storage engine** (InnoDB) reads/writes the data, handling transactions and locking.

**Key features:** open source, ACID transactions (InnoDB), foreign keys, indexes, views, stored procedures, triggers, window functions & CTEs (8.0+), JSON type, replication, fine-grained user privileges, cross-platform.

### Datatypes (cheat-sheet)
| Family | Type | Stores | Example |
|--------|------|--------|---------|
| Integer | `TINYINT`, `SMALLINT`, `INT`, `BIGINT` | whole numbers (1, 2, 4, 8 bytes); `UNSIGNED` doubles the positive range | `age TINYINT UNSIGNED` |
| Boolean | `BOOLEAN` = `TINYINT(1)` | 0 / 1 | `is_active BOOLEAN` |
| Exact decimal | `DECIMAL(p, s)` | exact numbers – **use for money** | `price DECIMAL(10,2)` |
| Floating point | `FLOAT`, `DOUBLE` | approximate numbers (science, ML features) | `ratio DOUBLE` |
| Fixed string | `CHAR(n)` | always n chars | `country CHAR(2)` |
| Variable string | `VARCHAR(n)` | up to n chars | `name VARCHAR(100)` |
| Long text | `TEXT`, `MEDIUMTEXT`, `LONGTEXT` | articles, comments | `bio TEXT` |
| List | `ENUM(...)` / `SET(...)` | one / several values from a fixed list | `size ENUM('S','M','L')` |
| Binary | `BLOB` | bytes (images, files) | `avatar BLOB` |
| Date/time | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, `YEAR` | `'2025-01-31'`, `'09:30:00'` … | `created_at DATETIME DEFAULT CURRENT_TIMESTAMP` |
| Document | `JSON` | validated JSON | `profile->>'$.level'` |

Why `DECIMAL` for money — real output from `02_datatypes_variables_complete.sql`:

| decimal_math (`1499.99 * 3`) | float_math (`FLOAT 0.1 + 0.2`) | double_math (`DOUBLE 0.1 + 0.2`) |
|---|---|---|
| 4499.97 | 0.30000000149011613 | 0.30000000000000004 |

### Variables
| Kind | Syntax | Scope |
|------|--------|-------|
| User-defined | `SET @tax = 0.18;` · `SELECT @max := MAX(price) FROM t;` · `SELECT COUNT(*) INTO @n FROM t;` | current connection (session) |
| System | `SELECT @@version, @@port;` · `SHOW VARIABLES LIKE 'max_connections';` · `SET SESSION sql_select_limit = 1;` | global or session |
| Local | `DECLARE v INT DEFAULT 0;` | inside a stored procedure/function only (see Module 8) |

An unset `@variable` is simply `NULL`.

### Connecting
| From | How |
|------|-----|
| Terminal | `mysql -u root -p` · `mysql -h 127.0.0.1 -P 3306 -u root -p mydb` · `mysql -u root -p < script.sql` |
| Inside the client | `STATUS;` (connection info), `USE db;`, `EXIT;` |
| Python | `mysql.connector.connect(host=..., user=..., password=...)` – see `mysql_connection.py` |

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `introduction_to_mysql.sql` | *Learner's original:* create a database and a `students` table, insert rows, `OPTIMIZE TABLE`, `SELECT` (uses `my_database`) |
| `02_datatypes_variables_complete.sql` | Server info & storage engines, a table with every major datatype, `DECIMAL` vs `FLOAT`, `CAST`, user variables (`@x`, `:=`, `SELECT … INTO`), system variables, CLI connection notes (DB `mysticml_intro`) |
| `mysql_connection.py` | Connect from Python with `mysql-connector-python`, credentials from env vars, parameterised queries, dict cursor, friendly message if the server is down |

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_1_Introduction_to_MySQL
mysql -u root -p < 02_datatypes_variables_complete.sql      # add -t for table-style output

pip install mysql-connector-python
export MYSQL_USER=root MYSQL_PASSWORD='your-password'        # optional; defaults: root / empty
python mysql_connection.py
```
Sample output of `mysql_connection.py`:
```
Connected to MySQL 9.6.0 at 127.0.0.1:3306 as 'root'
Inserted 3 rows

Week 2 learners:
  Aadil    91.50
  Emily    88.00

3 learners, average score 86.25

Dropped demo database 'mysticml_intro_py'.
Connection closed.
```
If no server is running you get: `Could not reach a MySQL server at 127.0.0.1:3306.` and the script exits cleanly.

## 🧠 Key Takeaways
- MySQL is a client/server RDBMS; SQL is the language, InnoDB is the default engine.
- Pick the **smallest correct type**; money → `DECIMAL`, never `FLOAT`.
- `@var` = session variable, `@@var` = server setting, `DECLARE` = inside procedures only.
- Never hard-code passwords in code; read them from environment variables, and always use `%s` placeholders.

## 📝 Practice Exercises
1. Create a table `movies` with suitable types for title, release year, rating (0–10, one decimal), genre (from a fixed list) and a JSON column for cast.
2. Store the average rating in `@avg` with `SELECT … INTO`, then list movies above `@avg`.
3. Run `SHOW VARIABLES LIKE 'character_set%';` and explain what `utf8mb4` means.
4. Extend `mysql_connection.py` to read `MYSQL_DB` from the environment and print all table names in that database.

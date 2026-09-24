"""
Module 2 · Script 05 – Reading Data from Databases
==================================================

To keep this runnable offline we use SQLite, which ships with Python
(`sqlite3` module) and can live entirely in memory. The exact same pandas
functions (`pd.read_sql_query`, `DataFrame.to_sql`) work with MySQL –
see the commented MySQL section at the bottom (it connects to the
databases you built in Week 2).
"""

import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "employees.csv"


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def build_database() -> sqlite3.Connection:
    """Create an in-memory SQLite database and load the CSV into a table."""
    section("1️⃣  Create an in-memory SQLite database")
    conn = sqlite3.connect(":memory:")
    employees = pd.read_csv(DATA_FILE)
    employees.to_sql("employees", conn, index=False)  # DataFrame -> SQL table
    print(f"Table 'employees' created with {len(employees)} rows.")

    # A second table so we can demonstrate a JOIN.
    departments = pd.DataFrame({
        "department": ["Engineering", "Marketing", "HR", "Finance", "Sales"],
        "floor": [3, 2, 1, 4, 2],
        "head": ["Meera", "Dev", "Lilith", "Arjun", "Farhan"],
    })
    departments.to_sql("departments", conn, index=False)
    print("Table 'departments' created.")
    return conn


def query_database(conn: sqlite3.Connection) -> None:
    """Run SQL queries and get DataFrames back."""
    section("2️⃣  pd.read_sql_query – SELECT *")
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    print(df.head())

    section("3️⃣  Filtering & aggregating in SQL")
    sql = """
        SELECT department,
               COUNT(*)              AS headcount,
               ROUND(AVG(salary), 0) AS avg_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC
    """
    print(pd.read_sql_query(sql, conn))

    section("4️⃣  Parameterised query (safe from SQL injection)")
    city = "Mumbai"
    df_city = pd.read_sql_query(
        "SELECT name, department, salary FROM employees WHERE city = ?",
        conn, params=(city,))
    print(f"Employees in {city}:\n", df_city)

    section("5️⃣  JOIN two tables")
    joined = pd.read_sql_query("""
        SELECT e.name, e.department, d.floor, d.head
        FROM employees e
        JOIN departments d ON e.department = d.department
        WHERE e.salary > 70000
    """, conn)
    print(joined)


# ---------------------------------------------------------------------------
# 🐬 MySQL variant (optional – needs a running MySQL server)
# ---------------------------------------------------------------------------
# pip install sqlalchemy mysql-connector-python
#
# from sqlalchemy import create_engine
#
# # mysql+mysqlconnector://<user>:<password>@<host>:<port>/<database>
# # Uses the Week 2 Module 9 database `join_demo` (table `students`).
# engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/join_demo")
# df = pd.read_sql("SELECT * FROM students", engine)      # read a query
# df.to_sql("students_copy", engine, if_exists="replace", index=False)  # write back
#
# # Without SQLAlchemy (plain connector – pandas will show a warning but works):
# import mysql.connector
# conn = mysql.connector.connect(host="localhost", user="root",
#                                password="password", database="join_demo")
# df = pd.read_sql("SELECT * FROM students", conn)
# conn.close()
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    connection = build_database()
    try:
        query_database(connection)
    finally:
        connection.close()
        print("\nConnection closed.")

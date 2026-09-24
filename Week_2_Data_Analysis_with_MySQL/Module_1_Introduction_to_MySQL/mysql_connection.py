"""
MysticML Journey - Week 2 - Module 1: Connecting to MySQL from Python
=====================================================================

Shows how a Python program talks to a MySQL server using the official
driver, ``mysql-connector-python``:

    pip install mysql-connector-python

Credentials are NEVER hard-coded. They are read from environment variables
(with safe defaults for a local learning setup):

    MYSQL_HOST      (default: 127.0.0.1)
    MYSQL_PORT      (default: 3306)
    MYSQL_USER      (default: root)
    MYSQL_PASSWORD  (default: empty)

Example (macOS / Linux):
    export MYSQL_PASSWORD='my-secret'
    python mysql_connection.py

If the server is not running / not reachable, the script prints a friendly
message and exits without a traceback.
"""

import os
import sys

# ------------------------------------------------------------
# Import the driver (with a helpful message if it's missing)
# ------------------------------------------------------------
try:
    import mysql.connector
    from mysql.connector import Error, errorcode
except ImportError:  # pragma: no cover - depends on the environment
    print("mysql-connector-python is not installed.")
    print("Install it with:  pip install mysql-connector-python")
    sys.exit(1)

DEMO_DB = "mysticml_intro_py"


def get_config() -> dict:
    """Build the connection settings from environment variables."""
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "connection_timeout": 5,  # seconds - fail fast if the server is down
    }


def connect():
    """Open a connection, or return None with a friendly explanation."""
    config = get_config()
    try:
        conn = mysql.connector.connect(**config)
        print(f"Connected to MySQL {conn.server_info} "
              f"at {config['host']}:{config['port']} as '{config['user']}'")
        return conn
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: check MYSQL_USER / MYSQL_PASSWORD.")
        elif err.errno in (2003, 2005, 2013):  # can't connect / unknown host / lost
            print(f"Could not reach a MySQL server at "
                  f"{config['host']}:{config['port']}.")
            print("Is MySQL running? (macOS: 'brew services start mysql', "
                  "Linux: 'sudo systemctl start mysql')")
        else:
            print(f"MySQL error {err.errno}: {err.msg}")
        return None


def run_demo(conn) -> None:
    """Create a tiny table, insert rows safely, query them, then clean up."""
    cursor = conn.cursor()

    # 1) Create and select a demo database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DEMO_DB}")
    cursor.execute(f"USE {DEMO_DB}")

    # 2) Create a table
    cursor.execute("DROP TABLE IF EXISTS learners")
    cursor.execute("""
        CREATE TABLE learners (
            id    INT AUTO_INCREMENT PRIMARY KEY,
            name  VARCHAR(100) NOT NULL,
            week  TINYINT NOT NULL,
            score DECIMAL(5, 2)
        )
    """)

    # 3) Insert with PLACEHOLDERS (%s) - never build SQL with f-strings from
    #    user input; placeholders protect against SQL injection.
    rows = [("Aadil", 2, 91.5), ("Emily", 2, 88.0), ("Sama", 1, 79.25)]
    cursor.executemany(
        "INSERT INTO learners (name, week, score) VALUES (%s, %s, %s)", rows
    )
    conn.commit()  # InnoDB is transactional: commit to make the inserts permanent
    print(f"Inserted {cursor.rowcount} rows")

    # 4) Parameterised SELECT
    cursor.execute(
        "SELECT name, score FROM learners WHERE week = %s ORDER BY score DESC",
        (2,),
    )
    print("\nWeek 2 learners:")
    for name, score in cursor.fetchall():
        print(f"  {name:<8} {score}")

    # 5) Dictionary cursor: rows come back as dicts
    dict_cursor = conn.cursor(dictionary=True)
    dict_cursor.execute("SELECT COUNT(*) AS n, AVG(score) AS avg_score FROM learners")
    stats = dict_cursor.fetchone()
    print(f"\n{stats['n']} learners, average score {float(stats['avg_score']):.2f}")
    dict_cursor.close()

    # 6) Clean up the demo database so the server stays tidy
    cursor.execute(f"DROP DATABASE IF EXISTS {DEMO_DB}")
    cursor.close()
    print(f"\nDropped demo database '{DEMO_DB}'.")


def main() -> int:
    """Entry point: connect, run the demo, always close the connection."""
    conn = connect()
    if conn is None:
        return 0  # graceful exit - nothing else to do without a server
    try:
        run_demo(conn)
    finally:
        conn.close()
        print("Connection closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

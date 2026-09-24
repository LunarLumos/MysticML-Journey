-- =====================================================================
-- MysticML Journey · Week 2 · Module 1 – Introduction to MySQL
-- File: 02_datatypes_variables_complete.sql
-- Covers: server info / "working of MySQL", every major datatype family,
--         user-defined variables (@x), session/system variables,
--         and how to connect (CLI notes at the bottom).
-- Run:   mysql -u root -p < 02_datatypes_variables_complete.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_intro;
USE mysticml_intro;

-- ---------------------------------------------------------------------
-- 1) Who / where am I?  (Working of MySQL: client -> server -> storage engine)
-- ---------------------------------------------------------------------
SELECT VERSION()      AS server_version,   -- the mysqld server version
       CURRENT_USER() AS connected_as,     -- account the server authenticated
       DATABASE()     AS current_database, -- set by USE
       NOW()          AS server_time;

-- Which storage engines does this server support? (InnoDB is the default)
SELECT ENGINE, SUPPORT, TRANSACTIONS
FROM information_schema.ENGINES
WHERE SUPPORT IN ('YES', 'DEFAULT');

-- ---------------------------------------------------------------------
-- 2) DATATYPES – one table that uses a column of each common type
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS datatype_showcase;
CREATE TABLE datatype_showcase (
    -- Numeric (integers)
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, -- 0 .. 4,294,967,295
    tiny_flag     TINYINT,            -- -128 .. 127  (BOOLEAN is an alias of TINYINT(1))
    is_active     BOOLEAN DEFAULT TRUE,
    small_count   SMALLINT,           -- -32,768 .. 32,767
    big_counter   BIGINT,             -- ~ ±9.22e18
    -- Numeric (fixed / floating point)
    price         DECIMAL(10, 2),     -- exact: 10 digits, 2 after the point (use for money)
    ratio         FLOAT,              -- approximate, 4 bytes
    precise_ratio DOUBLE,             -- approximate, 8 bytes
    -- Strings
    country_code  CHAR(2),            -- fixed length (padded)
    full_name     VARCHAR(100),       -- variable length, up to 100 chars
    bio           TEXT,               -- long text (up to 64 KB)
    size          ENUM('S', 'M', 'L', 'XL'),     -- exactly one of a list
    tags          SET('ml', 'sql', 'python'),    -- zero or more of a list
    avatar        BLOB,               -- binary data
    -- Date & time
    birth_date    DATE,               -- 'YYYY-MM-DD'
    login_time    TIME,               -- 'HH:MM:SS'
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,  -- date + time
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- stored in UTC
    grad_year     YEAR,
    -- JSON (MySQL 5.7+)
    profile       JSON
);

INSERT INTO datatype_showcase
    (tiny_flag, small_count, big_counter, price, ratio, precise_ratio,
     country_code, full_name, bio, size, tags, avatar,
     birth_date, login_time, grad_year, profile)
VALUES
    (1, 120, 9000000000, 1499.99, 0.1, 0.1,
     'IN', 'Aadil', 'Learning ML from zero to hero', 'M', 'ml,sql', NULL,
     '2002-04-15', '09:30:00', 2024, '{"level": "beginner", "skills": ["python", "sql"]}'),
    (0, 45, 42, 0.50, 3.14159, 3.14159265358979,
     'US', 'Emily', NULL, 'S', 'python', NULL,
     '2001-11-02', '18:05:30', 2023, '{"level": "intermediate"}');

SELECT id, full_name, price, size, tags, birth_date, grad_year,
       profile->>'$.level' AS level     -- ->> extracts a JSON value as text
FROM datatype_showcase;

-- DESCRIBE shows how MySQL stored each column's type
DESCRIBE datatype_showcase;

-- DECIMAL is exact, FLOAT is approximate: see the difference
SELECT price * 3        AS decimal_math,   -- 4499.97 exactly
       ratio + 0.2      AS float_math,     -- 0.30000000149011613 (binary rounding!)
       precise_ratio + 0.2 AS double_math
FROM datatype_showcase WHERE id = 1;

-- CAST / CONVERT between types
SELECT CAST('2025-01-31' AS DATE)      AS str_to_date,
       CAST(12.7 AS SIGNED)            AS decimal_to_int,  -- rounds -> 13
       CONVERT(2025, CHAR)             AS int_to_string;

-- ---------------------------------------------------------------------
-- 3) VARIABLES
-- ---------------------------------------------------------------------
-- 3a) User-defined (session) variables start with @ and live until you disconnect.
SET @course      = 'MysticML';
SET @week        = 2;
SET @tax_rate    = 0.18;

SELECT @course AS course, @week AS week, @tax_rate AS tax_rate;

-- Assign inside a SELECT with := (the := form is required inside SELECT)
SELECT @max_price := MAX(price) FROM datatype_showcase;
SELECT @max_price AS most_expensive,
       ROUND(@max_price * (1 + @tax_rate), 2) AS with_tax;

-- SELECT ... INTO assigns query results to variables
SELECT COUNT(*), AVG(price) INTO @rows, @avg_price FROM datatype_showcase;
SELECT @rows AS total_rows, ROUND(@avg_price, 2) AS avg_price;

-- Use a variable in a WHERE clause
SET @wanted_size = 'M';
SELECT full_name, size FROM datatype_showcase WHERE size = @wanted_size;

-- An unset variable is simply NULL
SELECT @never_set AS unset_variable;

-- 3b) System variables (configured by the server), prefixed with @@
SELECT @@version            AS version,
       @@port               AS port,
       @@autocommit         AS autocommit,
       @@sql_mode           AS sql_mode;

SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'character_set_server';

-- Session-scoped change (affects only this connection)
SET SESSION sql_select_limit = 1;
SELECT full_name FROM datatype_showcase;    -- only 1 row comes back
SET SESSION sql_select_limit = DEFAULT;

-- (Local variables declared with DECLARE exist only inside stored
--  programs; see Module 8's stored-procedure example.)

-- ---------------------------------------------------------------------
-- 4) MySQL CONNECTION (run these in a terminal, not inside mysql)
-- ---------------------------------------------------------------------
--   mysql -u root -p                          -- local server, prompts for password
--   mysql -h 127.0.0.1 -P 3306 -u root -p     -- explicit host and port
--   mysql -u root -p mysticml_intro           -- connect straight into a database
--   mysql -u root -p -e "SHOW DATABASES;"     -- run one statement and exit
--   mysql -u root -p < script.sql             -- run a whole script file
-- Inside the client:  STATUS;  (or \s) shows connection details, EXIT; quits.
-- From Python, see mysql_connection.py in this folder.

-- Optional cleanup:
-- DROP DATABASE IF EXISTS mysticml_intro;

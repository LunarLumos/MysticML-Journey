-- =====================================================================
-- MysticML Journey · Week 2 · Module 3 – MySQL Database
-- File: 02_database_operations_complete.sql
-- Covers: CREATE DATABASE (with charset), SHOW DATABASES, SELECT/USE a
--         database, SHOW CREATE DATABASE, ALTER DATABASE, COPY a database
--         (pure-SQL approach) and DROP DATABASE.
-- Run:   mysql -u root -p < 02_database_operations_complete.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1) CREATE DATABASE
-- ---------------------------------------------------------------------
-- IF NOT EXISTS avoids an error when the database is already there.
-- utf8mb4 stores every Unicode character (including emoji).
CREATE DATABASE IF NOT EXISTS mysticml_db_demo
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;     -- ai = accent-insensitive, ci = case-insensitive

-- CREATE SCHEMA is an exact synonym of CREATE DATABASE in MySQL.

-- ---------------------------------------------------------------------
-- 2) SHOW DATABASES
-- ---------------------------------------------------------------------
SHOW DATABASES;
SHOW DATABASES LIKE 'mysticml%';            -- pattern filter

-- The same information from the data dictionary (can be filtered/sorted):
SELECT schema_name, default_character_set_name, default_collation_name
FROM information_schema.schemata
WHERE schema_name LIKE 'mysticml%';

SHOW CREATE DATABASE mysticml_db_demo;      -- the exact DDL used

-- ---------------------------------------------------------------------
-- 3) SELECT (USE) A DATABASE
-- ---------------------------------------------------------------------
USE mysticml_db_demo;
SELECT DATABASE() AS currently_selected;

-- Put some data in it so we have something to copy
-- (drop the child table first: enrollments references courses)
DROP TABLE IF EXISTS enrollments, courses;
CREATE TABLE courses (
    course_id   INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    weeks       TINYINT NOT NULL
);
INSERT INTO courses (course_name, weeks) VALUES
('Python Programming', 1), ('Data Analysis with MySQL', 1), ('Machine Learning', 2);

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    learner       VARCHAR(50) NOT NULL,
    course_id     INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
INSERT INTO enrollments (learner, course_id) VALUES ('Aadil', 1), ('Aadil', 2), ('Emily', 3);

-- You can also query a table in another database without USE: db.table
SELECT * FROM mysticml_db_demo.courses;

-- ---------------------------------------------------------------------
-- 4) ALTER DATABASE (change default charset/collation for new tables)
-- ---------------------------------------------------------------------
ALTER DATABASE mysticml_db_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 5) COPY A DATABASE
-- ---------------------------------------------------------------------
-- MySQL has NO "COPY DATABASE" statement. Two approaches:
--
-- (A) mysqldump  – the standard way (run in a TERMINAL, not in mysql):
--       mysqldump -u root -p mysticml_db_demo > mysticml_db_demo.sql
--       mysql     -u root -p -e "CREATE DATABASE mysticml_db_copy"
--       mysql     -u root -p mysticml_db_copy < mysticml_db_demo.sql
--     Or in one line with a pipe:
--       mysqldump -u root -p mysticml_db_demo | mysql -u root -p mysticml_db_copy
--     Useful flags: --routines (procedures/functions), --triggers,
--                   --no-data (structure only), --databases db1 db2 (several DBs)
--     mysqldump copies EVERYTHING: indexes, keys, foreign keys, data.
--
-- (B) Pure SQL, table by table (what we do below):
--       CREATE TABLE new_db.t LIKE old_db.t;          -- exact structure + indexes
--       INSERT INTO new_db.t SELECT * FROM old_db.t;  -- the data
--     or the one-step shortcut
--       CREATE TABLE new_db.t AS SELECT * FROM old_db.t;
--     ⚠ CREATE TABLE ... SELECT copies columns & data but NOT the primary
--       key, AUTO_INCREMENT, indexes or foreign keys. Use LIKE + INSERT
--       when you need a faithful copy.

CREATE DATABASE IF NOT EXISTS mysticml_db_copy;

-- B1) Faithful copy: structure (LIKE) then data
DROP TABLE IF EXISTS mysticml_db_copy.courses;
CREATE TABLE mysticml_db_copy.courses LIKE mysticml_db_demo.courses;
INSERT INTO mysticml_db_copy.courses SELECT * FROM mysticml_db_demo.courses;

-- B2) Quick copy with CREATE TABLE ... SELECT (no keys copied!)
DROP TABLE IF EXISTS mysticml_db_copy.enrollments;
CREATE TABLE mysticml_db_copy.enrollments AS
SELECT * FROM mysticml_db_demo.enrollments;

-- Compare: the LIKE copy kept the PRIMARY KEY, the AS SELECT copy did not
SELECT table_name, column_name, column_key, extra
FROM information_schema.columns
WHERE table_schema = 'mysticml_db_copy' AND column_name IN ('course_id', 'enrollment_id')
ORDER BY table_name;

-- Row counts match between original and copy
SELECT 'original' AS db, (SELECT COUNT(*) FROM mysticml_db_demo.courses) AS courses,
       (SELECT COUNT(*) FROM mysticml_db_demo.enrollments) AS enrollments
UNION ALL
SELECT 'copy', (SELECT COUNT(*) FROM mysticml_db_copy.courses),
       (SELECT COUNT(*) FROM mysticml_db_copy.enrollments);

-- Size of our databases (MB)
SELECT table_schema AS db_name,
       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM information_schema.tables
WHERE table_schema LIKE 'mysticml_db%'
GROUP BY table_schema;

-- ---------------------------------------------------------------------
-- 6) DROP DATABASE  (permanently deletes the DB and ALL its tables!)
-- ---------------------------------------------------------------------
DROP DATABASE IF EXISTS mysticml_db_copy;
SHOW DATABASES LIKE 'mysticml_db%';

-- Optional cleanup:
-- DROP DATABASE IF EXISTS mysticml_db_demo;

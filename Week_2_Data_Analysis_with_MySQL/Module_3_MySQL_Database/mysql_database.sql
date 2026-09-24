-- =====================================================================
-- MysticML Journey · Week 2 · Module 3 – MySQL Database
-- Original practice file (learner's own work). The fuller companion
-- script in this folder is 02_*_complete.sql – see README.md.
-- Note: mysqldump / mysql lines are TERMINAL commands (commented out below) – run them in a shell, not inside mysql.
-- =====================================================================

-- Lists all the databases on the MySQL server.
SHOW DATABASES;

-- Backup a specific database ('my_database') to a file.
-- mysqldump -u root -p my_database > backup.sql

-- Restore the backup file into the 'my_database' database on the server.
-- mysql -u root -p my_database < backup.sql

-- Displays the size of each database on the server.
SELECT table_schema AS 'Database',
       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
GROUP BY table_schema;

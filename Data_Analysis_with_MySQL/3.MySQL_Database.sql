-- Lists all the databases on the MySQL server.
SHOW DATABASES;

--Backup a specific database ('my_database') to a file.
mysqldump -u root -p my_database > backup.sql

--Backuped  specific database ('my_database') to server.
mysql -u root -p my_database < backup.sql

-- Displays the size of each database on the server.
SELECT table_schema AS 'Database',
       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
GROUP BY table_schema;

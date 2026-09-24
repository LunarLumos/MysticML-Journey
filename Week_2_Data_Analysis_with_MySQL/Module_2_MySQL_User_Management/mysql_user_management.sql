-- =====================================================================
-- MysticML Journey · Week 2 · Module 2 – MySQL User Management
-- Original practice file (learner's own work). The fuller companion
-- script in this folder is 02_*_complete.sql – see README.md.
-- Note: Changes server-wide accounts – run only on your own practice server as an admin.
-- =====================================================================

-- Query to list all users and their allowed host connections.
SELECT user, host FROM mysql.user;

-- Create a new user named 'Aadil' with a password.
CREATE USER 'Aadil'@'localhost' IDENTIFIED BY 'password123';

-- Grant all privileges on the 'my_database' database to 'Aadil'.
GRANT ALL PRIVILEGES ON my_database.* TO 'Aadil'@'localhost';

-- Query to list all users who can connect only from localhost.
SELECT user, host FROM mysql.user WHERE host = 'localhost';

-- Check the privileges assigned to 'Aadil'.
SHOW GRANTS FOR 'Aadil'@'localhost';

-- Revoke the SELECT privilege from 'Aadil'.
REVOKE SELECT ON my_database.* FROM 'Aadil'@'localhost';

-- Query to list users along with their authentication details and plugins.
SELECT user, host, authentication_string, plugin FROM mysql.user;

-- Remove the user 'Aadil' from the MySQL server.
DROP USER 'Aadil'@'localhost';

-- Query to list all users and their allowed host connections.
SELECT user, host FROM mysql.user;

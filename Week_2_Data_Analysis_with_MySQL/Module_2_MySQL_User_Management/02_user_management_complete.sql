-- =====================================================================
-- MysticML Journey · Week 2 · Module 2 – MySQL User Management
-- File: 02_user_management_complete.sql
-- Covers: CREATE USER, GRANT, SHOW GRANTS, list users (mysql.user),
--         change password (ALTER USER), REVOKE, roles, DROP USER.
--
-- !! These statements change SERVER-WIDE accounts. Run them only on your
-- !! own local practice server, while connected as an admin (e.g. root):
--        mysql -u root -p < 02_user_management_complete.sql
-- !! The script cleans up after itself (drops the demo users/role).
-- =====================================================================

-- A demo database for the new users to work in
CREATE DATABASE IF NOT EXISTS mysticml_user_mgmt;
USE mysticml_user_mgmt;

DROP TABLE IF EXISTS reports;
CREATE TABLE reports (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);
INSERT INTO reports (title) VALUES ('Q1 revenue'), ('Q2 revenue');

-- ---------------------------------------------------------------------
-- 1) SHOW ALL USERS
-- ---------------------------------------------------------------------
-- Accounts live in the system table mysql.user. An account = 'user'@'host'.
SELECT user, host, plugin, account_locked
FROM mysql.user
ORDER BY user;

-- Who am I right now?
SELECT USER() AS login_as, CURRENT_USER() AS authenticated_as;

-- ---------------------------------------------------------------------
-- 2) CREATE USER
-- ---------------------------------------------------------------------
-- 'localhost' = can connect only from this machine; '%' = from any host.
CREATE USER IF NOT EXISTS 'mystic_analyst'@'localhost'
    IDENTIFIED BY 'Analyst#2025';

CREATE USER IF NOT EXISTS 'mystic_dev'@'%'
    IDENTIFIED BY 'Dev#2025'
    PASSWORD EXPIRE INTERVAL 90 DAY        -- force a change every 90 days
    FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 1;  -- lock 1 day after 3 bad logins

-- ---------------------------------------------------------------------
-- 3) GRANT PRIVILEGES
-- ---------------------------------------------------------------------
-- Syntax: GRANT <privileges> ON <db>.<table> TO 'user'@'host';
-- Read-only analyst on one database:
GRANT SELECT ON mysticml_user_mgmt.* TO 'mystic_analyst'@'localhost';

-- Developer: data changes + DDL on one database
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, INDEX
    ON mysticml_user_mgmt.* TO 'mystic_dev'@'%';

-- Column-level privilege: only the `title` column of one table
GRANT UPDATE (title) ON mysticml_user_mgmt.reports TO 'mystic_analyst'@'localhost';

-- (ALL PRIVILEGES ON *.* ... WITH GRANT OPTION would make a super-admin –
--  avoid that for normal users: principle of least privilege.)

-- ---------------------------------------------------------------------
-- 4) SHOW GRANTS – what can a user do?
-- ---------------------------------------------------------------------
SHOW GRANTS FOR 'mystic_analyst'@'localhost';
SHOW GRANTS FOR 'mystic_dev'@'%';
SHOW GRANTS;                              -- your own privileges

-- ---------------------------------------------------------------------
-- 5) ROLES (MySQL 8+) – a named bundle of privileges
-- ---------------------------------------------------------------------
CREATE ROLE IF NOT EXISTS 'mystic_readonly';
GRANT SELECT ON mysticml_user_mgmt.* TO 'mystic_readonly';
GRANT 'mystic_readonly' TO 'mystic_dev'@'%';
SET DEFAULT ROLE 'mystic_readonly' TO 'mystic_dev'@'%';
SHOW GRANTS FOR 'mystic_dev'@'%' USING 'mystic_readonly';

-- ---------------------------------------------------------------------
-- 6) CHANGE USER PASSWORD
-- ---------------------------------------------------------------------
ALTER USER 'mystic_analyst'@'localhost' IDENTIFIED BY 'NewAnalyst#2025';
-- A logged-in user can change their own password with:
--   ALTER USER USER() IDENTIFIED BY 'new_password';
-- Lock / unlock an account without dropping it:
ALTER USER 'mystic_dev'@'%' ACCOUNT LOCK;
ALTER USER 'mystic_dev'@'%' ACCOUNT UNLOCK;

-- Rename an account
RENAME USER 'mystic_analyst'@'localhost' TO 'mystic_reader'@'localhost';

-- ---------------------------------------------------------------------
-- 7) REVOKE – take privileges back
-- ---------------------------------------------------------------------
REVOKE DROP, ALTER ON mysticml_user_mgmt.* FROM 'mystic_dev'@'%';
REVOKE UPDATE (title) ON mysticml_user_mgmt.reports FROM 'mystic_reader'@'localhost';
SHOW GRANTS FOR 'mystic_dev'@'%';

-- List only our demo accounts
SELECT user, host, account_locked, password_lifetime
FROM mysql.user
WHERE user LIKE 'mystic%';

-- ---------------------------------------------------------------------
-- 8) DROP USER / DROP ROLE (cleanup)
-- ---------------------------------------------------------------------
DROP USER IF EXISTS 'mystic_reader'@'localhost';
DROP USER IF EXISTS 'mystic_dev'@'%';
DROP ROLE IF EXISTS 'mystic_readonly';

SELECT user, host FROM mysql.user WHERE user LIKE 'mystic%';  -- should be empty

-- Optional cleanup:
-- DROP DATABASE IF EXISTS mysticml_user_mgmt;

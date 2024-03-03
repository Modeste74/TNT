-- prepares a MySQL server
-- should have all privileges
CREATE DATABASE IF NOT EXISTS tnt_dev_db;
CREATE USER IF NOT EXISTS 'tnt_dev'@'localhost' IDENTIFIED BY 'tnt_dev_pwd';
GRANT ALL PRIVILEGES ON tnt_dev_db.* TO 'tnt_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'tnt_dev'@'localhost';
FLUSH PRIVILEGES;
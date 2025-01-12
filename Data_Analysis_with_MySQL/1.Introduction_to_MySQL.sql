-- Create a database for storing student data.
CREATE DATABASE my_database;

--  Create a new database (if not already exist).
CREATE DATABASE IF NOT EXISTS my_database;

-- Switch to the newly created database.
USE my_database;

-- Create a table to store student information with id, name, and age columns.
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each student.
    name VARCHAR(100) NOT NULL, -- Name of the student (up to 100 characters).
    age INT NOT NULL CHECK (age > 0) -- Age of the student (must be a positive number).
);

--  Create a sample table in the database.
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each student.
    name VARCHAR(100) NOT NULL,        -- Student's name (required field).
    age INT                            -- Student's age.
);

-- Insert sample data into the students table.
INSERT INTO students (name, age) VALUES ('Aadil', 22);
INSERT INTO students (name, age) VALUES ('Emily', 21);

-- Improves performance by optimizing all tables in 'my_database'.
OPTIMIZE TABLE students;

-- Retrieve all records from the students table.
SELECT * FROM students;

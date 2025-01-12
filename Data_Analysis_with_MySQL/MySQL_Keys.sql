--  Create the database
CREATE DATABASE school_management;
USE school_management;

-- Create the `students` table (Primary Key + Unique Key)
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,  -- Primary Key
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,                 -- Unique Key
    age INT NOT NULL
);

--  Create the `courses` table (Primary Key + Unique Key)
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,  -- Primary Key
    course_name VARCHAR(100) UNIQUE NOT NULL   -- Unique Key
);

-- Create the `enrollments` table (Composite Key + Foreign Keys)
CREATE TABLE enrollments (
    student_id INT,                            -- Part of Composite Key
    course_id INT,                             -- Part of Composite Key
    enrollment_date DATE NOT NULL,
    PRIMARY KEY (student_id, course_id),       -- Composite Key
    FOREIGN KEY (student_id) REFERENCES students(student_id),  -- Foreign Key
    FOREIGN KEY (course_id) REFERENCES courses(course_id)       -- Foreign Key
);

--  Insert data into `students`
INSERT INTO students (name, email, age) VALUES
('Aadil', 'aadil@example.com', 22),
('Emily', 'emily@example.com', 23),
('Sama', 'sama@example.com', 21);

--  Insert data into `courses`
INSERT INTO courses (course_name) VALUES
('Mathematics'),
('Physics'),
('Chemistry');

--  Insert data into `enrollments`
INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES
(1, 1, '2025-01-10'),  -- Aadil enrolled in Mathematics
(1, 2, '2025-01-11'),  -- Aadil enrolled in Physics
(2, 1, '2025-01-12'),  -- Emily enrolled in Mathematics
(3, 3, '2025-01-13');  -- Sama enrolled in Chemistry

--  Query data to view relationships
SELECT
    e.enrollment_date,
    s.name AS student_name,
    c.course_name
FROM
    enrollments e
JOIN
    students s ON e.student_id = s.student_id
JOIN
    courses c ON e.course_id = c.course_id;


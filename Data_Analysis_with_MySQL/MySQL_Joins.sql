-- Create the database
CREATE DATABASE IF NOT EXISTS join_demo;
USE join_demo;

-- Create the `students` table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    class VARCHAR(20)
);

-- Create the `grades` table
CREATE TABLE grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject VARCHAR(50),
    grade CHAR(1),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Insert data into `students`
INSERT INTO students (name, class) VALUES
('Aadil', 'Mathematics'),
('Emily', 'Science'),
('Sama', 'Mathematics'),
('John', 'History');

-- Insert data into `grades`
INSERT INTO grades (student_id, subject, grade) VALUES
(1, 'Algebra', 'A'),
(1, 'Geometry', 'B'),
(2, 'Biology', 'A'),
(3, 'Calculus', 'C'),
(4, 'World History', 'B');

--  INNER JOIN - Matching records in both tables
SELECT
    students.name AS student_name,
    students.class,
    grades.subject,
    grades.grade
FROM students
INNER JOIN grades
ON students.student_id = grades.student_id;

-- LEFT JOIN - All records from the `students` table
SELECT
    students.name AS student_name,
    students.class,
    grades.subject,
    grades.grade
FROM students
LEFT JOIN grades
ON students.student_id = grades.student_id;

--  RIGHT JOIN - All records from the `grades` table
SELECT
    students.name AS student_name,
    students.class,
    grades.subject,
    grades.grade
FROM students
RIGHT JOIN grades
ON students.student_id = grades.student_id;

-- FULL JOIN - Emulated using UNION
SELECT
    students.name AS student_name,
    students.class,
    grades.subject,
    grades.grade
FROM students
LEFT JOIN grades
ON students.student_id = grades.student_id
UNION
SELECT
    students.name AS student_name,
    students.class,
    grades.subject,
    grades.grade
FROM students
RIGHT JOIN grades
ON students.student_id = grades.student_id;

-- CROSS JOIN - Cartesian product of both tables
SELECT
    students.name AS student_name,
    grades.subject
FROM students
CROSS JOIN grades;

-- SELF JOIN - Students in the same class
SELECT
    A.name AS student_1,
    B.name AS student_2,
    A.class
FROM students A
INNER JOIN students B
ON A.class = B.class
WHERE A.student_id != B.student_id;

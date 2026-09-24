-- =====================================================================
-- MysticML Journey · Week 2 · Module 8 – Control Flow Functions & Conditions
-- File: 02_control_flow_complete.sql
-- Covers: IF(), IFNULL(), NULLIF(), COALESCE(), CASE (simple + searched),
--         the IF ... ELSEIF ... ELSE statement inside a stored procedure
--         (with DELIMITER), CASE statement in a procedure, and MySQL
--         conditions/operators (AND, OR, NOT, XOR, IN, BETWEEN, LIKE,
--         IS NULL, EXISTS, comparison with NULL).
-- Run:   mysql -u root -p < 02_control_flow_complete.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mysticml_control_flow;
USE mysticml_control_flow;

DROP TABLE IF EXISTS exam_results;
CREATE TABLE exam_results (
    result_id  INT AUTO_INCREMENT PRIMARY KEY,
    student    VARCHAR(50) NOT NULL,
    subject    VARCHAR(30) NOT NULL,
    score      INT NULL,               -- NULL = absent / not graded yet
    max_score  INT NOT NULL DEFAULT 100,
    bonus      INT NULL,
    attempts   INT NOT NULL DEFAULT 1
);

INSERT INTO exam_results (student, subject, score, max_score, bonus, attempts) VALUES
('Aadil', 'SQL',     92, 100, 5,    1),
('Aadil', 'Python',  78, 100, NULL, 2),
('Emily', 'SQL',     64, 100, 0,    1),
('Emily', 'Python',  NULL, 100, NULL, 0),  -- absent
('Sama',  'SQL',     39, 100, 3,    3),
('Sama',  'Python',  85, 100, 0,    1),
('Rohan', 'SQL',     55,   0, NULL, 1);    -- data-entry error: max_score = 0

-- ---------------------------------------------------------------------
-- 1) IF(condition, value_if_true, value_if_false)
-- ---------------------------------------------------------------------
SELECT student, subject, score,
       IF(score >= 40, 'Pass', 'Fail')            AS result,       -- NULL score -> 'Fail'!
       IF(score IS NULL, 'Absent',
          IF(score >= 40, 'Pass', 'Fail'))        AS result_fixed  -- nested IF
FROM exam_results;

-- IF inside an aggregate: count passes per subject
SELECT subject,
       SUM(IF(score >= 40, 1, 0)) AS passed,
       SUM(IF(score <  40, 1, 0)) AS failed
FROM exam_results
GROUP BY subject;

-- ---------------------------------------------------------------------
-- 2) IFNULL(expr, fallback) – replace NULL with a fallback
--    COALESCE(a, b, c, ...) – first non-NULL of many (standard SQL)
-- ---------------------------------------------------------------------
SELECT student, subject,
       IFNULL(score, 0)                    AS score_or_zero,
       IFNULL(bonus, 0)                    AS bonus_or_zero,
       score + bonus                       AS naive_total,     -- NULL if either is NULL
       IFNULL(score, 0) + IFNULL(bonus, 0) AS safe_total,
       COALESCE(bonus, score, -1)          AS first_non_null
FROM exam_results;

-- ---------------------------------------------------------------------
-- 3) NULLIF(a, b) – returns NULL when a = b, otherwise a.
--    Classic use: avoid division by zero.
-- ---------------------------------------------------------------------
SELECT student, subject, score, max_score,
       ROUND(score / NULLIF(max_score, 0) * 100, 1)     AS pct,          -- NULL, not an error
       ROUND(score / NULLIF(attempts, 0), 1)            AS score_per_attempt
FROM exam_results;

SELECT NULLIF(5, 5) AS same_values, NULLIF(5, 3) AS different_values;

-- ---------------------------------------------------------------------
-- 4) CASE expression
-- ---------------------------------------------------------------------
-- 4a) Searched CASE: arbitrary conditions, first TRUE branch wins
SELECT student, subject, score,
       CASE
           WHEN score IS NULL THEN 'Absent'
           WHEN score >= 90   THEN 'A'
           WHEN score >= 75   THEN 'B'
           WHEN score >= 60   THEN 'C'
           WHEN score >= 40   THEN 'D'
           ELSE 'F'
       END AS grade
FROM exam_results;

-- 4b) Simple CASE: compare one expression to fixed values
SELECT student, subject,
       CASE subject
           WHEN 'SQL'    THEN 'Databases'
           WHEN 'Python' THEN 'Programming'
           ELSE 'Other'
       END AS track
FROM exam_results;

-- CASE in ORDER BY: custom sort order (Python first, then SQL)
SELECT student, subject FROM exam_results
ORDER BY CASE subject WHEN 'Python' THEN 1 WHEN 'SQL' THEN 2 ELSE 3 END, student;

-- CASE in UPDATE: conditional bonus
UPDATE exam_results
SET bonus = CASE
                WHEN attempts >= 3 THEN 0
                WHEN bonus IS NULL THEN 2
                ELSE bonus
            END;
SELECT student, subject, attempts, bonus FROM exam_results;

-- ---------------------------------------------------------------------
-- 5) IF STATEMENT (IF ... THEN ... ELSEIF ... ELSE ... END IF)
--    Only allowed inside stored programs (procedures, functions, triggers).
--    DELIMITER changes the statement terminator so the ; inside the body
--    doesn't end the CREATE PROCEDURE early.
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS classify_student;
DROP FUNCTION  IF EXISTS letter_grade;

DELIMITER //

CREATE PROCEDURE classify_student(IN p_student VARCHAR(50), OUT p_label VARCHAR(40))
BEGIN
    DECLARE v_avg DECIMAL(5, 2);                  -- local variable

    SELECT AVG(score) INTO v_avg
    FROM exam_results
    WHERE student = p_student;

    IF v_avg IS NULL THEN
        SET p_label = 'No results';
    ELSEIF v_avg >= 80 THEN
        SET p_label = 'Distinction';
    ELSEIF v_avg >= 50 THEN
        SET p_label = 'Pass';
    ELSE
        SET p_label = 'Needs support';
    END IF;
END //

-- A stored FUNCTION using a CASE *statement* (not expression)
CREATE FUNCTION letter_grade(p_score INT) RETURNS CHAR(1)
DETERMINISTIC
BEGIN
    DECLARE v_grade CHAR(1);
    CASE
        WHEN p_score IS NULL THEN SET v_grade = '-';
        WHEN p_score >= 90   THEN SET v_grade = 'A';
        WHEN p_score >= 75   THEN SET v_grade = 'B';
        WHEN p_score >= 60   THEN SET v_grade = 'C';
        ELSE SET v_grade = 'F';
    END CASE;
    RETURN v_grade;
END //

DELIMITER ;

CALL classify_student('Aadil', @label_aadil);
CALL classify_student('Sama',  @label_sama);
CALL classify_student('Nobody', @label_nobody);
SELECT @label_aadil AS aadil, @label_sama AS sama, @label_nobody AS nobody;

SELECT student, subject, score, letter_grade(score) AS grade FROM exam_results;

-- ---------------------------------------------------------------------
-- 6) MySQL CONDITIONS (operators used in WHERE / IF / CASE)
-- ---------------------------------------------------------------------
-- AND / OR / NOT  (AND binds tighter than OR – use parentheses!)
SELECT student, subject, score FROM exam_results
WHERE subject = 'SQL' AND (score >= 90 OR score < 40);

SELECT student, subject FROM exam_results WHERE NOT subject = 'SQL';

-- XOR: true when exactly one side is true
SELECT student, subject, score, attempts FROM exam_results
WHERE (score >= 80) XOR (attempts > 1);

-- IN / NOT IN, BETWEEN, LIKE
SELECT student, score FROM exam_results WHERE student IN ('Aadil', 'Sama');
SELECT student, score FROM exam_results WHERE score BETWEEN 50 AND 80;
SELECT DISTINCT student FROM exam_results WHERE student LIKE '_a%';  -- 2nd letter 'a'

-- NULL is never "= NULL": comparisons with NULL are UNKNOWN (neither true nor false)
SELECT NULL = NULL AS eq, NULL IS NULL AS is_null, NULL <=> NULL AS null_safe_eq;
SELECT student, subject FROM exam_results WHERE score IS NULL;

-- EXISTS: students who failed at least one exam
SELECT DISTINCT r.student
FROM exam_results r
WHERE EXISTS (SELECT 1 FROM exam_results f
              WHERE f.student = r.student AND f.score < 40);

-- Boolean expressions evaluate to 1 / 0 / NULL
SELECT 5 > 3 AS true_is_1, 5 < 3 AS false_is_0, 5 > NULL AS unknown_is_null;

-- Optional cleanup:
-- DROP DATABASE IF EXISTS mysticml_control_flow;

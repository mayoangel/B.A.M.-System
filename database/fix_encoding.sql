-- =============================================================================
-- 1) Charset de la BD y tablas
-- 2) Vaciar datos de demo (respeta FKs) para reimportar seeds limpios
--
-- Luego, desde la shell de XAMPP (NO dentro de mysql), corre:
--   C:\xampp\mysql\bin\mysql.exe -u root --default-character-set=utf8mb4 BAM_System < "C:\Coding\anzuelomike\B.A.M.-System\database\seeds.sql"
--   C:\xampp\mysql\bin\mysql.exe -u root --default-character-set=utf8mb4 BAM_System < "C:\Coding\anzuelomike\B.A.M.-System\database\seed_fill.sql"
-- =============================================================================

USE BAM_System;

ALTER DATABASE BAM_System CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE attendance;
TRUNCATE TABLE biometric_information;
TRUNCATE TABLE student_courses;
TRUNCATE TABLE employee_course;
TRUNCATE TABLE student_tutor;
TRUNCATE TABLE reports;
TRUNCATE TABLE pre_register;
TRUNCATE TABLE non_working_days;
TRUNCATE TABLE students;
TRUNCATE TABLE employees;
TRUNCATE TABLE courses;
TRUNCATE TABLE parents;
TRUNCATE TABLE role;

SET FOREIGN_KEY_CHECKS = 1;

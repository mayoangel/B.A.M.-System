-- =============================================================================
-- Rellena una BD ya sembrada SIN fallar si algunos datos ya existen.
-- Seguro de re-ejecutar (idempotente donde hay UNIQUE).
--
--   C:\xampp\mysql\bin\mysql.exe -u root BAM_System -e "SOURCE C:/Coding/anzuelomike/B.A.M.-System/database/seed_fill.sql;"
--
-- Contraseña de cuentas nuevas: Bam2026!
-- =============================================================================

USE BAM_System;

DELETE FROM biometric_information
WHERE encryption_hash LIKE 'hash_biometrico_encriptado_%';

INSERT IGNORE INTO parents (name, lastname, surename, phone, email, password, dir_street, dir_col, dir_num) VALUES
('Patricia', 'Ramírez', 'Vega', '5552010101', 'patricia.ramirez@mail.com', '$2b$12$RnR8iTGBRxpf68hoFIQwk.ZzABbzhBUyKJy7F2uiAHDH0XcEwhKZW', 'Av. Universidad', 'Narvarte', '88'),
('Jorge', 'Hernández', 'Soto', '5552020202', 'jorge.hernandez@mail.com', '$2b$12$dxWKw9k.ki7dmsP4rKh9fOMt9FjhB4i6MS1TfDQZZ7qST9eRsAYxO', 'Calle Durango', 'Condesa', '23'),
('Elena', 'Vargas', 'Mejía', '5552030303', 'elena.vargas@mail.com', '$2b$12$46anHMm5NrSukM24Jk7K8uIYh/JwYLQ83NafgeXbHuaBurjjG0hD2', 'Av. Patriotismo', 'Mixcoac', '56'),
('Ricardo', 'Flores', 'Nava', '5552040404', 'ricardo.flores@mail.com', '$2b$12$RnR8iTGBRxpf68hoFIQwk.ZzABbzhBUyKJy7F2uiAHDH0XcEwhKZW', 'Calle Amberes', 'Juárez', '9'),
('Mónica', 'Reyes', 'Paredes', '5552050505', 'monica.reyes@mail.com', '$2b$12$dxWKw9k.ki7dmsP4rKh9fOMt9FjhB4i6MS1TfDQZZ7qST9eRsAYxO', 'Av. División del Norte', 'Portales', '140');

INSERT INTO courses (name, description, category, start_date, end_date, time_duration, days_of_week, status)
SELECT * FROM (
  SELECT 'Inglés Conversacional' AS name, 'Práctica oral nivel intermedio' AS description, 'Idiomas' AS category, '2026-02-10' AS start_date, '2026-08-10' AS end_date, '70 horas' AS time_duration, 'Martes-Jueves' AS days_of_week, 'Activo' AS status
  UNION ALL SELECT 'Robótica Educativa', 'Introducción a sensores y motores', 'STEM', '2026-03-05', '2026-08-30', '90 horas', 'Sábado', 'Activo'
  UNION ALL SELECT 'Matemáticas Aplicadas', 'Álgebra y resolución de problemas', 'Académico', '2026-01-20', '2026-06-20', '60 horas', 'Lunes-Miércoles', 'Inactivo'
) AS x
WHERE NOT EXISTS (SELECT 1 FROM courses c WHERE c.name = x.name);

INSERT INTO employees (id_employee, name, lastname, surename, email, password, phone, age, status, dir_street, dir_col, dir_num, role_id)
SELECT * FROM (
  SELECT '1004' AS id_employee, 'Miguel' AS name, 'Ortega' AS lastname, 'Lira' AS surename, 'miguel.ortega@bam.com' AS email, '$2b$12$u41JnNd8C58LXv2bpsyPn.tXhvRxV7viGOt4iS6scre2zFyKVbDTS' AS password, '5556667778' AS phone, 31 AS age, 'Activo' AS status, 'Calle Amberes' AS dir_street, 'Juárez' AS dir_col, '15' AS dir_num, 2 AS role_id
  UNION ALL SELECT '1005', 'Carmen', 'Delgado', 'Ruiz', 'carmen.delgado@bam.com', '$2b$12$Y3kwo0O04lsrgVOc77BX/uD8xfTwCEcWphPR8xMNN8CM2TwtxfdvW', '5557778889', 39, 'Activo', 'Av. Coyoacán', 'Del Valle', '220', 2
  UNION ALL SELECT '1006', 'Pedro', 'Navarro', 'Gil', 'pedro.navarro@bam.com', '$2b$12$nFjOgKo.NZniKillccrnOOWUWUjMV6XVhhHN0Zn1RdkRaGqaGIuIC', '5558889990', 27, 'Activo', 'Calle Medellín', 'Roma Norte', '44', 3
) AS x
WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.email = x.email);

INSERT INTO pre_register (name, lastname, surename, email, phone, course_id)
SELECT 'Andrea', 'Salinas', 'Mora', 'andrea.salinas@mail.com', '5553001001', id FROM courses WHERE name = 'Inglés Conversacional'
AND NOT EXISTS (SELECT 1 FROM pre_register p WHERE p.email = 'andrea.salinas@mail.com')
UNION ALL
SELECT 'Bruno', 'Ibarra', 'León', 'bruno.ibarra@mail.com', '5553001002', id FROM courses WHERE name = 'Robótica Educativa'
AND NOT EXISTS (SELECT 1 FROM pre_register p WHERE p.email = 'bruno.ibarra@mail.com')
UNION ALL
SELECT 'Camila', 'Duarte', 'Paz', 'camila.duarte@mail.com', '5553001003', id FROM courses WHERE name = 'Diseño UI/UX'
AND NOT EXISTS (SELECT 1 FROM pre_register p WHERE p.email = 'camila.duarte@mail.com');

INSERT INTO reports (name, generation_date, employee_id)
SELECT 'Reporte Semanal de Asistencia - Jul', '2026-07-31 17:00:00', 1
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM reports r WHERE r.name = 'Reporte Semanal de Asistencia - Jul')
UNION ALL
SELECT 'Concentrado de Faltas - Agosto', '2026-08-08 10:00:00', 1
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM reports r WHERE r.name = 'Concentrado de Faltas - Agosto');

INSERT INTO students (id_student, name, lastname, surename, date_of_birth, status, id_parent, created_at)
SELECT v.matricula, v.nombre, v.ap1, v.ap2, v.dob, v.estatus, p.id, v.creado
FROM (
  SELECT 'BAM-2026-0004' AS matricula, 'Mariana' AS nombre, 'Ramírez' AS ap1, 'López' AS ap2, '2010-05-18' AS dob, 'Activo' AS estatus, 'patricia.ramirez@mail.com' AS parent_email, '2026-03-01 09:30:00' AS creado
  UNION ALL SELECT 'BAM-2026-0005', 'Andrés', 'Hernández', 'Cruz', '2009-09-30', 'Activo', 'jorge.hernandez@mail.com', '2026-03-15 10:15:00'
  UNION ALL SELECT 'BAM-2026-0006', 'Paula', 'Vargas', 'Díaz', '2011-01-12', 'Activo', 'elena.vargas@mail.com', '2026-04-02 08:45:00'
  UNION ALL SELECT 'BAM-2026-0007', 'Emilio', 'Flores', 'Ríos', '2010-08-25', 'Activo', 'ricardo.flores@mail.com', '2026-04-20 12:00:00'
  UNION ALL SELECT 'BAM-2026-0008', 'Renata', 'Reyes', 'Campos', '2009-12-03', 'Activo', 'monica.reyes@mail.com', '2026-05-10 09:00:00'
  UNION ALL SELECT 'BAM-2026-0009', 'Mateo', 'Ramírez', 'Soto', '2011-04-17', 'Activo', 'patricia.ramirez@mail.com', '2026-06-01 10:30:00'
  UNION ALL SELECT 'BAM-2026-0010', 'Valentina', 'Hernández', 'Mora', '2010-10-09', 'Activo', 'jorge.hernandez@mail.com', '2026-06-18 11:00:00'
  UNION ALL SELECT 'BAM-2026-0011', 'Santiago', 'Vargas', 'Peña', '2009-06-21', 'Activo', 'elena.vargas@mail.com', '2026-07-05 09:20:00'
  UNION ALL SELECT 'BAM-2026-0012', 'Isabella', 'Flores', 'Guzmán', '2011-02-28', 'Activo', 'ricardo.flores@mail.com', '2026-07-22 14:00:00'
  UNION ALL SELECT 'BAM-2026-0013', 'Daniel', 'Reyes', 'Aguilar', '2010-07-11', 'Activo', 'monica.reyes@mail.com', '2026-08-01 09:00:00'
  UNION ALL SELECT 'BAM-2026-0014', 'Camila', 'Mendoza', 'Ruiz', '2009-11-19', 'Activo', 'carlos.mendoza@mail.com', '2026-08-05 10:00:00'
  UNION ALL SELECT 'BAM-2026-0015', 'Nicolás', 'Espinoza', 'Torres', '2011-03-08', 'Baja', 'gabriela.espinoza@mail.com', '2026-05-28 16:00:00'
) AS v
JOIN parents p ON p.email = v.parent_email
WHERE NOT EXISTS (SELECT 1 FROM students s WHERE s.id_student = v.matricula);

INSERT INTO student_tutor (start_date, end_date, status, student_id, employee_id)
SELECT t.start_date, t.end_date, t.status, s.id, e.id
FROM (
  SELECT '2026-03-01' AS start_date, NULL AS end_date, 'En Progreso' AS status, 'BAM-2026-0004' AS matricula, 'miguel.ortega@bam.com' AS emp
  UNION ALL SELECT '2026-04-01', NULL, 'En Progreso', 'BAM-2026-0005', 'miguel.ortega@bam.com'
  UNION ALL SELECT '2026-04-15', NULL, 'En Progreso', 'BAM-2026-0006', 'carmen.delgado@bam.com'
  UNION ALL SELECT '2026-05-01', NULL, 'En Progreso', 'BAM-2026-0007', 'carmen.delgado@bam.com'
  UNION ALL SELECT '2026-06-01', NULL, 'En Progreso', 'BAM-2026-0008', 'roberto.sanchez@bam.com'
) AS t
JOIN students s ON s.id_student = t.matricula
JOIN employees e ON e.email = t.emp
WHERE NOT EXISTS (
  SELECT 1 FROM student_tutor st WHERE st.student_id = s.id AND st.employee_id = e.id
);

INSERT IGNORE INTO student_courses (student_id, course_id)
SELECT s.id, c.id FROM students s JOIN courses c ON c.name = 'Programación en Python' WHERE s.id_student IN ('BAM-2026-0004','BAM-2026-0005','BAM-2026-0009','BAM-2026-0011','BAM-2026-0013')
UNION ALL
SELECT s.id, c.id FROM students s JOIN courses c ON c.name = 'Diseño UI/UX' WHERE s.id_student IN ('BAM-2026-0004','BAM-2026-0006','BAM-2026-0010','BAM-2026-0012')
UNION ALL
SELECT s.id, c.id FROM students s JOIN courses c ON c.name = 'Base de Datos SQL' WHERE s.id_student IN ('BAM-2026-0005','BAM-2026-0007','BAM-2026-0010','BAM-2026-0013')
UNION ALL
SELECT s.id, c.id FROM students s JOIN courses c ON c.name = 'Inglés Conversacional' WHERE s.id_student IN ('BAM-2026-0002','BAM-2026-0006','BAM-2026-0008','BAM-2026-0011','BAM-2026-0014')
UNION ALL
SELECT s.id, c.id FROM students s JOIN courses c ON c.name = 'Robótica Educativa' WHERE s.id_student IN ('BAM-2026-0007','BAM-2026-0008','BAM-2026-0009','BAM-2026-0012','BAM-2026-0014');

INSERT IGNORE INTO employee_course (employee_id, course_id)
SELECT e.id, c.id FROM employees e JOIN courses c ON c.name = 'Diseño UI/UX' WHERE e.email = 'miguel.ortega@bam.com'
UNION ALL
SELECT e.id, c.id FROM employees e JOIN courses c ON c.name = 'Inglés Conversacional' WHERE e.email = 'miguel.ortega@bam.com'
UNION ALL
SELECT e.id, c.id FROM employees e JOIN courses c ON c.name = 'Robótica Educativa' WHERE e.email = 'carmen.delgado@bam.com'
UNION ALL
SELECT e.id, c.id FROM employees e JOIN courses c ON c.name = 'Programación en Python' WHERE e.email = 'carmen.delgado@bam.com'
UNION ALL
SELECT e.id, c.id FROM employees e JOIN courses c ON c.name = 'Diseño UI/UX' WHERE e.email = 'lucia.torres@bam.com'
UNION ALL
SELECT e.id, c.id FROM employees e JOIN courses c ON c.name = 'Inglés Conversacional' WHERE e.email = 'pedro.navarro@bam.com'
UNION ALL
SELECT e.id, c.id FROM employees e JOIN courses c ON c.name = 'Robótica Educativa' WHERE e.email = 'pedro.navarro@bam.com';

INSERT IGNORE INTO non_working_days (date, description) VALUES
('2026-01-01', 'Año Nuevo'),
('2026-02-02', 'Día de la Candelaria'),
('2026-03-16', 'Natalicio de Benito Juárez'),
('2026-05-01', 'Día del Trabajo'),
('2026-09-16', 'Independencia de México'),
('2026-11-02', 'Día de Muertos'),
('2026-12-25', 'Navidad');

-- Asistencias demo: evita duplicar el mismo alumno/curso/fecha/hora
INSERT INTO attendance (date, time, status, method, student_id, employee_id, course_id)
SELECT d.fecha, d.hora, d.estatus, d.metodo, s.id, e.id, c.id
FROM (
  SELECT '2026-08-03' AS fecha, '08:01:10' AS hora, 'Asistencia' AS estatus, 'Biométrico Facial' AS metodo, 'BAM-2026-0001' AS matricula, 'lucia.torres@bam.com' AS emp, 'Programación en Python' AS curso
  UNION ALL SELECT '2026-08-03','08:03:22','Asistencia','Biométrico Facial','BAM-2026-0002','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-03','08:07:40','Retardo','Manual','BAM-2026-0004','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-03','08:02:05','Asistencia','Biométrico Facial','BAM-2026-0005','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-03','08:04:18','Asistencia','Manual','BAM-2026-0009','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-03','08:10:00','Falta injustificada','Manual','BAM-2026-0011','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-03','08:05:33','Asistencia','Biométrico Facial','BAM-2026-0013','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-04','09:01:00','Asistencia','Biométrico Facial','BAM-2026-0004','pedro.navarro@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-04','09:02:15','Asistencia','Manual','BAM-2026-0006','pedro.navarro@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-04','09:08:40','Retardo','Manual','BAM-2026-0010','pedro.navarro@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-04','09:03:20','Asistencia','Biométrico Facial','BAM-2026-0012','pedro.navarro@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-05','08:00:50','Asistencia','Biométrico Facial','BAM-2026-0001','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-05','08:02:10','Asistencia','Biométrico Facial','BAM-2026-0002','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-05','08:03:00','Asistencia','Manual','BAM-2026-0004','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-05','08:15:20','Retardo','Manual','BAM-2026-0005','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-05','08:04:40','Asistencia','Biométrico Facial','BAM-2026-0009','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-05','08:05:10','Asistencia','Manual','BAM-2026-0011','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-05','08:06:00','Asistencia','Biométrico Facial','BAM-2026-0013','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-06','10:01:00','Asistencia','Biométrico Facial','BAM-2026-0002','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-06','10:02:30','Asistencia','Manual','BAM-2026-0006','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-06','10:12:00','Retardo','Manual','BAM-2026-0008','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-06','10:03:45','Asistencia','Biométrico Facial','BAM-2026-0011','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-06','10:04:20','Asistencia','Manual','BAM-2026-0014','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-07','08:01:30','Asistencia','Biométrico Facial','BAM-2026-0001','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-07','08:02:40','Asistencia','Manual','BAM-2026-0005','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-07','08:03:10','Asistencia','Biométrico Facial','BAM-2026-0007','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-07','08:20:00','Falta injustificada','Manual','BAM-2026-0010','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-07','08:04:50','Asistencia','Manual','BAM-2026-0013','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-10','08:01:05','Asistencia','Biométrico Facial','BAM-2026-0001','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-10','08:02:18','Asistencia','Biométrico Facial','BAM-2026-0002','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-10','08:03:40','Asistencia','Manual','BAM-2026-0004','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-10','08:14:22','Retardo','Manual','BAM-2026-0005','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-10','08:04:55','Asistencia','Biométrico Facial','BAM-2026-0009','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-10','08:05:30','Asistencia','Manual','BAM-2026-0011','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-10','08:06:10','Asistencia','Biométrico Facial','BAM-2026-0013','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-10','08:07:00','Asistencia','Manual','BAM-2026-0014','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-10','09:01:20','Asistencia','Biométrico Facial','BAM-2026-0004','miguel.ortega@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-10','09:02:45','Asistencia','Manual','BAM-2026-0006','miguel.ortega@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-10','09:03:10','Asistencia','Biométrico Facial','BAM-2026-0010','miguel.ortega@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-10','09:18:00','Falta injustificada','Manual','BAM-2026-0012','miguel.ortega@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-11','08:00:40','Asistencia','Biométrico Facial','BAM-2026-0001','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-11','08:01:55','Asistencia','Biométrico Facial','BAM-2026-0002','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-11','08:16:10','Retardo','Manual','BAM-2026-0004','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-11','08:03:20','Asistencia','Manual','BAM-2026-0005','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-11','08:04:00','Asistencia','Biométrico Facial','BAM-2026-0009','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-11','08:05:25','Asistencia','Manual','BAM-2026-0011','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-11','08:20:40','Falta injustificada','Manual','BAM-2026-0013','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-11','10:01:10','Asistencia','Biométrico Facial','BAM-2026-0002','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-11','10:02:30','Asistencia','Manual','BAM-2026-0006','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-11','10:03:45','Asistencia','Biométrico Facial','BAM-2026-0008','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-11','10:04:20','Asistencia','Manual','BAM-2026-0011','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-11','10:05:00','Asistencia','Biométrico Facial','BAM-2026-0014','pedro.navarro@bam.com','Inglés Conversacional'
  UNION ALL SELECT '2026-08-11','11:01:00','Asistencia','Manual','BAM-2026-0007','carmen.delgado@bam.com','Robótica Educativa'
  UNION ALL SELECT '2026-08-11','11:02:15','Asistencia','Biométrico Facial','BAM-2026-0008','carmen.delgado@bam.com','Robótica Educativa'
  UNION ALL SELECT '2026-08-11','11:12:40','Retardo','Manual','BAM-2026-0009','carmen.delgado@bam.com','Robótica Educativa'
  UNION ALL SELECT '2026-08-11','11:03:50','Asistencia','Manual','BAM-2026-0012','carmen.delgado@bam.com','Robótica Educativa'
  UNION ALL SELECT '2026-08-11','11:04:30','Asistencia','Biométrico Facial','BAM-2026-0014','carmen.delgado@bam.com','Robótica Educativa'
  UNION ALL SELECT '2026-08-12','08:01:00','Asistencia','Biométrico Facial','BAM-2026-0001','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-12','08:02:20','Asistencia','Biométrico Facial','BAM-2026-0002','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-12','08:03:15','Asistencia','Manual','BAM-2026-0004','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-12','08:04:40','Asistencia','Manual','BAM-2026-0005','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-12','08:15:10','Retardo','Manual','BAM-2026-0009','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-12','08:05:50','Asistencia','Biométrico Facial','BAM-2026-0011','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-12','08:06:30','Asistencia','Manual','BAM-2026-0013','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-12','08:07:05','Asistencia','Biométrico Facial','BAM-2026-0014','lucia.torres@bam.com','Programación en Python'
  UNION ALL SELECT '2026-08-12','09:01:30','Asistencia','Manual','BAM-2026-0004','miguel.ortega@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-12','09:02:40','Asistencia','Biométrico Facial','BAM-2026-0006','miguel.ortega@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-12','09:03:55','Asistencia','Manual','BAM-2026-0010','miguel.ortega@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-12','09:04:20','Asistencia','Biométrico Facial','BAM-2026-0012','miguel.ortega@bam.com','Diseño UI/UX'
  UNION ALL SELECT '2026-08-12','08:02:00','Asistencia','Manual','BAM-2026-0001','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-12','08:03:10','Asistencia','Biométrico Facial','BAM-2026-0005','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-12','08:04:25','Asistencia','Manual','BAM-2026-0007','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-12','08:18:00','Retardo','Manual','BAM-2026-0010','lucia.torres@bam.com','Base de Datos SQL'
  UNION ALL SELECT '2026-08-12','08:05:40','Asistencia','Biométrico Facial','BAM-2026-0013','lucia.torres@bam.com','Base de Datos SQL'
) AS d
JOIN students s ON s.id_student = d.matricula
JOIN employees e ON e.email = d.emp
JOIN courses c ON c.name = d.curso
WHERE NOT EXISTS (
  SELECT 1 FROM attendance a
  WHERE a.student_id = s.id AND a.course_id = c.id AND a.date = d.fecha AND a.time = d.hora
);

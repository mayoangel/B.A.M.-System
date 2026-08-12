USE BAM_System;

-- =============================================================================
-- Seeds de demostración B.A.M.
-- Contraseña de todas las cuentas (empleados y tutores): Bam2026!
-- =============================================================================

INSERT INTO role (name, description) VALUES
('Administrador', 'Acceso total al sistema y reportes'),
('Profesor', 'Control de asistencia y gestión de cursos'),
('Prefecto', 'Encargado de la toma de asistencia biométrica');

INSERT INTO parents (name, lastname, surename, phone, email, password, dir_street, dir_col, dir_num) VALUES
('Carlos', 'Mendoza', 'Ruiz', '5551234567', 'carlos.mendoza@mail.com', '$2b$12$RnR8iTGBRxpf68hoFIQwk.ZzABbzhBUyKJy7F2uiAHDH0XcEwhKZW', 'Av. Juárez', 'Centro', '12'),
('Gabriela', 'Espinoza', 'Luna', '5557654321', 'gabriela.espinoza@mail.com', '$2b$12$dxWKw9k.ki7dmsP4rKh9fOMt9FjhB4i6MS1TfDQZZ7qST9eRsAYxO', 'Calle Olivo', 'Del Valle', '45'),
('Manuel', 'Castro', 'Ortiz', '5559876543', 'manuel.castro@mail.com', '$2b$12$46anHMm5NrSukM24Jk7K8uIYh/JwYLQ83NafgeXbHuaBurjjG0hD2', 'Calle Colima', 'Roma', '110'),
('Patricia', 'Ramírez', 'Vega', '5552010101', 'patricia.ramirez@mail.com', '$2b$12$RnR8iTGBRxpf68hoFIQwk.ZzABbzhBUyKJy7F2uiAHDH0XcEwhKZW', 'Av. Universidad', 'Narvarte', '88'),
('Jorge', 'Hernández', 'Soto', '5552020202', 'jorge.hernandez@mail.com', '$2b$12$dxWKw9k.ki7dmsP4rKh9fOMt9FjhB4i6MS1TfDQZZ7qST9eRsAYxO', 'Calle Durango', 'Condesa', '23'),
('Elena', 'Vargas', 'Mejía', '5552030303', 'elena.vargas@mail.com', '$2b$12$46anHMm5NrSukM24Jk7K8uIYh/JwYLQ83NafgeXbHuaBurjjG0hD2', 'Av. Patriotismo', 'Mixcoac', '56'),
('Ricardo', 'Flores', 'Nava', '5552040404', 'ricardo.flores@mail.com', '$2b$12$RnR8iTGBRxpf68hoFIQwk.ZzABbzhBUyKJy7F2uiAHDH0XcEwhKZW', 'Calle Amberes', 'Juárez', '9'),
('Mónica', 'Reyes', 'Paredes', '5552050505', 'monica.reyes@mail.com', '$2b$12$dxWKw9k.ki7dmsP4rKh9fOMt9FjhB4i6MS1TfDQZZ7qST9eRsAYxO', 'Av. División del Norte', 'Portales', '140');

INSERT INTO courses (name, description, category, start_date, end_date, time_duration, days_of_week, status) VALUES
('Programación en Python', 'Curso básico desde cero', 'Tecnología', '2026-01-15', '2026-06-15', '80 horas', 'Lunes-Miércoles', 'Activo'),
('Diseño UI/UX', 'Principios de diseño de interfaces', 'Diseño', '2026-02-01', '2026-05-01', '50 horas', 'Martes-Jueves', 'Activo'),
('Base de Datos SQL', 'Diseño y optimización de consultas', 'Tecnología', '2026-03-01', '2026-07-01', '60 horas', 'Lunes-Miércoles-Viernes', 'Activo'),
('Inglés Conversacional', 'Práctica oral nivel intermedio', 'Idiomas', '2026-02-10', '2026-08-10', '70 horas', 'Martes-Jueves', 'Activo'),
('Robótica Educativa', 'Introducción a sensores y motores', 'STEM', '2026-03-05', '2026-08-30', '90 horas', 'Sábado', 'Activo'),
('Matemáticas Aplicadas', 'Álgebra y resolución de problemas', 'Académico', '2026-01-20', '2026-06-20', '60 horas', 'Lunes-Miércoles', 'Inactivo');

INSERT INTO employees (id_employee, name, lastname, surename, email, password, phone, age, status, dir_street, dir_col, dir_num, role_id) VALUES
(1001, 'Ana', 'Gomez', 'Pérez', 'ana.gomez@bam.com', '$2b$12$u41JnNd8C58LXv2bpsyPn.tXhvRxV7viGOt4iS6scre2zFyKVbDTS', '5551112223', 35, 'Activo', 'Av. Reforma', 'Centro', '102', 1),
(1002, 'Roberto', 'Sánchez', 'Díaz', 'roberto.sanchez@bam.com', '$2b$12$Y3kwo0O04lsrgVOc77BX/uD8xfTwCEcWphPR8xMNN8CM2TwtxfdvW', '5553334445', 42, 'Activo', 'Calle Juarez', 'Del Valle', '405', 2),
(1003, 'Lucía', 'Torres', 'Marín', 'lucia.torres@bam.com', '$2b$12$nFjOgKo.NZniKillccrnOOWUWUjMV6XVhhHN0Zn1RdkRaGqaGIuIC', '5555556667', 28, 'Activo', 'Av. Insurgentes', 'Roma', '78', 3),
(1004, 'Miguel', 'Ortega', 'Lira', 'miguel.ortega@bam.com', '$2b$12$u41JnNd8C58LXv2bpsyPn.tXhvRxV7viGOt4iS6scre2zFyKVbDTS', '5556667778', 31, 'Activo', 'Calle Amberes', 'Juárez', '15', 2),
(1005, 'Carmen', 'Delgado', 'Ruiz', 'carmen.delgado@bam.com', '$2b$12$Y3kwo0O04lsrgVOc77BX/uD8xfTwCEcWphPR8xMNN8CM2TwtxfdvW', '5557778889', 39, 'Activo', 'Av. Coyoacán', 'Del Valle', '220', 2),
(1006, 'Pedro', 'Navarro', 'Gil', 'pedro.navarro@bam.com', '$2b$12$nFjOgKo.NZniKillccrnOOWUWUjMV6XVhhHN0Zn1RdkRaGqaGIuIC', '5558889990', 27, 'Activo', 'Calle Medellín', 'Roma Norte', '44', 3);

INSERT INTO pre_register (name, lastname, surename, email, phone, course_id) VALUES
('Valeria', 'Rojas', 'Solís', 'valeria.rojas@mail.com', '5554443322', 1),
('Javier', 'Pacheco', 'Cruz', 'javier.pach@mail.com', '5559998877', 3),
('Andrea', 'Salinas', 'Mora', 'andrea.salinas@mail.com', '5553001001', 4),
('Bruno', 'Ibarra', 'León', 'bruno.ibarra@mail.com', '5553001002', 5),
('Camila', 'Duarte', 'Paz', 'camila.duarte@mail.com', '5553001003', 2);

INSERT INTO reports (name, generation_date, employee_id) VALUES
('Reporte de Asistencia Mensual - Mayo', '2026-05-31 18:00:00', 1),
('Auditoría de Alumnos Activos', '2026-06-01 09:30:00', 1),
('Reporte Semanal de Asistencia - Jul', '2026-07-31 17:00:00', 1),
('Concentrado de Faltas - Agosto', '2026-08-08 10:00:00', 1);

-- created_at variado para que el dashboard muestre crecimiento mensual
INSERT INTO students (id_student, name, lastname, surename, date_of_birth, status, id_parent, created_at) VALUES
('BAM-2026-0001', 'Luis', 'Mendoza', 'Espinoza', '2010-03-14', 'Activo', 1, '2026-01-20 09:00:00'),
('BAM-2026-0002', 'Sofía', 'Castro', 'Espinoza', '2009-07-22', 'Activo', 3, '2026-02-05 10:00:00'),
('BAM-2026-0003', 'Diego', 'Mendoza', 'Luna', '2011-11-05', 'Inactivo', 2, '2026-02-12 11:00:00'),
('BAM-2026-0004', 'Mariana', 'Ramírez', 'López', '2010-05-18', 'Activo', 4, '2026-03-01 09:30:00'),
('BAM-2026-0005', 'Andrés', 'Hernández', 'Cruz', '2009-09-30', 'Activo', 5, '2026-03-15 10:15:00'),
('BAM-2026-0006', 'Paula', 'Vargas', 'Díaz', '2011-01-12', 'Activo', 6, '2026-04-02 08:45:00'),
('BAM-2026-0007', 'Emilio', 'Flores', 'Ríos', '2010-08-25', 'Activo', 7, '2026-04-20 12:00:00'),
('BAM-2026-0008', 'Renata', 'Reyes', 'Campos', '2009-12-03', 'Activo', 8, '2026-05-10 09:00:00'),
('BAM-2026-0009', 'Mateo', 'Ramírez', 'Soto', '2011-04-17', 'Activo', 4, '2026-06-01 10:30:00'),
('BAM-2026-0010', 'Valentina', 'Hernández', 'Mora', '2010-10-09', 'Activo', 5, '2026-06-18 11:00:00'),
('BAM-2026-0011', 'Santiago', 'Vargas', 'Peña', '2009-06-21', 'Activo', 6, '2026-07-05 09:20:00'),
('BAM-2026-0012', 'Isabella', 'Flores', 'Guzmán', '2011-02-28', 'Activo', 7, '2026-07-22 14:00:00'),
('BAM-2026-0013', 'Daniel', 'Reyes', 'Aguilar', '2010-07-11', 'Activo', 8, '2026-08-01 09:00:00'),
('BAM-2026-0014', 'Camila', 'Mendoza', 'Ruiz', '2009-11-19', 'Activo', 1, '2026-08-05 10:00:00'),
('BAM-2026-0015', 'Nicolás', 'Espinoza', 'Torres', '2011-03-08', 'Baja', 2, '2026-05-28 16:00:00');

-- NO insertar face_vector falsos: el motor exige tokens Fernet reales.
-- Enrolar rostros desde la UI (RF-02).

INSERT INTO student_tutor (start_date, end_date, status, student_id, employee_id) VALUES
('2026-01-15', '2026-06-15', 'Completado', 1, 2),
('2026-03-01', NULL, 'En Progreso', 2, 2),
('2026-03-01', NULL, 'En Progreso', 4, 4),
('2026-04-01', NULL, 'En Progreso', 5, 4),
('2026-04-15', NULL, 'En Progreso', 6, 5),
('2026-05-01', NULL, 'En Progreso', 7, 5),
('2026-06-01', NULL, 'En Progreso', 8, 2);

INSERT INTO student_courses (student_id, course_id) VALUES
(1, 1), (1, 3),
(2, 1), (2, 4),
(3, 2),
(4, 1), (4, 2),
(5, 1), (5, 3),
(6, 2), (6, 4),
(7, 3), (7, 5),
(8, 4), (8, 5),
(9, 1), (9, 5),
(10, 2), (10, 3),
(11, 4), (11, 1),
(12, 5), (12, 2),
(13, 1), (13, 3),
(14, 4), (14, 5);

INSERT INTO employee_course (employee_id, course_id) VALUES
(2, 1), (2, 3),
(4, 2), (4, 4),
(5, 5), (5, 1),
(3, 1), (3, 2), (3, 3),
(6, 4), (6, 5);

INSERT INTO non_working_days (date, description) VALUES
('2026-01-01', 'Año Nuevo'),
('2026-02-02', 'Día de la Candelaria'),
('2026-03-16', 'Natalicio de Benito Juárez'),
('2026-05-01', 'Día del Trabajo'),
('2026-09-16', 'Independencia de México'),
('2026-11-02', 'Día de Muertos'),
('2026-12-25', 'Navidad');

-- Asistencias históricas (junio-julio) + semana actual (10-12 ago 2026)
-- Estados usados por el dashboard: Asistencia, Retardo; también Falta injustificada
INSERT INTO attendance (date, time, status, method, student_id, employee_id, course_id) VALUES
-- Semana del 3-7 ago (semana anterior)
('2026-08-03', '08:01:10', 'Asistencia', 'Biométrico Facial', 1, 3, 1),
('2026-08-03', '08:03:22', 'Asistencia', 'Biométrico Facial', 2, 3, 1),
('2026-08-03', '08:07:40', 'Retardo', 'Manual', 4, 3, 1),
('2026-08-03', '08:02:05', 'Asistencia', 'Biométrico Facial', 5, 3, 1),
('2026-08-03', '08:04:18', 'Asistencia', 'Manual', 9, 3, 1),
('2026-08-03', '08:10:00', 'Falta injustificada', 'Manual', 11, 3, 1),
('2026-08-03', '08:05:33', 'Asistencia', 'Biométrico Facial', 13, 3, 1),
('2026-08-04', '09:01:00', 'Asistencia', 'Biométrico Facial', 4, 6, 2),
('2026-08-04', '09:02:15', 'Asistencia', 'Manual', 6, 6, 2),
('2026-08-04', '09:08:40', 'Retardo', 'Manual', 10, 6, 2),
('2026-08-04', '09:03:20', 'Asistencia', 'Biométrico Facial', 12, 6, 2),
('2026-08-05', '08:00:50', 'Asistencia', 'Biométrico Facial', 1, 3, 1),
('2026-08-05', '08:02:10', 'Asistencia', 'Biométrico Facial', 2, 3, 1),
('2026-08-05', '08:03:00', 'Asistencia', 'Manual', 4, 3, 1),
('2026-08-05', '08:15:20', 'Retardo', 'Manual', 5, 3, 1),
('2026-08-05', '08:04:40', 'Asistencia', 'Biométrico Facial', 9, 3, 1),
('2026-08-05', '08:05:10', 'Asistencia', 'Manual', 11, 3, 1),
('2026-08-05', '08:06:00', 'Asistencia', 'Biométrico Facial', 13, 3, 1),
('2026-08-06', '10:01:00', 'Asistencia', 'Biométrico Facial', 2, 6, 4),
('2026-08-06', '10:02:30', 'Asistencia', 'Manual', 6, 6, 4),
('2026-08-06', '10:12:00', 'Retardo', 'Manual', 8, 6, 4),
('2026-08-06', '10:03:45', 'Asistencia', 'Biométrico Facial', 11, 6, 4),
('2026-08-06', '10:04:20', 'Asistencia', 'Manual', 14, 6, 4),
('2026-08-07', '08:01:30', 'Asistencia', 'Biométrico Facial', 1, 3, 3),
('2026-08-07', '08:02:40', 'Asistencia', 'Manual', 5, 3, 3),
('2026-08-07', '08:03:10', 'Asistencia', 'Biométrico Facial', 7, 3, 3),
('2026-08-07', '08:20:00', 'Falta injustificada', 'Manual', 10, 3, 3),
('2026-08-07', '08:04:50', 'Asistencia', 'Manual', 13, 3, 3),

-- Semana actual (lun 10 – mié 12 ago 2026) — alimenta weekly-attendance y summary
('2026-08-10', '08:01:05', 'Asistencia', 'Biométrico Facial', 1, 3, 1),
('2026-08-10', '08:02:18', 'Asistencia', 'Biométrico Facial', 2, 3, 1),
('2026-08-10', '08:03:40', 'Asistencia', 'Manual', 4, 3, 1),
('2026-08-10', '08:14:22', 'Retardo', 'Manual', 5, 3, 1),
('2026-08-10', '08:04:55', 'Asistencia', 'Biométrico Facial', 9, 3, 1),
('2026-08-10', '08:05:30', 'Asistencia', 'Manual', 11, 3, 1),
('2026-08-10', '08:06:10', 'Asistencia', 'Biométrico Facial', 13, 3, 1),
('2026-08-10', '08:07:00', 'Asistencia', 'Manual', 14, 3, 1),
('2026-08-10', '09:01:20', 'Asistencia', 'Biométrico Facial', 4, 4, 2),
('2026-08-10', '09:02:45', 'Asistencia', 'Manual', 6, 4, 2),
('2026-08-10', '09:03:10', 'Asistencia', 'Biométrico Facial', 10, 4, 2),
('2026-08-10', '09:18:00', 'Falta injustificada', 'Manual', 12, 4, 2),

('2026-08-11', '08:00:40', 'Asistencia', 'Biométrico Facial', 1, 3, 1),
('2026-08-11', '08:01:55', 'Asistencia', 'Biométrico Facial', 2, 3, 1),
('2026-08-11', '08:16:10', 'Retardo', 'Manual', 4, 3, 1),
('2026-08-11', '08:03:20', 'Asistencia', 'Manual', 5, 3, 1),
('2026-08-11', '08:04:00', 'Asistencia', 'Biométrico Facial', 9, 3, 1),
('2026-08-11', '08:05:25', 'Asistencia', 'Manual', 11, 3, 1),
('2026-08-11', '08:20:40', 'Falta injustificada', 'Manual', 13, 3, 1),
('2026-08-11', '10:01:10', 'Asistencia', 'Biométrico Facial', 2, 6, 4),
('2026-08-11', '10:02:30', 'Asistencia', 'Manual', 6, 6, 4),
('2026-08-11', '10:03:45', 'Asistencia', 'Biométrico Facial', 8, 6, 4),
('2026-08-11', '10:04:20', 'Asistencia', 'Manual', 11, 6, 4),
('2026-08-11', '10:05:00', 'Asistencia', 'Biométrico Facial', 14, 6, 4),
('2026-08-11', '11:01:00', 'Asistencia', 'Manual', 7, 5, 5),
('2026-08-11', '11:02:15', 'Asistencia', 'Biométrico Facial', 8, 5, 5),
('2026-08-11', '11:12:40', 'Retardo', 'Manual', 9, 5, 5),
('2026-08-11', '11:03:50', 'Asistencia', 'Manual', 12, 5, 5),
('2026-08-11', '11:04:30', 'Asistencia', 'Biométrico Facial', 14, 5, 5),

('2026-08-12', '08:01:00', 'Asistencia', 'Biométrico Facial', 1, 3, 1),
('2026-08-12', '08:02:20', 'Asistencia', 'Biométrico Facial', 2, 3, 1),
('2026-08-12', '08:03:15', 'Asistencia', 'Manual', 4, 3, 1),
('2026-08-12', '08:04:40', 'Asistencia', 'Manual', 5, 3, 1),
('2026-08-12', '08:15:10', 'Retardo', 'Manual', 9, 3, 1),
('2026-08-12', '08:05:50', 'Asistencia', 'Biométrico Facial', 11, 3, 1),
('2026-08-12', '08:06:30', 'Asistencia', 'Manual', 13, 3, 1),
('2026-08-12', '08:07:05', 'Asistencia', 'Biométrico Facial', 14, 3, 1),
('2026-08-12', '09:01:30', 'Asistencia', 'Manual', 4, 4, 2),
('2026-08-12', '09:02:40', 'Asistencia', 'Biométrico Facial', 6, 4, 2),
('2026-08-12', '09:03:55', 'Asistencia', 'Manual', 10, 4, 2),
('2026-08-12', '09:04:20', 'Asistencia', 'Biométrico Facial', 12, 4, 2),
('2026-08-12', '08:02:00', 'Asistencia', 'Manual', 1, 3, 3),
('2026-08-12', '08:03:10', 'Asistencia', 'Biométrico Facial', 5, 3, 3),
('2026-08-12', '08:04:25', 'Asistencia', 'Manual', 7, 3, 3),
('2026-08-12', '08:18:00', 'Retardo', 'Manual', 10, 3, 3),
('2026-08-12', '08:05:40', 'Asistencia', 'Biométrico Facial', 13, 3, 3);

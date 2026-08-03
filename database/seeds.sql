USE BAM_System;

INSERT INTO role (name, description) VALUES
('Administrador', 'Acceso total al sistema y reportes'),
('Profesor', 'Control de asistencia y gestión de cursos'),
('Prefecto', 'Encargado de la toma de asistencia biométrica');

INSERT INTO parents (name, lastname, surename, phone, email, password, dir_street, dir_col, dir_num) VALUES
('Carlos', 'Mendoza', 'Ruiz', '5551234567', 'carlos.mendoza@mail.com', '$2y$10$parent1', 'Av. Juárez', 'Centro', '12'),
('Gabriela', 'Espinoza', 'Luna', '5557654321', 'gabriela.espinoza@mail.com', '$2y$10$parent2', 'Calle Olivo', 'Del Valle', '45'),
('Manuel', 'Castro', 'Ortiz', '5559876543', 'manuel.castro@mail.com', '$2y$10$parent3', 'Calle Colima', 'Roma', '110');

INSERT INTO courses (name, description, category, start_date, end_date, time_duration) VALUES
('Programación en Python', 'Curso básico desde cero', 'Tecnología', '2026-01-15', '2026-06-15', '80 horas'),
('Diseño UI/UX', 'Principios de diseño de interfaces', 'Diseño', '2026-02-01', '2026-05-01', '50 horas'),
('Base de Datos SQL', 'Diseño y optimización de consultas', 'Tecnología', '2026-03-01', '2026-07-01', '60 horas');

INSERT INTO employees (id_employee, name, lastname, surename, email, password, phone, age, status, dir_street, dir_col, dir_num, role_id) VALUES
(1001, 'Ana', 'Gomez', 'Pérez', 'ana.gomez@bam.com', '$2y$10$xyz123', '5551112223', 35, 'Activo', 'Av. Reforma', 'Centro', '102', 1), 
(1002, 'Roberto', 'Sánchez', 'Díaz', 'roberto.sanchez@bam.com', '$2y$10$xyz456', '5553334445', 42, 'Activo', 'Calle Juarez', 'Del Valle', '405', 2), 
(1003, 'Lucía', 'Torres', 'Marín', 'lucia.torres@bam.com', '$2y$10$xyz789', '5555556667', 28, 'Activo', 'Av. Insurgentes', 'Roma', '78', 3);

INSERT INTO pre_register (name, lastname, surename, email, phone, course_id) VALUES
('Valeria', 'Rojas', 'Solís', 'valeria.rojas@mail.com', '5554443322', 1),
('Javier', 'Pacheco', 'Cruz', 'javier.pach@mail.com', '5559998877', 3);

INSERT INTO reports (name, generation_date, employee_id) VALUES
('Reporte de Asistencia Mensual - Mayo', '2026-05-31 18:00:00', 1),
('Auditoría de Alumnos Activos', '2026-06-01 09:30:00', 1);

INSERT INTO students (id_student, name, lastname, surename, date_of_birth, status, id_parent) VALUES
('BAM-2026-0001', 'Luis', 'Mendoza', 'Espinoza', '2010-03-14', 'Activo', 1),
('BAM-2026-0002', 'Sofía', 'Castro', 'Espinoza', '2009-07-22', 'Activo', 3),
('BAM-2026-0003', 'Diego', 'Mendoza', 'Luna', '2011-11-05', 'Inactivo', 2);

INSERT INTO biometric_information (face_vector, encryption_hash, enrollment_date, student_id) VALUES
('[0.123, -0.456, 0.789, 0.012]', 'hash_biometrico_encriptado_1', '2026-01-16 08:00:00', 1),
('[0.987, 0.654, -0.321, 0.111]', 'hash_biometrico_encriptado_2', '2026-02-02 08:15:00', 2);

INSERT INTO attendance (date, time, status, method, student_id, employee_id, course_id) VALUES
('2026-06-01', '08:02:15', 'Asistencia', 'Biométrico Facial', 1, 3, 1),
('2026-06-01', '08:05:40', 'Asistencia', 'Biométrico Facial', 2, 3, 1),
('2026-06-02', '08:21:00', 'Retardo', 'Manual', 1, 3, 3);

INSERT INTO student_tutor (start_date, end_date, status, student_id, employee_id) VALUES
('2026-01-15', '2026-06-15', 'Completado', 1, 2),
('2026-03-01', NULL, 'En Progreso', 2, 2);

INSERT INTO student_courses (student_id, course_id) VALUES
(1, 1), 
(1, 3), 
(2, 1), 
(3, 2); 

INSERT INTO employee_course (employee_id, course_id) VALUES
(2, 1), 
(2, 3);

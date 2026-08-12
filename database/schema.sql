CREATE DATABASE IF NOT EXISTS BAM_System;
 
USE BAM_System;


CREATE TABLE IF NOT EXISTS role (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS parents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    surename VARCHAR(100) NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    dir_street VARCHAR(150) NOT NULL,
    dir_col VARCHAR(100) NOT NULL,
    dir_num VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS courses(
   id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    time_duration VARCHAR(50) NOT NULL,
    days_of_week VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Activo'
);

CREATE TABLE IF NOT EXISTS employees(
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_employee VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    surename VARCHAR(100) NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR (255) NOT NULL,
    phone VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    status VARCHAR(100) NOT NULL,
    dir_street VARCHAR(100) NOT NULL,
    dir_col VARCHAR(100) NOT NULL,
    dir_num VARCHAR(100) NOT NULL,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES role (id)
);

CREATE TABLE IF NOT EXISTS reports(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    generation_date DATETIME NOT NULL,
    employee_id INT,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
);

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    -- Matrícula autogenerada por el backend (formato BAM-<año>-<secuencia>);
    -- nunca se acepta un valor de matrícula enviado por el cliente.
    id_student VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    surename VARCHAR(100) NULL,
    -- Los alumnos son menores de edad: sin credenciales ni contacto propio;
    -- esos datos viven exclusivamente en su tutor (parents).
    date_of_birth DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_parent INT NOT NULL,
    FOREIGN KEY (id_parent) REFERENCES parents (id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS pre_register (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    surename VARCHAR(100) NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS biometric_information (
    id INT PRIMARY KEY AUTO_INCREMENT,
    face_vector TEXT NOT NULL,
    encryption_hash VARCHAR(255) NOT NULL,
    enrollment_date DATETIME NOT NULL,
    student_id INT NOT NULL UNIQUE,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    time TIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    method VARCHAR(50) NOT NULL,
    student_id INT NOT NULL,
    employee_id INT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE RESTRICT,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student_tutor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    status VARCHAR(50) NOT NULL,
    student_id INT NOT NULL,
    employee_id INT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE RESTRICT,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS student_courses (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS employee_course (
    employee_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (employee_id, course_id),
    FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS non_working_days (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL UNIQUE,          
    description VARCHAR(150) NOT NULL  
);
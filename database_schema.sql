-- Crear base de datos
CREATE DATABASE IF NOT EXISTS sistema_biblioteca;
USE sistema_biblioteca;

-- Tabla de libros
CREATE TABLE IF NOT EXISTS libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    fecha_publicacion INT,
    disponible BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo ENUM('Estudiante', 'Profesor') NOT NULL,
    carrera_depto VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de préstamos
CREATE TABLE IF NOT EXISTS prestamos (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    id_libro INT NOT NULL,
    id_usuario VARCHAR(50) NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE NULL,
    devuelto BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de ejemplo
INSERT INTO libros (titulo, autor, fecha_publicacion, disponible) VALUES
('Cien años de soledad', 'Gabriel García Márquez', 1967, TRUE),
('1984', 'George Orwell', 1949, TRUE),
('El Quijote', 'Miguel de Cervantes', 1605, TRUE);

INSERT INTO usuarios (id_usuario, nombre, tipo, carrera_depto) VALUES
('EST001', 'Ana García', 'Estudiante', 'Ingeniería Informática'),
('PROF001', 'Carlos López', 'Profesor', 'Departamento de Literatura');

-- Crear usuario para la aplicación (ejecutar en MySQL como root)
CREATE USER IF NOT EXISTS 'biblioteca_user'@'localhost' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON sistema_biblioteca.* TO 'biblioteca_user'@'localhost';
FLUSH PRIVILEGES;
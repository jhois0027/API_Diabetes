CREATE DATABASE IF NOT EXISTS diabetes;
USE diabetes;

CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    glucosa INT NOT NULL,
    edad INT NOT NULL,
    riesgo INT NOT NULL -- 0: No riesgo, 1: Riesgo
);

-- Insertar datos iniciales para que el entrenamiento tenga de donde sacar
INSERT INTO pacientes (glucosa, edad, riesgo) VALUES 
(85, 25, 0), (190, 50, 1), (110, 30, 0), (160, 45, 1),
(88, 22, 0), (155, 60, 1), (105, 35, 0), (145, 55, 1),
(92, 28, 0), (180, 65, 1), (120, 40, 0), (170, 48, 1),
(75, 20, 0), (200, 70, 1), (115, 33, 0), (130, 52, 1);
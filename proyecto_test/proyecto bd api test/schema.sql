-- =====================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- API de Recomendaciones Escolares
-- =====================================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS escuela_recomendaciones;
USE escuela_recomendaciones;

-- =====================================================
-- TABLA: ESCUELAS
-- =====================================================
CREATE TABLE IF NOT EXISTS escuelas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    ciudad VARCHAR(100),
    nivel VARCHAR(50),
    calificacion DECIMAL(3,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ciudad (ciudad),
    INDEX idx_nivel (nivel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: RECOMENDACIONES
-- =====================================================
CREATE TABLE IF NOT EXISTS recomendaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    escuela_id INT NOT NULL,
    estudiante VARCHAR(100) NOT NULL,
    motivo TEXT,
    calificacion INT CHECK(calificacion >= 1 AND calificacion <= 5),
    estado VARCHAR(20) DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (escuela_id) REFERENCES escuelas(id) ON DELETE CASCADE,
    INDEX idx_escuela_id (escuela_id),
    INDEX idx_calificacion (calificacion),
    INDEX idx_estado (estado),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- DATOS DE EJEMPLO
-- =====================================================

-- Insertar escuelas de ejemplo
INSERT INTO escuelas (nombre, ciudad, nivel, calificacion) VALUES
('Escuela Primaria Central', 'Lima', 'primaria', 4.7),
('Colegio Nacional Secundario', 'Lima', 'secundaria', 4.5),
('Instituto Técnico Profesional', 'Arequipa', 'técnico', 4.3),
('Escuela Rural San Martín', 'Ayacucho', 'primaria', 3.8),
('Colegio Bilingüe Virtual', 'Lima', 'secundaria', 4.9);

-- Insertar recomendaciones de ejemplo
INSERT INTO recomendaciones (escuela_id, estudiante, motivo, calificacion, estado) VALUES
(1, 'Juan Pérez López', 'Excelente educación y profesores dedicados', 5, 'activa'),
(1, 'María García Sánchez', 'Buenas instalaciones y ambiente seguro', 4, 'activa'),
(2, 'Carlos Rodríguez', 'Programa académico integral', 5, 'activa'),
(2, 'Laura Martínez', 'Biblioteca bien equipada', 4, 'actualizada'),
(3, 'Pedro Flores', 'Formación técnica de calidad', 4, 'activa'),
(4, 'Ana Torres', 'Dedicados a estudiantes de zonas rurales', 3, 'activa'),
(5, 'Roberto Soto', 'Capacidades en idiomas excepcionales', 5, 'activa');

-- =====================================================
-- VISTAS ÚTILES (OPCIONAL)
-- =====================================================

-- Vista para obtener recomendaciones con datos de escuela
CREATE OR REPLACE VIEW v_recomendaciones_con_escuela AS
SELECT 
    r.id,
    r.escuela_id,
    e.nombre as escuela_nombre,
    e.ciudad,
    e.nivel,
    r.estudiante,
    r.motivo,
    r.calificacion,
    r.estado,
    r.created_at
FROM recomendaciones r
JOIN escuelas e ON r.escuela_id = e.id
ORDER BY r.created_at DESC;

-- Vista para estadísticas por escuela
CREATE OR REPLACE VIEW v_estadisticas_escuelas AS
SELECT 
    e.id,
    e.nombre,
    e.ciudad,
    e.nivel,
    COUNT(r.id) as total_recomendaciones,
    AVG(r.calificacion) as calificacion_promedio,
    MAX(r.calificacion) as calificacion_maxima,
    MIN(r.calificacion) as calificacion_minima
FROM escuelas e
LEFT JOIN recomendaciones r ON e.id = r.escuela_id
GROUP BY e.id, e.nombre, e.ciudad, e.nivel;

-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS (OPCIONAL)
-- =====================================================

-- Procedimiento para obtener recomendaciones por rango de calificación
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_recomendaciones_por_calificacion(
    IN p_min_cal INT,
    IN p_max_cal INT
)
BEGIN
    SELECT * FROM v_recomendaciones_con_escuela
    WHERE calificacion BETWEEN p_min_cal AND p_max_cal
    ORDER BY calificacion DESC, created_at DESC;
END//
DELIMITER ;

-- Procedimiento para obtener estadísticas de una escuela
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_estadisticas_escuela(
    IN p_escuela_id INT
)
BEGIN
    SELECT * FROM v_estadisticas_escuelas
    WHERE id = p_escuela_id;
END//
DELIMITER ;

-- =====================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- =====================================================

-- Los índices principales ya están creados en las tablas,
-- pero aquí hay algunos índices adicionales opcionales

-- Índice combinado para búsquedas frecuentes
ALTER TABLE recomendaciones ADD INDEX idx_escuela_estado (escuela_id, estado);
ALTER TABLE recomendaciones ADD INDEX idx_calificacion_estado (calificacion, estado);

-- =====================================================
-- COMENTARIOS
-- =====================================================

-- Para ejecutar este script en MySQL:
-- mysql -u root -p < schema.sql
-- 
-- O desde SQLyog/Workbench:
-- 1. Abrir este archivo
-- 2. Ejecutar todo el contenido
-- 3. Verificar que se crean las tablas correctamente

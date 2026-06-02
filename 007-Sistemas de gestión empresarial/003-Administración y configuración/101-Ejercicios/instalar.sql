CREATE DATABASE IF NOT EXISTS ticketing_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ticketing_db;

-- Usuarios administradores
CREATE TABLE admin_users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Categorías
CREATE TABLE categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  is_active TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB;

-- Estados
CREATE TABLE statuses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  is_active TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB;

-- Tickets
CREATE TABLE tickets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  requester_name VARCHAR(120) NOT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  category_id INT NOT NULL,
  status_id INT NOT NULL,
  attachment_original_name VARCHAR(255) NULL,
  attachment_stored_name VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NULL DEFAULT NULL,
  INDEX idx_created_at (created_at),
  INDEX idx_category (category_id),
  INDEX idx_status (status_id),
  INDEX idx_requester_name (requester_name),
  CONSTRAINT fk_tickets_category
    FOREIGN KEY (category_id) REFERENCES categories(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_tickets_status
    FOREIGN KEY (status_id) REFERENCES statuses(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =========================
-- DATOS DE MUESTRA
-- =========================

INSERT INTO categories (name, is_active) VALUES
('Acceso / Login', 1),
('Email', 1),
('Impresoras', 1),
('Red / WiFi', 1),
('Software interno', 1);

INSERT INTO statuses (name, is_active) VALUES
('Nuevo', 1),
('En progreso', 1),
('Pendiente de usuario', 1),
('Resuelto', 1),
('Cerrado', 1);

-- IMPORTANTE:
-- password_hash está pensado para un hash de Werkzeug (pbkdf2:sha256:...)
-- Para que el login funcione, crea el usuario desde Flask con el endpoint /admin/init-demo
-- (ver app.py). Aun así dejamos un ejemplo de username:
INSERT INTO admin_users (username, password_hash) VALUES
('admin', 'REEMPLAZAR_DESDE_FLASK_INIT');

INSERT INTO tickets (requester_name, title, description, category_id, status_id, created_at)
VALUES
('Ana Gómez', 'No puedo iniciar sesión', 'Al introducir mi usuario, vuelve a la pantalla de login.', 1, 1, NOW()),
('Carlos Pérez', 'No imprime en la oficina', 'La impresora aparece offline y no imprime ningún documento.', 3, 2, NOW()),
('Marta Ruiz', 'WiFi intermitente', 'Se corta cada pocos minutos en la sala de reuniones.', 4, 1, NOW());
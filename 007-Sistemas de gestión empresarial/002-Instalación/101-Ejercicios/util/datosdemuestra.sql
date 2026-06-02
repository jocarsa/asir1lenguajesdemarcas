PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- -----------------------
-- USERS (login)
-- -----------------------
INSERT OR IGNORE INTO users (id, username, password_hash, created_at) VALUES
(1, 'jocarsa', 'scrypt:32768:8:1$FdZi7t3ZN7Q3QkrQ$81647af6bf437deed4dd9b479a796ece39462c5c06d69dd1baa8e803e2256e5011b697af875f2beb66b008edd9686f2e9e59b3acea38f28e47abee768d080125', '2026-02-26T08:00:00');

-- -----------------------
-- CLIENTES
-- -----------------------
INSERT INTO clientes (id, nombre, apellidos, email, telefono, direccion, created_at) VALUES
(1, 'Lucía', 'Martínez Soto', 'lucia.martinez@example.com', '+34 600 111 222', 'C/ Colón 12, Valencia', '2026-02-20T10:15:00'),
(2, 'Álvaro', 'Gómez Pérez', 'alvaro.gomez@example.com', '+34 600 333 444', 'Av. Aragón 55, Valencia', '2026-02-20T11:02:00'),
(3, 'Carmen', 'Navarro Ruiz', 'carmen.navarro@example.com', '+34 600 555 666', 'C/ Xàtiva 3, Valencia', '2026-02-21T09:20:00'),
(4, 'Javier', 'Sánchez López', 'javier.sanchez@example.com', '+34 600 777 888', 'C/ Serranos 18, Valencia', '2026-02-21T12:40:00'),
(5, 'Elena', 'Torres Gil', 'elena.torres@example.com', '+34 600 999 000', 'Pl. Ayuntamiento 1, Valencia', '2026-02-22T08:35:00'),
(6, 'Marcos', 'Hernández Vidal', 'marcos.hernandez@example.com', '+34 611 123 456', 'C/ Jesús 27, Valencia', '2026-02-22T13:10:00');

-- -----------------------
-- PRODUCTOS
-- -----------------------
INSERT INTO productos (id, nombre, sku, precio, stock, created_at) VALUES
(1, 'Licencia Microsaas Básica (mensual)', 'MS-BASIC-M', 19.90, 9999, '2026-02-20T10:20:00'),
(2, 'Licencia Microsaas Pro (mensual)',   'MS-PRO-M',   39.90, 9999, '2026-02-20T10:21:00'),
(3, 'Licencia Microsaas Empresa (mensual)','MS-ENT-M',  89.90, 9999, '2026-02-20T10:22:00'),
(4, 'Paquete Soporte 1h',                 'SUP-1H',     45.00,   50, '2026-02-21T09:00:00'),
(5, 'Paquete Soporte 5h',                 'SUP-5H',    199.00,   25, '2026-02-21T09:01:00'),
(6, 'Implantación Inicial',               'SETUP-INIT', 350.00,   10, '2026-02-21T09:02:00'),
(7, 'Formación (2h)',                     'TRN-2H',     80.00,   30, '2026-02-22T10:00:00'),
(8, 'Módulo extra: Informes',             'ADD-RPT',    12.00,  100, '2026-02-22T10:01:00');

-- -----------------------
-- PEDIDOS (cabecera)
-- -----------------------
INSERT INTO pedidos (id, cliente_id, fecha, estado, notas, created_at) VALUES
(1, 1, '2026-02-23', 'confirmado', 'Alta inicial y licencia básica.', '2026-02-23T09:15:00'),
(2, 2, '2026-02-23', 'confirmado', 'Pro + soporte 1h.',             '2026-02-23T10:05:00'),
(3, 3, '2026-02-24', 'enviado',    'Empresa + implantación.',        '2026-02-24T11:20:00'),
(4, 5, '2026-02-25', 'borrador',   'Pendiente de confirmación.',     '2026-02-25T16:40:00'),
(5, 6, '2026-02-26', 'confirmado', 'Pro + formación.',              '2026-02-26T08:10:00');

-- -----------------------
-- LÍNEAS DE PEDIDO
-- -----------------------
INSERT INTO pedido_lineas (id, pedido_id, producto_id, cantidad, precio_unitario) VALUES
-- Pedido 1 (Lucía)
(1, 1, 1, 1, 19.90),
(2, 1, 6, 1, 350.00),

-- Pedido 2 (Álvaro)
(3, 2, 2, 1, 39.90),
(4, 2, 4, 1, 45.00),

-- Pedido 3 (Carmen)
(5, 3, 3, 1, 89.90),
(6, 3, 6, 1, 350.00),
(7, 3, 5, 1, 199.00),

-- Pedido 4 (Elena) borrador
(8, 4, 1, 1, 19.90),
(9, 4, 8, 1, 12.00),

-- Pedido 5 (Marcos)
(10, 5, 2, 1, 39.90),
(11, 5, 7, 1, 80.00);

COMMIT;
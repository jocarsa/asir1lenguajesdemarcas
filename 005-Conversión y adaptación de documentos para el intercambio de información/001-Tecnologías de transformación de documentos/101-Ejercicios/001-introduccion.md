Entramos en DBBrowser
Creamos una base de datos
La base de datos se va a llamar empresa
Creamos una tabla llamada clientes
Creamos las columnas:
-id PK AI
-nombre
-apellidos
-email

CREATE TABLE "clientes" (
	"id"	INTEGER,
	"nombre"	TEXT,
	"apellidos"	TEXT,
	"email"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO clientes (nombre, apellidos, email) VALUES
('Ana', 'García López', 'ana.garcia@example.com'),
('Luis', 'Martínez Pérez', 'luis.martinez@example.com'),
('María', 'Sánchez Ruiz', 'maria.sanchez@example.com'),
('Carlos', 'Fernández Gómez', 'carlos.fernandez@example.com'),
('Laura', 'Jiménez Torres', 'laura.jimenez@example.com'),
('Javier', 'Moreno Díaz', 'javier.moreno@example.com'),
('Carmen', 'Navarro Romero', 'carmen.navarro@example.com'),
('David', 'Ruiz Molina', 'david.ruiz@example.com'),
('Elena', 'Hernández Castro', 'elena.hernandez@example.com'),
('Pablo', 'Ortega Vidal', 'pablo.ortega@example.com'),
('Isabel', 'Ramos León', 'isabel.ramos@example.com'),
('Sergio', 'Gil Cabrera', 'sergio.gil@example.com'),
('Patricia', 'Flores Soto', 'patricia.flores@example.com'),
('Miguel', 'Vega Núñez', 'miguel.vega@example.com'),
('Raquel', 'Campos Blanco', 'raquel.campos@example.com'),
('Alberto', 'Méndez Cruz', 'alberto.mendez@example.com'),
('Silvia', 'Prieto Lozano', 'silvia.prieto@example.com'),
('Antonio', 'Herrera Peña', 'antonio.herrera@example.com'),
('Natalia', 'Iglesias Fuentes', 'natalia.iglesias@example.com'),
('Fernando', 'Cano Aguilar', 'fernando.cano@example.com');

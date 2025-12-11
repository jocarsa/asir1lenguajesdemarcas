Empezamos suave:

1.-Vamos a crear una base de datos
Pero de la forma más sencilla posible
Usando DB Browser (sqlitebrowser)

2.-Abrimos DB browser
(el programa que descargamos ayer en clase)

3.-Creamos una nueva base de datos
Arriba a la izquierda: botón "Nueva base de datos"
Las extensiones en SQLite preferidas son
.db
.sqlite
.sqlite3
(blog.db)

4.-Nombre de la tabla: entradas
Campos:

CREATE TABLE "entradas" (
	"id"	INTEGER,
	"titulo"	TEXT,
	"fecha"	TEXT,
	"autor"	TEXT,
	"categoria"	TEXT,
	"contenido"	TEXT,
	"imagen"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

5.-Cada operación que hagáis, le dais al botón "Guardar cambios"











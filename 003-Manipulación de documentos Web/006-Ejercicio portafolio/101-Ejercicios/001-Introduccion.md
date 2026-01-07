Un portafolio es una colección de tus trabajos más destacados
Junto con el CV, es la clave para poder conseguir trabajo

El objetivo del portafolio es mostrar lo que sabes hacer
El portafolio es una excusa para crear el siguiente ejercicio

Vamos a crear un portafolio web

1.-Primer paso:
Creamos la base de datos
Seguimos de momento en SQLite
Seguimos con un ejercicio en el que hacemos SELECT
-Abrimos DBBrowser (el cliente sqlite que instalásteis el otro día)
-Creamos una base de datos llamada portafolio - la guardamos como portafolio.db
-Creamos una tabla llamada "piezas"
	-La tabla tendrá las siguientes columnas:
  	-id PRIMARY AUTO
    -titulo TEXT
    -descripcion TEXT
    -imagen TEXT
    -fecha TEXT
    
CREATE TABLE "piezas" (
	"id"	INTEGER,
	"titulo"	TEXT,
	"descripcion"	TEXT,
	"imagen"	TEXT,
	"fecha"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

Pulsamos el botón "guardar"





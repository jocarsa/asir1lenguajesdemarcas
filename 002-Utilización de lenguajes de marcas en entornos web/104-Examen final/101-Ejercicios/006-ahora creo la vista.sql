CREATE VIEW piezas_y_categorias AS 
SELECT 
Categorias.titulo AS categoriatitulo,
Categorias.descripcion AS categoriadescripcion,
Piezas.titulo AS piezatitulo,
Piezas.descripcion AS piezadescripcion,
imagen,
url
FROM Piezas
LEFT JOIN Categorias
ON Piezas.id_categoria = Categorias.Identificador;

SELECT * FROM piezas_y_categorias;

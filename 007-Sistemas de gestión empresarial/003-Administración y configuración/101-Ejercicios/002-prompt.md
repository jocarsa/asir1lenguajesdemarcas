Quiero crear un sistema de gestión empresarial.
Estará realizado con Python+flask y MySQL en el back. Estará
realizado con HTML y CSS en el front. No llevará Javascript.
Es un sistema de ticketing. Tendrá dos bloques:
-Por una parte, en un front, el usuario externo tendrá un
formulario para poner tickets con incidencias. El ticket
tendrá un desplegable de categorias. El usuario deberá
introducir su nombre, un titulo de la incidencia, y una 
descripción de la incidencia. Se podrá adjuntar un archivo
(captura de pantalla)
-Por otra parte, habrá un panel de control que tendrá
gestión de las categorías CRUD, y un panel CRUD
para las incidencias recibidas, además de poder cambiar su 
estado (otro CRUD para estados)
Además el listado de incidencias tendrá múltiples filtros
(por estado de incidencia, por categoría, y buscadores
generales, por ejemplo por nombre). Además necesitaré un login
para el panel de administración, y una tabla en MySQL.
Dame: el código MySQL con create table, e insert into con datos 
de muestra, el app.py y los html/css necesarios
import sqlite3 # Viene preintegrada con el sistema

# 1. Conectar (si no existe, la BD se crea automáticamente)
conexion = sqlite3.connect("clientes.db")
cursor = conexion.cursor() # cursor necesario para movernos por la base de datos

# 2. Mostrar el cliente insertado
cursor.execute("SELECT * FROM clientes")
clientes = cursor.fetchall() 	# Almaceno lo que devuelve BD en lista
print(clientes)								# Imprimo la lista

# Cerrar conexión
conexion.close()

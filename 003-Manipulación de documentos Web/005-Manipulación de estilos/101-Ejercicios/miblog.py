# Ejecutad esto en terminal 
import sqlite3 														# Uso la librería SQLite3
from flask import Flask,render_template		#I Uso la libreria flask para crear web

app = Flask(__name__)											#I Creo una aplicación web

@app.get("/")															#I Cuando alguien pida la raiz de la web								
def inicio():															#I Ejecuto esta funcion
	conexion = sqlite3.connect("blog.db")		# Me conecto a la base de datos
	conexion.row_factory = sqlite3.Row 			# CONVIERTE EN DICCIONARIO
	cursor = conexion.cursor()							# Creo un cursor para pedirle cosas a la bd
	cursor.execute("SELECT * FROM entradas")# Le digo lo que quiero
	clientes = cursor.fetchall()						# Ejecuto la petición contra la base de datos
	
	lista = []															# Creo una lista vacía
 
	for fila in clientes:										# Y para cada fila de la base de datos
		lista.append(dict(fila))   						# Añado esa fila a la lista

	print(lista)														# Imprimo la lista

	
	return render_template("blog.html",datos=lista)	#I renderizo la web

if __name__ == "__main__":								#I Si estoy en el archivo principal		
	app.run(debug=True)										#I Pongo en marcha la web
  

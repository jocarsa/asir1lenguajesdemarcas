# pip install flask - Visual Studio
# pip3 install flask --break-system-packages - Linux

from flask import Flask								# Importamos la libreria Flask

app = Flask(__name__)									# Creamos una nueva aplicación

@app.get("/")													# Escuchamos en la raiz de la web
def index():													# Creamos una entrada
    return "Hola mundo desde Flask"		# Devolvemos algo minimo

if __name__ == "__main__":						# Si nos encontramos en el archivo principal
    app.run(debug=True)								# Ejecutamos la aplicación
    

# Primero navego a la carpeta indicada (o le dais a play los niños del Visual Studio)
# Si estais en linea de comandos, python3 "001-flask sencillo.py"
# Ahora abrimos un navegador web
# y entramos la url: http://127.0.0.1:5000
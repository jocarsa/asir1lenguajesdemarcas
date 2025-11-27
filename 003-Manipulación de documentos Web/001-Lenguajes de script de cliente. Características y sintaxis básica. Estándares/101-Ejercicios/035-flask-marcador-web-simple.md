Enunciado

Crea una pequeña aplicación web con Flask para mostrar un mensaje sencillo sobre un partido.

Importa Flask y crea la aplicación como en los ejemplos.

Define una ruta en "/" que devuelva un texto como:
"Bienvenido al marcador online de tu liga".

Ejecuta la aplicación con app.run(debug=True).

Este ejercicio usa solo lo que ya aparece en tus archivos: importación de Flask, creación de app, ruta con @app.get("/") y app.run(debug=True).

Solución
from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    return "Bienvenido al marcador online de tu liga"

if __name__ == "__main__":
    app.run(debug=True)

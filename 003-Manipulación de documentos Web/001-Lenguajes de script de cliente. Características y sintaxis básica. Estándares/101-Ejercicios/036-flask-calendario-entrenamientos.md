Enunciado

Crea una aplicación Flask que muestre un calendario de entrenamientos de un mes, similar al ejemplo de calendario que ya tienes, pero con un título y estilos simples.

Usa from flask import Flask, crea la aplicación y define la ruta "/".

En la ruta:

Crea una cadena cadena con estilos CSS sencillos.

Usa un bucle for con range(1,31) para generar 30 días.

En cada día, añade un div con el número de día.

Devuelve la cadena.

Solución
from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    cadena = '''
      <style>
        .dia{
          width:40px;
          height:40px;
          border:1px solid black;
          display:inline-block;
          text-align:center;
          line-height:40px;
          margin:2px;
        }
      </style>
      <h1>Calendario de entrenamientos</h1>
    '''
    for dia in range(1,31):
        cadena = cadena + "<div class='dia'>" + str(dia) + "</div>"
    return cadena

if __name__ == "__main__": 
    app.run(debug=True)

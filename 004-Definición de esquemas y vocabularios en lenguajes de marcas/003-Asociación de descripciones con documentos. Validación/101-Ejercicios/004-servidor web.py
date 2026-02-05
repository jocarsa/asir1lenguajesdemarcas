import json
from flask import Flask

app = Flask(__name__)

@app.get("/")	
def inicio():
  archivo = open("persona.json",'r')
  contenido = json.load(archivo)
  return "<p>"+contenido['nombre']+"</p>"
  archivo.close()

if __name__ == "__main__":								
	app.run(debug=True)	
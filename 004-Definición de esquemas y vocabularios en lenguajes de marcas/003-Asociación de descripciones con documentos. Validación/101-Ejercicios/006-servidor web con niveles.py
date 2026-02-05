import json
from flask import Flask,render_template

app = Flask(__name__)

@app.get("/")	
def inicio():
  archivo = open("curriculum.json",'r')
  contenido = json.load(archivo)
  
  return render_template("no tan sencillo.html",contenido=contenido)

  archivo.close()

if __name__ == "__main__":								
	app.run(debug=True)	
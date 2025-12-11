from flask import Flask,render_template					

app = Flask(__name__)					

datos = {
  'nombre':'Jose Vicente',
  'apellidos':'Carratala Sanchis',
}

@app.get("/")										
def inicio():										
    return render_template("masdatos.html",misdatos=datos)

if __name__ == "__main__":				
    app.run(debug=True)	
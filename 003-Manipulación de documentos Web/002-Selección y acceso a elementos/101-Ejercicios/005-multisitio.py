from flask import Flask,render_template					

app = Flask(__name__)					

@app.get("/")										
def inicio():										
    return render_template("inicio.html")
  
@app.get("/sobremi")										
def sobremi():										
    return render_template("sobremi.html")
  
@app.get("/contacto")										
def contacto():										
    return render_template("contacto.html")

if __name__ == "__main__":				
    app.run(debug=True)	
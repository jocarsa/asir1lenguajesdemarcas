from flask import Flask,render_template					

app = Flask(__name__)					

datos = {'nombre':'Jose Vicente'}

@app.get("/")										
def inicio():										
    return render_template("datos.html",misdatos=datos)

if __name__ == "__main__":				
    app.run(debug=True)	
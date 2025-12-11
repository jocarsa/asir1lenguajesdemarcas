from flask import Flask,render_template # NUEVO						

app = Flask(__name__)					

@app.get("/")										
def index():										
    return render_template("004-deseable.html") # NUEVO

if __name__ == "__main__":				
    app.run(debug=True)			
    

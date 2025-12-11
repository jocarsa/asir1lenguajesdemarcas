# pip install flask - Visual Studio
# pip3 install flask --break-system-packages - Linux

from flask import Flask						

app = Flask(__name__)					

@app.get("/")										
def index():										
    return "<h1>Hola mundo desde Flask</h1>"		# NUEVO ##############

if __name__ == "__main__":				
    app.run(debug=True)			
    

# Primero navego a la carpeta indicada (o le dais a play los niños del Visual Studio)
# Si estais en linea de comandos, python3 "001-flask sencillo.py"
# Ahora abrimos un navegador web
# y entramos la url: http://127.0.0.1:5000
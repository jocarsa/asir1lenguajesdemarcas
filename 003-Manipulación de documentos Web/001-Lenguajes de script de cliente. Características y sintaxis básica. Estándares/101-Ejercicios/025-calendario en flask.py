from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
	cadena = '''
      <style>
        .dia{width:30px;height:30px;border:1px solid black;display:inline-block;}
      </style>
    '''
	for dia in range(1,31):
		cadena += "<div class='dia'>"+str(dia)+"</div>"
	return cadena

if __name__ == "__main__":
	app.run(debug=True)

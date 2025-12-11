from flask import Flask						

app = Flask(__name__)					

@app.get("/")										
def index():										
    return '''
    <!docytpe html>
    <html>
    	<head>
      </head>
      <body>
      	<p>Hola mundo desde Python</p>
      </body>
    </html>
    ''' ############# NUEVO

if __name__ == "__main__":				
    app.run(debug=True)			
    

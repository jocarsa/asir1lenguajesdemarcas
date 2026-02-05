import json

archivo = open("persona.json",'r')

contenido = json.load(archivo)

print(contenido)

archivo.close()
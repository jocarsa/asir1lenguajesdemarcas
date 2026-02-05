import json

archivo = open("persona.json",'r')

contenido = json.load(archivo)

print("Mi nombre es",contenido['nombre'])
print("Mis apellidos son",contenido['apellidos'])
print("Mi correo es",contenido['email'])

archivo.close()
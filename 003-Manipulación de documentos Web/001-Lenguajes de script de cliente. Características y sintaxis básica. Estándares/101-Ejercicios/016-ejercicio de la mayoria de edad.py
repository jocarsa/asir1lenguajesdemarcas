# En un programa, primero da la bienvenida

print("Calculadora fantástica de la mayoría de edad")
print("por Jose Vicente Carratalá")

# A continuación, toma datos de entrada

edad = input("Introduce tu edad: ")

# Ahora realiza cálculos con esos datos

edad_en_entero = int(edad)
mensaje = ""

if edad_en_entero < 18:
  mensaje = "Eres menor de edad"
else:
  mensaje = "Eres mayor de edad"
  
# Por último, ofrece una salida

print(mensaje)



  

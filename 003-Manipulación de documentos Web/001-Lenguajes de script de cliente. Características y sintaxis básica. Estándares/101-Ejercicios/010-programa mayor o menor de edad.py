# En un programa, primero da la bienvenida

print("Programa maravilloso calculador de la mayoría de edad")
print("por Jose Vicente Carratala")

# A continuación, toma datos de entrada

edad = input("Indica tu edad: ")    # Pedimos un dato de entrada
edad_en_entero = int(edad)          # Lo convertimos a entero

# Ahora realiza cálculos con esos datos

menor_de_edad = edad_en_entero < 18
mayor_de_edad = edad_en_entero >= 18

# Por último, ofrece una salida

print("¿Eres menor de edad?",menor_de_edad)
print("¿Eres mayor de edad?",mayor_de_edad)




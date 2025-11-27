Enunciado

En un evento deportivo, solo pueden acceder a una zona especial las personas mayores de edad (18 o más).

Pide por teclado la edad de la persona.

Convierte la edad a int.

Usa una estructura condicional if/else para:

Mostrar "Puedes acceder a la zona especial" si la edad es mayor o igual a 18.

Mostrar "No puedes acceder a la zona especial" en caso contrario.

Solución
# Control de acceso a una zona especial en un evento deportivo

print("Control de acceso")
print("Por Jose Vicente (ejemplo)")

# Entrada
edad_texto = input("Introduce tu edad: ")

# Conversión
edad = int(edad_texto)

# Decisión
if edad >= 18:
    print("Puedes acceder a la zona especial")
else:
    print("No puedes acceder a la zona especial")

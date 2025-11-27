Enunciado

Se quiere clasificar el rendimiento de un jugador de baloncesto según los puntos anotados en un partido:

Menos de 10 puntos: "Rendimiento bajo"

Entre 10 y 19 puntos: "Rendimiento medio"

Entre 20 y 29 puntos: "Rendimiento alto"

30 puntos o más: "Rendimiento estrella"

Pide por teclado los puntos anotados.

Convierte a int.

Usa if, elif y else para mostrar el mensaje correcto.

Solución
# Clasificación del rendimiento de un jugador

print("Clasificador de rendimiento")
print("Por Jose Vicente (ejemplo)")

puntos_texto = input("Introduce los puntos anotados por el jugador: ")
puntos = int(puntos_texto)

if puntos < 10:
    print("Rendimiento bajo")
elif puntos < 20:
    print("Rendimiento medio")
elif puntos < 30:
    print("Rendimiento alto")
else:
    print("Rendimiento estrella")


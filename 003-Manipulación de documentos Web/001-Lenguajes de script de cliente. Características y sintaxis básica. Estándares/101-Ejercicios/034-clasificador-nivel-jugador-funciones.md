Enunciado

Crea un programa que clasifique el nivel de un jugador según su puntuación total en un videojuego deportivo.

Reglas:

Menos de 1000 puntos: "Principiante"

Entre 1000 y 4999 puntos: "Intermedio"

5000 puntos o más: "Avanzado"

Crea una función clasificarNivel(puntos) que:

Reciba los puntos.

Use if, elif y else.

Devuelva una cadena con el nivel.

En el programa principal:

Pide los puntos por teclado.

Convierte a int.

Llama a la función y muestra el resultado.

Solución
# Clasificador de nivel de jugador

def clasificarNivel(puntos):
    """
    Clasifica el nivel de un jugador según sus puntos.
    """
    if puntos < 1000:
        return "Principiante"
    elif puntos < 5000:
        return "Intermedio"
    else:
        return "Avanzado"

print("Clasificador de nivel de jugador")
puntos_texto = input("Introduce los puntos del jugador: ")
puntos = int(puntos_texto)

nivel = clasificarNivel(puntos)

print("Nivel del jugador:", nivel)

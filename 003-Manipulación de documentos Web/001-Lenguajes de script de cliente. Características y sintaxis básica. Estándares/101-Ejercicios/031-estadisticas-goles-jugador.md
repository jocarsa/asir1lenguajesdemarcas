Enunciado

Queremos calcular las estadísticas de goles de un jugador en una serie de 5 partidos.

Usa un bucle for que vaya de 1 a 5.

En cada iteración, pide por teclado los goles anotados en ese partido y conviértelos a int.

Ve acumulando los goles en una variable total.

Al final, muestra:

El total de goles.

La media de goles por partido (total dividido entre 5).

Solución
# Estadísticas de goles de un jugador

print("Estadísticas de goles")
print("Por Jose Vicente (ejemplo)")

total_goles = 0

for partido in range(1,6):
    goles_texto = input("Introduce los goles del partido " + str(partido) + ": ")
    goles = int(goles_texto)
    total_goles = total_goles + goles

media = total_goles / 5

print("Total de goles en la serie:", total_goles)
print("Media de goles por partido:", media)

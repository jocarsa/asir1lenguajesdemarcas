Crea un programa que muestre el marcador final de un partido de fútbol.

Declara dos variables para los goles del Equipo A y del Equipo B.

Muestra por pantalla un mensaje con este formato:

Partido terminado
Equipo A: X goles
Equipo B: Y goles
Diferencia de goles: Z


La diferencia de goles se calcula restando los goles del Equipo B a los del Equipo A.

No se piden entradas por teclado en este ejercicio: puedes asignar tú los valores a las variables.

Solución
# Marcador de un partido de fútbol

print("Marcador del partido de fútbol")
print("Por Jose Vicente (ejemplo)")

# Datos del partido (sin pedir por teclado en este ejercicio)
goles_equipo_a = 3
goles_equipo_b = 1

# Cálculo de la diferencia
diferencia = goles_equipo_a - goles_equipo_b

# Salidas
print("Partido terminado")
print("Equipo A:", goles_equipo_a, "goles")
print("Equipo B:", goles_equipo_b, "goles")
print("Diferencia de goles:", diferencia)

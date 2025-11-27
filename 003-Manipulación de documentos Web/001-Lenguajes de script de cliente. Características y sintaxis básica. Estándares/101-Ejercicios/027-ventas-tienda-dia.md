Enunciado

En una tienda de material deportivo se registran las ventas de un día.

Pide por teclado el importe total de ventas de la mañana y el importe total de ventas de la tarde.

Convierte esas entradas a float.

Calcula el total del día sumando ambas cantidades.

Muestra un resumen en pantalla con este formato:

Ventas de la mañana: X
Ventas de la tarde: Y
Ventas totales del día: Z

Solución
# Resumen de ventas de una tienda deportiva

print("Resumen de ventas del día")
print("Por Jose Vicente (ejemplo)")

# Entradas
manana = input("Introduce las ventas de la mañana: ")
tarde = input("Introduce las ventas de la tarde: ")

# Conversión a número
ventas_manana = float(manana)
ventas_tarde = float(tarde)

# Cálculos
ventas_totales = ventas_manana + ventas_tarde

# Salidas
print("Ventas de la mañana:", ventas_manana)
print("Ventas de la tarde:", ventas_tarde)
print("Ventas totales del día:", ventas_totales)


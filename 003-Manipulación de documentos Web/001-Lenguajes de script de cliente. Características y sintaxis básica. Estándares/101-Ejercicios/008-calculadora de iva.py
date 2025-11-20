# En un programa, primero da la bienvenida

print("Calculadora fantástica de IVA")
print("Por Jose Vicente Carratalá")
print("(c) 2025")

# A continuación, toma datos de entrada

base_imponible = input("Introduce la base imponible: ")

# Ahora realiza cálculos con esos datos
base_imponible = float(base_imponible)   # Convierto la base a numero con decimales
iva = base_imponible * 0.21              # Calculo el IVA
total = base_imponible + iva             # Calculo el total

# Por último, ofrece una salida

print("Resultado del cálculo:")
print("Tu base imponible:",base_imponible)
print("IVA 21%:",iva)
print("Total de la factura:",total)


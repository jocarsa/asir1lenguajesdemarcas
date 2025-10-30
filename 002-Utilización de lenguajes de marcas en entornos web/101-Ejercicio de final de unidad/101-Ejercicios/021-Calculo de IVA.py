'''
    Calculadora de Impuestos
    v0.1 por Jose Vicente Carratalá
    Funcionamiento: Introduce una base imponible y se calcula IVA y total
'''

# Este programa no tiene importaciones

# Creo variables
base_imponible = 0
total_iva = 0
total_factura = 0

# Aquí pondría las funciones/clases

# Ahora calculamos

# Primero pido una entrada
print("Programa calculadora de impuestos")
print("(c) 2025 Jose Vicente Carratalá")
print("Introduce una base y te calculo el IVA y el total")
base_imponible = float(input("Introduce la base imponible de la factura: "))

# Luego realizo cálculos
total_iva = base_imponible*0.21
total_factura = base_imponible + total_iva

# Por último expreso una salida
print("El IVA de la factura es: ",total_iva)
print("El total de la factura es: ",total_factura)




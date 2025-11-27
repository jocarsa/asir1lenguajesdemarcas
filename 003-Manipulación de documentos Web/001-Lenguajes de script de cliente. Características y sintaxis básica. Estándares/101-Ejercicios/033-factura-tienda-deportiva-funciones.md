Enunciado

En una tienda de deportes se quiere calcular el total de una factura con IVA.

Crea una función calculaIVA(base) que:

Reciba la base imponible (tipo float).

Calcule el 21% de IVA.

Devuelva el IVA calculado.

Crea otra función calculaTotal(base, iva) que:

Reciba la base y el IVA.

Devuelva la suma de ambos.

En el programa principal:

Pide la base imponible por teclado y conviértela a float.

Llama a las funciones.

Muestra por pantalla: base, IVA y total.

Solución
'''
Programa calculadora de factura para tienda deportiva
Por Jose Vicente (ejemplo)
'''

def calculaIVA(base):
    """
    Calcula el 21% de IVA a partir de una base imponible.
    Devuelve el IVA calculado.
    """
    iva = base * 0.21
    return iva

def calculaTotal(base, iva):
    """
    Calcula el total de la factura sumando base e IVA.
    Devuelve el total.
    """
    total = base + iva
    return total

# Programa principal

print("Calculadora de facturas - Tienda deportiva")

base_texto = input("Introduce la base imponible de la factura: ")
base = float(base_texto)

iva = calculaIVA(base)
total = calculaTotal(base, iva)

print("Base imponible:", base)
print("IVA:", iva)
print("Total factura:", total)

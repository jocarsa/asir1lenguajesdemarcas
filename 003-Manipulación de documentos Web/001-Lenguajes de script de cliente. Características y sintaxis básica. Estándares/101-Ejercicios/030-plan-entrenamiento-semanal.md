Enunciado

Crea un programa que muestre un plan de entrenamiento semanal para un equipo:

De lunes (1) a viernes (5): "Entrenamiento intenso".

Sábado (6): "Partido".

Domingo (7): "Descanso".

Usa un bucle for con range(1,8) para recorrer los días de la semana.

Para cada día, muestra el número de día y el mensaje correspondiente.

Solución
# Plan de entrenamiento semanal

print("Plan de entrenamiento semanal")
print("Por Jose Vicente (ejemplo)")

for dia in range(1,8):
    mensaje = ""

    if dia <= 5:
        mensaje = "Entrenamiento intenso"
    elif dia == 6:
        mensaje = "Partido"
    else:
        mensaje = "Descanso"

    print("Día", dia, "->", mensaje)
    print("---------------")

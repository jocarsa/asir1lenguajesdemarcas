Enunciado

En un videojuego deportivo, al entrar se quiere mostrar un mensaje de bienvenida.

Crea una función llamada mostrarBienvenida que:

No reciba parámetros.

Use print para mostrar dos líneas de mensaje de bienvenida al juego.

Llama a la función varias veces desde el programa principal.

Solución
# Mensaje de bienvenida de un videojuego deportivo

def mostrarBienvenida():
    """
    Muestra un mensaje de bienvenida al juego.
    """
    print("Bienvenido al Juego de Liga Profesional")
    print("Prepara tu equipo y salta al campo")

# Programa principal
print("Arrancando el juego...")
mostrarBienvenida()
print("Cargando menú principal...")
mostrarBienvenida()


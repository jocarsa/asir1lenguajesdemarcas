from flask import Flask,render_template		
from datetime import datetime

ahora = datetime.now()

anio   = ahora.year
mes  = ahora.month
dia    = ahora.day
hora   = ahora.hour
minuto = ahora.minute
segundo = ahora.second

app = Flask(__name__)					

blog = {
  'fecha': {
    'anio': anio,
    'mes': mes,
    'dia': dia,
    'hora': hora,
    'minuto': minuto,
    'segundo': segundo
  },
  'articulos': [
    {
      'titulo': 'Introducción a Flask',
      'texto': (
        'Flask es un microframework de Python diseñado para ofrecer una base ligera y flexible '
        'para el desarrollo de aplicaciones web. A diferencia de otros frameworks más completos, '
        'Flask permite comenzar con una estructura mínima y expandirse progresivamente conforme '
        'las necesidades del proyecto crecen. Su sencillez radica en que no impone una arquitectura '
        'específica, facilitando que cada desarrollador organice su aplicación de la manera más '
        'adecuada. Además, cuenta con una amplia comunidad que mantiene extensiones para gestionar '
        'bases de datos, autenticación, validación de formularios y otras funcionalidades avanzadas. '
        'Por todo ello, Flask se ha convertido en una opción ideal tanto para principiantes como para '
        'expertos que requieren flexibilidad y control total sobre su aplicación web.'
      ),
      'fecha': '2025-12-04'
    },

    {
      'titulo': 'Plantillas con Jinja2',
      'texto': (
        'El motor de plantillas Jinja2 permite separar la lógica de programación del diseño visual, '
        'lo cual es especialmente útil cuando la interfaz de la aplicación requiere cambios frecuentes. '
        'Mediante el uso de directivas como bloques, bucles y condicionales, es posible generar HTML '
        'dinámico de forma clara y organizada. Las plantillas también facilitan la reutilización de '
        'componentes, como encabezados, menús o pies de página, reduciendo la duplicación de código. '
        'Una característica destacable es la posibilidad de aplicar filtros para formatear datos antes '
        'de mostrarlos, así como el escape automático para prevenir vulnerabilidades XSS. Gracias a este '
        'sistema, Jinja2 se integra de forma natural con Flask y mejora significativamente la mantenibilidad.'
      ),
      'fecha': '2025-12-05'
    },

    {
      'titulo': 'Cómo estructurar un proyecto en Python',
      'texto': (
        'Una estructura adecuada es esencial para garantizar que un proyecto en Python pueda ampliarse y '
        'mantenerse sin dificultad. Normalmente se recomienda separar los módulos según su responsabilidad: '
        'ficheros dedicados a la lógica de negocio, configuración, modelos, rutas, utilidades y pruebas. '
        'Además, es aconsejable utilizar entornos virtuales para aislar las dependencias y un archivo '
        '"requirements.txt" que permita reproducir el entorno fácilmente. La documentación, ya sea mediante '
        'docstrings o un sistema más completo como Sphinx, ayuda a otros desarrolladores —o a uno mismo en '
        'el futuro— a comprender mejor el funcionamiento de cada parte del proyecto. Organizar desde el '
        'principio estos elementos ahorra tiempo a largo plazo y reduce la probabilidad de errores.'
      ),
      'fecha': '2025-12-06'
    },

    {
      'titulo': 'Bases de datos con SQLite',
      'texto': (
        'SQLite es una base de datos relacional ligera que opera mediante un único fichero, lo cual la '
        'convierte en una solución ideal para aplicaciones pequeñas o medianas que no requieren un servidor '
        'dedicado. Su velocidad, simplicidad de configuración y compatibilidad con Python la hacen muy '
        'accesible. A través de bibliotecas como "sqlite3", es posible ejecutar consultas SQL directamente '
        'desde Python, crear tablas, insertar datos y realizar operaciones complejas. A pesar de su '
        'sencillez, SQLite soporta transacciones, índices y restricciones, cumpliendo con gran parte del '
        'estándar SQL. No obstante, para aplicaciones que requieren alta concurrencia o escalabilidad, suele '
        'ser conveniente migrar a soluciones como PostgreSQL o MySQL. En cualquier caso, SQLite continúa '
        'siendo una herramienta valiosa en desarrollo, testing y proyectos de escritorio.'
      ),
      'fecha': '2025-12-07'
    },

    {
      'titulo': 'Despliegue de una aplicación Flask',
      'texto': (
        'El despliegue de una aplicación Flask requiere considerar aspectos como el servidor WSGI, la '
        'seguridad, el rendimiento y la accesibilidad pública. Una práctica común consiste en utilizar '
        'Gunicorn como servidor WSGI y Nginx como servidor inverso para manejar peticiones HTTP, archivos '
        'estáticos y balanceo básico de carga. Es importante definir variables de entorno para separar la '
        'configuración de la lógica de la aplicación, así como asegurarse de que los paquetes del sistema y '
        'del entorno virtual estén actualizados. También se recomienda habilitar HTTPS mediante certificados '
        'SSL para garantizar la privacidad y autenticidad de las comunicaciones. Un buen despliegue no solo '
        'consiste en subir la aplicación al servidor, sino en crear un sistema estable que soporte tráfico '
        'real sin comprometer la seguridad ni la experiencia del usuario.'
      ),
      'fecha': '2025-12-08'
    },

    {
      'titulo': 'Buenas prácticas de programación',
      'texto': (
        'Aplicar buenas prácticas de programación es fundamental para desarrollar software robusto, legible '
        'y fácil de mantener. Entre las más recomendables destacan el uso de nombres descriptivos para '
        'variables y funciones, la división del código en módulos independientes y la adopción de patrones '
        'de diseño cuando resulta apropiado. La escritura de pruebas unitarias permite detectar errores de '
        'forma temprana y facilita futuras refactorizaciones. Mantener un estilo uniforme, por ejemplo '
        'siguiendo la guía PEP8 en Python, contribuye a la claridad del código. Por último, documentar '
        'adecuadamente cada componente es clave para que otros desarrolladores puedan comprender y ampliar '
        'el software sin dificultades. Estas prácticas, aplicadas de manera constante, mejoran notablemente '
        'la calidad global del proyecto.'
      ),
      'fecha': '2025-12-09'
    }
  ]
}


@app.get("/")										
def inicio():										
    return render_template("blog.html",datos=blog)

if __name__ == "__main__":				
    app.run(debug=True)	
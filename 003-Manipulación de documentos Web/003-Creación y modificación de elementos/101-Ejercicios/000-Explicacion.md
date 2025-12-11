Mediante Flask y Jinja queremos hacer webs dinámicas
Una web dinámica es una web que cambia con los datos

///////////////// ENVIO DE DATOS

Desde Python, pasamos datos de esta forma:
return render_template("blog.html",datos=blog)
Los datos son un parámetro que se pone después de la plantilla html

///////////////// RECOGIDA DE DATOS

En HTML

Tengo soporte para coger variables
La sintaxis es {{ datos['loquequierascoger'] }}

También tengo soporte para estructuras de recorrer
La sintaxis es:

{% for elemento in conjunto %}
	... y aquí dentro puedes poner lo que quieras que se repita
{% endfor %}






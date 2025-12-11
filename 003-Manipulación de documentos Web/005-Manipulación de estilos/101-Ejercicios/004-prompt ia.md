tengo una base de datos sqlite con una tabla con esta estructura CREATE TABLE "entradas" ( "id" INTEGER, "titulo" TEXT, "fecha" TEXT, "autor" TEXT, "categoria" TEXT, "contenido" TEXT, "imagen" TEXT, PRIMARY KEY("id" AUTOINCREMENT) ); y este es un insert into de muestra: INSERT INTO entradas VALUES ( NULL, 'Este es el título 2', '2025-12-11', 'Jose Vicente Carratala', 'general', 'Este es el contenido del artículo 2', 'josevicente.jpg' ); con lo cual por favor creame 30 entradas más que traten sobre mis actividades

INSERT INTO entradas VALUES
(NULL,'Desarrollo del motor de simulación fractal', '2025-01-10','Jose Vicente Carratala','programacion','Hoy he avanzado en mi simulación de terreno infinito utilizando C++ y OpenCV, incorporando capas de ruido fractal y optimizaciones con OpenMP.','fractal.jpg'),

(NULL,'Publicación de contenido formativo para DAM y DAW','2025-01-18','Jose Vicente Carratala','formacion','He ampliado los apuntes y actividades de FP, incluyendo ejercicios de bases de datos, programación y proyectos intermodulares.','formacion.jpg'),

(NULL,'Entrenamiento del modelo conversacional educativo', '2025-02-05','Jose Vicente Carratala','ia','He continuado con el entrenamiento del modelo Nous-Hermes-2-Mistral-7B mediante QLoRA, generando datasets personalizados en ChatML.','entrenamiento.jpg'),

(NULL,'Mejora del dashboard de gestión de alumnos','2025-02-12','Jose Vicente Carratala','programacion','Hoy he actualizado el módulo alumnos2, integrando búsqueda avanzada y tarjetas informativas más claras.','dashboard.jpg'),

(NULL,'Integración del sistema de matrícula automática con Moodle','2025-02-20','Jose Vicente Carratala','programacion','He creado un sistema que comprueba automáticamente la existencia de usuarios en Moodle y su matriculación en cursos correspondientes.','moodle.jpg'),

(NULL,'Progreso en el libro de SQL basado en ejercicios','2025-03-01','Jose Vicente Carratala','libros','He continuado la redacción del libro de SQL, ampliando los ejemplos de DDL, DML y subconsultas.','sqlbook.jpg'),

(NULL,'Desarrollo del juego Rebote en JavaScript','2025-03-10','Jose Vicente Carratala','programacion','He creado una versión didáctica del juego Pong con emojis y mecánicas progresivas orientado a estudiantes.','rebote.jpg'),

(NULL,'Automatización del blog mediante IA','2025-03-14','Jose Vicente Carratala','ia','He integrado scripts que generan artículos desde transcripciones de YouTube usando modelos locales y los publican automáticamente en el blog.','blogia.jpg'),

(NULL,'Simulación de campo estelar tipo queso gruyere','2025-03-22','Jose Vicente Carratala','programacion','He trabajado en una simulación de estrellas con ruido fractal 3D creando túneles y desplazamiento infinito.','estrellas.jpg'),

(NULL,'Nuevo sistema de backups automáticos de Moodle','2025-04-01','Jose Vicente Carratala','devops','He creado un script en Python que realiza backups MBZ, los transfiere por SSH y elimina archivos temporales.','backup.jpg'),

(NULL,'Mejora del motor de renderizado con CUDA','2025-04-09','Jose Vicente Carratala','programacion','He avanzado en mi proyecto de ray tracing interactivo en C++ y CUDA, optimizando la interfaz gráfica.','cuda.jpg'),

(NULL,'Diseño de la plataforma BI para Jocarsa','2025-04-15','Jose Vicente Carratala','jocarsa','He definido la arquitectura inicial de la plataforma de Business Intelligence con dashboards y análisis en tiempo real.','bi.jpg'),

(NULL,'Desarrollo del libro sobre Ubuntu Server','2025-04-20','Jose Vicente Carratala','libros','Hoy he redactado varios capítulos sobre la instalación, gestión de servicios y configuración avanzada en Ubuntu Server.','ubuntu.jpg'),

(NULL,'Integración del modelo 3D con sincronización de voces','2025-04-28','Jose Vicente Carratala','ia','He unido el asistente conversacional con un avatar 3D en A-Frame, sincronizando lipsync con morph targets.','avatar.jpg'),

(NULL,'Simulación 2D del campo de fútbol interactivo','2025-05-02','Jose Vicente Carratala','programacion','He añadido IA rival que persigue el balón y dispara a portería en mi motor 2D HTML Canvas.','futbol.jpg'),

(NULL,'Revisión y mejora del sistema de blog con SQLite','2025-05-10','Jose Vicente Carratala','programacion','He optimizado el sistema de carga de artículos, mejorado el parseo y añadido nuevas categorías.','sqlite.jpg'),

(NULL,'Expansión del universo narrativo Fragmentarios','2025-05-18','Jose Vicente Carratala','creativo','He ampliado el trasfondo de Naara y Roan, integrando temas de protección, valentía y observación crítica.','fragmentarios.jpg'),

(NULL,'Generación de nubes de puntos desde cortes ortográficos','2025-05-26','Jose Vicente Carratala','programacion','He desarrollado un script para combinar 1000 imágenes en una nube XYZ+RGB procesando profundidades.','nube.jpg'),

(NULL,'Mejora del script de procesamiento de vídeos YouTube','2025-06-01','Jose Vicente Carratala','ia','He creado una versión simplificada que corta fragmentos al 0%, 33%, 66% y final, convirtiéndolos en Shorts.','shorts.jpg'),

(NULL,'Desarrollo del módulo darksalmon para gestión de empleados','2025-06-10','Jose Vicente Carratala','jocarsa','He avanzado en la gestión de asistencia, incidencias y vacaciones con administración por panel web.','darksalmon.jpg'),

(NULL,'Proyecto de asistente conversacional para programación','2025-06-18','Jose Vicente Carratala','ia','Hoy he integrado modelos locales con un sistema SVG interactivo y lectura en voz alta.','asistente.jpg'),

(NULL,'Creación de material didáctico para el módulo de DAW','2025-06-25','Jose Vicente Carratala','formacion','He escrito descripciones de módulos del segundo curso de DAW basadas en las ya generadas para DAM.','daw.jpg'),

(NULL,'Nueva herramienta interna para mapas mentales','2025-07-03','Jose Vicente Carratala','jocarsa','He creado un sistema visual para generar mapas mentales como parte del paquete de herramientas de productividad.','mapas.jpg'),

(NULL,'Mejora de la web de cursos comoprogramar.es','2025-07-12','Jose Vicente Carratala','web','He adaptado la estructura JSON y actualizado las descripciones de los cursos para la nueva plataforma.','comoprogramar.jpg'),

(NULL,'Progreso en el libro sobre Markdown','2025-07-20','Jose Vicente Carratala','libros','He añadido ejercicios continuos, incluyendo un gestor de posts en XML para enseñar vocabularios y esquemas.','markdown.jpg'),

(NULL,'Creación de miniaplicación React para paletas de colores','2025-07-29','Jose Vicente Carratala','programacion','He completado un selector avanzado que genera paletas complementarias, similares y triádicas.','react.jpg'),

(NULL,'Expansión del catálogo de productos Jocarsa','2025-08-05','Jose Vicente Carratala','jocarsa','He preparado textos comerciales orientados al cliente destacando beneficios de cada solución SaaS.','catalogo.jpg'),

(NULL,'Actualización del sistema de búsqueda de archivos en Flask','2025-08-14','Jose Vicente Carratala','programacion','Hoy he implementado filtros avanzados, tamaño de archivo y mejoras visuales en CSS.','flask.jpg'),

(NULL,'Nuevo script de scraping con tiempos de espera','2025-09-01','Jose Vicente Carratala','programacion','He añadido almacenamiento progresivo y pausas entre solicitudes para evitar bloqueos y mejorar la estabilidad.','scraping.jpg'),

(NULL,'Despliegue optimizado de BigBlueButton 3.0','2025-10-05','Jose Vicente Carratala','devops','He configurado BigBlueButton con Greenlight y firewall, dejando pendiente la instalación de certificados SSL.','bbb.jpg');

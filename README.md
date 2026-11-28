# Bocado de Culto

Aplicación web desarrollada con Django para explorar la relación entre platos populares del cine, sus países de procedencia y las películas en las que aparecen.

## Requisitos

- Python 3.12 o superior.
- Django 6.1.2.

## Puesta en marcha

Desde la carpeta que contiene `manage.py`:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_demo
python manage.py preparar_roles
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`. El panel de administración está disponible en `http://127.0.0.1:8000/admin/`.

El comando python manage.py cargar_demo carga el catálogo desde core/fixtures/bocado_demo.json cuando la base está vacía. Incluye 14 países, 63 platos, 41 películas, 75 relaciones entre películas y platos, una sugerencia de película y una sugerencia de plato. Si se vuelve a ejecutar, conserva los datos existentes. El comando python manage.py preparar_roles prepara los grupos Consulta y Edición.

## Secciones

- **Inicio** (`/`): muestra en el mapa un plato destacado de cada país con platos registrados. Se priorizan los platos asociados a más películas.
- **Platos** (`/platos/`, `/platos/<id>/`): catálogo y ficha de cada plato, con su país de origen y las películas relacionadas.
- **Países** (`/paises/`, `/paises/<id>/`): catálogo dinámico de países y ficha de cada país, con sus platos y las películas enlazadas desde esos platos.
- **Películas** (`/peliculas/`, `/peliculas/<id>/`): catálogo y ficha de cada película, con director, sinopsis, país y platos asociados.
- **Administración** (`/admin/`): gestión de países, platos y películas mediante el panel nativo de Django.

## Datos incluidos

La base de datos proporcionada contiene 14 países, 63 platos y 41 películas. Las imágenes del catálogo se encuentran en `static/images/`. Los países que todavía no tengan un sello ilustrado propio utilizan el sello genérico.

## Pruebas

Ejecuta la batería de pruebas con:

```bash
python manage.py test core
```

Los estilos compartidos se definen en `static/css/base.css`; cada sección amplía esos estilos desde su propia hoja CSS. Las plantillas heredan de `core/templates/base.html` y utilizan las variables de contexto de `core/views.py` y las rutas nombradas de `core/urls.py`.

## Buscador e idiomas

Las tres listas del catálogo comparten un buscador AJAX por nombre (platos y países) o por título (películas). Buscar y Limpiar actualizan únicamente la zona `#resultados`, sin recargar la página. Sin JavaScript, el formulario GET y el enlace Limpiar funcionan igualmente.

| Sección | Castellano | Inglés | Búsqueda de ejemplo |
| --- | --- | --- | --- |
| Platos | `/platos/` | `/en/platos/` | `ramen`: Ramen con jamón y huevo y Ramen de Cerdo |
| Películas | `/peliculas/` | `/en/peliculas/` | `ratatouille`: Ratatouille |
| Países | `/paises/` | `/en/paises/` | `italia`: Italia |

- También se pueden abrir directamente las rutas con `?q=ramen`, `?q=ratatouille` o `?q=italia`, respectivamente.
- Busca `zzzzz` en cada sección para comprobar el aviso de búsqueda sin resultados. Limpiar recupera los 63 platos, 41 películas o 14 países del catálogo de demostración. El contador de sellos se actualiza con el número de países encontrados.
- El selector Castellano/English conserva la lista o ficha actual y los parámetros de búsqueda, incluso después de una petición AJAX.
- La navegación, portada, encabezados, textos de interfaz de las listas y fichas, mensajes de resultados y formulario de sugerencias disponen de traducciones al inglés. Los nombres de países y platos, títulos de películas, descripciones y sinopsis del catálogo de demostración se muestran también en inglés mediante `core/catalogo_en.json`. La base de datos, los nombres usados en rutas de imágenes, las ilustraciones y la cita decorativa en castellano se conservan. Las búsquedas aceptan los nombres originales y los ingleses en ambos idiomas (por ejemplo, `España`/`Spain`, `El Padrino`/`The Godfather`). Para nuevos datos, añade sus textos originales y traducciones al JSON; si no existe una traducción, se muestra el original. Los botones de búsqueda e idioma comparten los colores y texturas del diseño original.
- Las tres listas utilizan el mismo script `static/js/buscador-platos.js` y sus fragmentos `_tarjetas.html` para las respuestas parciales.

Para regenerar y compilar el catálogo de traducciones con GNU gettext instalado:

```bash
python manage.py makemessages -l en -i "env1/*" -i ".venv/*"
python manage.py compilemessages -l en -i "env1/*" -i ".venv/*"
python manage.py check
python manage.py test core
```

Los archivos `locale/en/LC_MESSAGES/django.po` y `django.mo` se incluyen en el proyecto; no hace falta recompilar para usar las traducciones existentes. Las pruebas de buscadores e idiomas se encuentran en `core/test_buscadores.py`.

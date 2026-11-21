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
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`. El panel de administración está disponible en `http://127.0.0.1:8000/admin/`.

La base de datos SQLite incluida (`db.sqlite3`) contiene el catálogo de demostración. Si se crea una base de datos vacía, `migrate` prepara el esquema, pero no introduce automáticamente los datos de demostración.

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

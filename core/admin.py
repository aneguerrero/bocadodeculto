from django.contrib import admin
from .models import Pais, Pelicula, Plato, Sugerencia

admin.site.site_header = "Bocado de Culto"
admin.site.site_title = "Bocado de Culto"
admin.site.index_title = "Catálogo y sugerencias"


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "pais_origen")
    list_filter = ("pais_origen",)
    search_fields = ("nombre",)


@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "director", "pais")
    search_fields = ("titulo", "director")
    list_filter = ("pais",)
    filter_horizontal = ("platos_maridados",)


@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ("titulo_pelicula", "plato")
    list_filter = ("plato__pais_origen",)
    search_fields = ("titulo_pelicula", "plato__nombre")
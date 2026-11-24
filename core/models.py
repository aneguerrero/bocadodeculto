
from django.db import models


class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    pais_origen = models.ForeignKey(
        Pais, on_delete=models.CASCADE, related_name='platos'
    )

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=150)
    sinopsis = models.TextField()
    director = models.CharField(max_length=100)
    pais = models.ForeignKey(
        Pais, on_delete=models.CASCADE, related_name='peliculas'
    )
    platos_maridados = models.ManyToManyField(
        Plato, related_name='peliculas'
    )

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"

    def __str__(self):
        return self.titulo


class Sugerencia(models.Model):
    """Propuesta de una película nueva, sin modificar el catálogo público."""

    plato = models.ForeignKey(
        Plato, on_delete=models.CASCADE, related_name="sugerencias"
    )
    titulo_pelicula = models.CharField(max_length=150)
    comentario = models.TextField(blank=True)

    class Meta:
        verbose_name = "Sugerencia de película"
        verbose_name_plural = "Sugerencias de películas"

    def __str__(self):
        return f"{self.titulo_pelicula} ({self.plato})"


class SugerenciaPlato(models.Model):
    """Propuesta de un plato nuevo, sin modificar el catálogo público."""

    pelicula = models.ForeignKey(
        Pelicula, on_delete=models.CASCADE,
        related_name="sugerencias_platos"
    )
    nombre_plato = models.CharField(max_length=100)
    comentario = models.TextField(blank=True)

    class Meta:
        verbose_name = "Sugerencia de plato"
        verbose_name_plural = "Sugerencias de platos"

    def __str__(self):
        return f"{self.nombre_plato} ({self.pelicula})"

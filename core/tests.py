from django.test import TestCase
from django.urls import reverse

from .models import Pais, Pelicula, Plato


class CatalogPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pais_a = Pais.objects.create(nombre="Italia")
        cls.pais_b = Pais.objects.create(nombre="Japón")

        cls.plato_a = Plato.objects.create(
            nombre="Pasta de prueba",
            descripcion="Una pasta para comprobar las fichas del catálogo.",
            pais_origen=cls.pais_a,
        )
        cls.plato_b = Plato.objects.create(
            nombre="Pizza de prueba",
            descripcion="Una pizza para comprobar la selección de portada.",
            pais_origen=cls.pais_a,
        )
        cls.plato_c = Plato.objects.create(
            nombre="Ramen de prueba",
            descripcion="Un ramen para el segundo país.",
            pais_origen=cls.pais_b,
        )

        cls.pelicula_a = Pelicula.objects.create(
            titulo="Película uno",
            sinopsis="Sinopsis de prueba uno.",
            director="Directora uno",
            pais=cls.pais_a,
        )
        cls.pelicula_b = Pelicula.objects.create(
            titulo="Película dos",
            sinopsis="Sinopsis de prueba dos.",
            director="Director dos",
            pais=cls.pais_b,
        )
        cls.pelicula_a.platos_maridados.add(cls.plato_a, cls.plato_b)
        cls.pelicula_b.platos_maridados.add(cls.plato_a, cls.plato_c)

    def test_all_public_list_and_detail_routes_render(self):
        paths = [
            reverse("portada"),
            reverse("lista_platos"),
            reverse("detalle_plato", args=[self.plato_a.pk]),
            reverse("lista_paises"),
            reverse("detalle_pais", args=[self.pais_a.pk]),
            reverse("lista_peliculas"),
            reverse("detalle_pelicula", args=[self.pelicula_a.pk]),
        ]
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Bocado de Culto")

    def test_home_selects_one_dish_per_country_and_prioritizes_film_count(self):
        response = self.client.get(reverse("portada"))
        self.assertEqual(response.status_code, 200)

        selected = response.context["platos_destacados"]
        self.assertEqual(len(selected), 2)
        selected_names = {plato.nombre for plato in selected}
        self.assertEqual(selected_names, {"Pasta de prueba", "Ramen de prueba"})

    def test_country_list_uses_database_and_extends_base_template(self):
        pais_nuevo = Pais.objects.create(nombre="Perú")

        response = self.client.get(reverse("lista_paises"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Perú")
        self.assertContains(
            response,
            f'href="{reverse("detalle_pais", args=[pais_nuevo.pk])}"',
        )
        self.assertContains(response, "3 SELLOS")
        self.assertContains(response, "/static/css/base.css")
        self.assertContains(response, "/static/css/paises.css")
        self.assertContains(response, 'class="footer-contenido"')
        self.assertContains(response, "/static/images/sello.png")

    def test_related_links_connect_dishes_countries_and_films(self):
        dish_list_response = self.client.get(reverse("lista_platos"))
        movie_list_response = self.client.get(reverse("lista_peliculas"))
        dish_response = self.client.get(
            reverse("detalle_plato", args=[self.plato_a.pk])
        )
        country_response = self.client.get(
            reverse("detalle_pais", args=[self.pais_a.pk])
        )
        movie_response = self.client.get(
            reverse("detalle_pelicula", args=[self.pelicula_a.pk])
        )

        country_url = reverse("detalle_pais", args=[self.pais_a.pk])
        movie_url = reverse("detalle_pelicula", args=[self.pelicula_a.pk])
        dish_url = reverse("detalle_plato", args=[self.plato_a.pk])

        self.assertContains(dish_list_response, dish_url)
        self.assertContains(dish_list_response, country_url)
        self.assertContains(movie_list_response, movie_url)
        self.assertContains(dish_response, country_url)
        self.assertContains(dish_response, movie_url)
        self.assertContains(country_response, dish_url)
        self.assertContains(country_response, movie_url)
        self.assertContains(movie_response, country_url)
        self.assertContains(movie_response, dish_url)

    def test_stylesheets_are_linked_from_the_shared_template(self):
        response = self.client.get(reverse("lista_platos"))
        self.assertContains(response, "/static/css/base.css")
        self.assertContains(response, "/static/css/platos.css")

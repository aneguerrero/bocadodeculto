from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from .models import Pais, Pelicula, Plato


class BuscadoresIdiomasTests(TestCase):
    def setUp(self):
        self.addCleanup(translation.activate, translation.get_language())
        translation.activate("es")

    @classmethod
    def setUpTestData(cls):
        cls.japon = Pais.objects.create(nombre="Japón")
        cls.italia = Pais.objects.create(nombre="Italia")
        cls.ramen = Plato.objects.create(nombre="Ramen de prueba", pais_origen=cls.japon)
        Plato.objects.create(nombre="Pasta de prueba", pais_origen=cls.italia)
        cls.film = Pelicula.objects.create(titulo="Chef de prueba", pais=cls.japon)
        Pelicula.objects.create(titulo="Otra película", pais=cls.italia)

    def test_busquedas_completas_y_ajax_en_ambos_idiomas(self):
        casos = (
            ("platos", "RAMEN", "Ramen de prueba", "Pasta de prueba", "plato-caja"),
            ("peliculas", "CHEF", "Chef de prueba", "Otra película", "pelicula-caja"),
            ("paises", "JAP", "Japón", "Italia", "sello-pais"),
        )
        for prefijo in ("", "/en"):
            for seccion, q, incluido, excluido, clase in casos:
                ruta = f"{prefijo}/{seccion}/"
                with self.subTest(ruta=ruta):
                    esperado = "Japan" if prefijo and seccion == "paises" else incluido
                    completa = self.client.get(ruta, {"q": " " + q + " "})
                    parcial = self.client.get(ruta, {"q": q}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
                    self.assertContains(completa, 'id="buscar"')
                    self.assertContains(completa, esperado)
                    self.assertContains(parcial, esperado)
                    self.assertNotContains(parcial, excluido)
                    self.assertNotContains(parcial, '<html')
                    self.assertNotContains(parcial, 'id="buscar"')
                    self.assertContains(parcial, f'class="{clase}"', count=1)
                    self.assertIn("X-Requested-With", parcial.headers["Vary"])
                    self.assertIn("X-Requested-With", completa.headers["Vary"])
                    self.assertContains(completa, f'value="{q}"')
                    limpia = self.client.get(ruta, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
                    self.assertContains(limpia, f'class="{clase}"', count=2)

    def test_sin_resultados_traducidos(self):
        for seccion, es, en in (
            ("platos", "No hay platos para esta búsqueda.", "No dishes match your search."),
            ("peliculas", "No hay películas para esta búsqueda.", "No films match your search."),
            ("paises", "No hay países para esta búsqueda.", "No countries match your search."),
        ):
            for prefijo, texto in (("", es), ("/en", en)):
                with self.subTest(seccion=seccion, idioma=prefijo):
                    respuesta = self.client.get(f"{prefijo}/{seccion}/", {"q": "zzzzz"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
                    self.assertContains(respuesta, texto)

    def test_contador_de_paises_filtrado(self):
        for prefijo, singular, plural in (("", "1 SELLO", "2 SELLOS"), ("/en", "1 STAMP", "2 STAMPS")):
            ruta = f"{prefijo}/paises/"
            self.assertContains(self.client.get(ruta, {"q": "Jap"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest"), singular)
            self.assertContains(self.client.get(ruta), plural)

    def test_selector_conserva_filtros_y_fichas(self):
        for ruta, q in (("/platos/", "ramen"), ("/peliculas/", "Chef"), ("/paises/", "Jap")):
            url = ruta + "?q=" + q
            inglesa = "/en" + url
            self.assertContains(self.client.get(url), f'value="{inglesa}"')
            respuesta = self.client.post("/i18n/setlang/", {"language": "en", "next": inglesa})
            self.assertRedirects(respuesta, inglesa)
            self.assertContains(self.client.get(inglesa), f'value="{url}"')
            respuesta = self.client.post("/i18n/setlang/", {"language": "es", "next": url})
            self.assertRedirects(respuesta, url)
        for nombre, pk in (("detalle_plato", self.ramen.pk), ("detalle_pais", self.japon.pk), ("detalle_pelicula", self.film.pk), ("sugerir_pelicula", self.ramen.pk)):
            with translation.override("es"):
                ruta = reverse(nombre, args=[pk])
            self.assertContains(self.client.get(ruta), f'value="/en{ruta}"')
            self.assertContains(self.client.get("/en" + ruta), f'value="{ruta}"')

    def test_interfaz_inglesa_en_listas_fichas_y_portada(self):
        for ruta, texto in (
            ("/en/", "Our starring dishes"),
            ("/en/platos/", "Find a dish"),
            ("/en/paises/", "Find a country"),
            ("/en/peliculas/", "Find a film"),
            (f"/en/platos/{self.ramen.pk}/", "About the dish"),
            (f"/en/paises/{self.japon.pk}/", "Flavours of the destination"),
            (f"/en/peliculas/{self.film.pk}/", "Synopsis"),
            (f"/en/platos/{self.ramen.pk}/sugerir/", "Send suggestion"),
        ):
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertContains(respuesta, texto)
                self.assertContains(respuesta, '<html lang="en">')
                self.assertContains(respuesta, "Home")


    def test_datos_del_catalogo_en_ambos_idiomas(self):
        pais = Pais.objects.create(nombre="España")
        plato = Plato.objects.create(
            nombre="Tortilla española", pais_origen=pais,
            descripcion="Tortilla jugosa de patata y huevo, preparada en bares y cocinas familiares españolas.",
        )
        film = Pelicula.objects.create(
            titulo="El Padrino", pais=pais,
            sinopsis="El envejecido patriarca de una dinastía del crimen organizado traslada el control de su imperio clandestino a su hijo reacio.",
        )
        film.platos_maridados.add(plato)
        for prefijo, nombre_pais, nombre_plato, titulo in (
            ("", "España", "Tortilla española", "El Padrino"),
            ("/en", "Spain", "Spanish Omelette", "The Godfather"),
        ):
            for seccion, terminos, texto in (
                ("paises", ("España", "Spain", "espana"), nombre_pais),
                ("platos", ("Tortilla española", "Spanish Omelette"), nombre_plato),
                ("peliculas", ("El Padrino", "The Godfather"), titulo),
            ):
                for termino in terminos:
                    respuesta = self.client.get(f"{prefijo}/{seccion}/", {"q": termino}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
                    self.assertContains(respuesta, texto)
        inglesa = self.client.get(f"/en/platos/{plato.pk}/")
        self.assertContains(inglesa, "Spanish Omelette")
        self.assertContains(inglesa, "A tender potato and egg omelette")
        self.assertContains(inglesa, "tortilla-espanola.jpg")
        self.assertContains(inglesa, "The Godfather")
        self.assertContains(self.client.get(f"/en/peliculas/{film.pk}/"), "The ageing patriarch")
        self.assertContains(self.client.get(f"/en/paises/{pais.pk}/"), "A tender potato and egg omelette")
        self.assertContains(self.client.get(f"/en/platos/{plato.pk}/sugerir/"), "Spanish Omelette")
        plato.refresh_from_db()
        self.assertEqual(plato.nombre, "Tortilla española")
        self.assertEqual(film.titulo, "El Padrino")

    def test_textos_nuevos_sin_traduccion_conservan_original(self):
        self.assertContains(self.client.get(f"/en/platos/{self.ramen.pk}/"), "Ramen de prueba")

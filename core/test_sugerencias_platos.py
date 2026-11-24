from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import Client, TestCase
from .models import Pais, Pelicula, Plato, Sugerencia, SugerenciaPlato


class SugerenciasPlatosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pais = Pais.objects.create(nombre="España")
        cls.plato = Plato.objects.create(nombre="Tortilla española", pais_origen=pais)
        cls.otro = Plato.objects.create(nombre="Paella valenciana", pais_origen=pais)
        cls.pelicula = Pelicula.objects.create(titulo="El Padrino", pais=pais)
        cls.pelicula.platos_maridados.add(cls.otro)

    def test_formulario_original_conserva_validacion_y_guardado(self):
        ruta = f"/platos/{self.plato.pk}/sugerir/"
        invalida = self.client.post(ruta, {"titulo_pelicula": ""})
        self.assertTrue(invalida.context["form"].errors)
        self.assertEqual(Sugerencia.objects.count(), 0)
        self.assertRedirects(self.client.post(ruta, {"titulo_pelicula": "Otra película"}), f"/platos/{self.plato.pk}/")
        self.assertEqual(Sugerencia.objects.get().titulo_pelicula, "Otra película")
        self.assertEqual(SugerenciaPlato.objects.count(), 0)

    def test_nuevo_formulario_en_ambos_idiomas(self):
        for prefijo, boton, nombre in (("", "Sugerir un plato", "Nombre del plato"), ("/en", "Suggest a dish", "Dish name")):
            ruta = f"{prefijo}/peliculas/{self.pelicula.pk}/"
            self.assertContains(self.client.get(ruta), f'href="{ruta}sugerir/"')
            respuesta = self.client.get(ruta + "sugerir/")
            self.assertContains(respuesta, boton)
            self.assertContains(respuesta, nombre)
            self.assertContains(respuesta, 'name="nombre_plato"')
            self.assertNotContains(respuesta, '<select')
            self.assertContains(respuesta, 'name="csrfmiddlewaretoken"')
            self.assertContains(respuesta, f'value="{"/en" if not prefijo else ""}/peliculas/{self.pelicula.pk}/sugerir/"')

    def test_nueva_sugerencia_no_modifica_catalogo(self):
        ruta = f"/en/peliculas/{self.pelicula.pk}/sugerir/"
        datos = {"nombre_plato": "  Cannoli caseros  ", "comentario": "Test", "pelicula": 99999}
        respuesta = self.client.post(ruta, datos, follow=True)
        self.assertContains(respuesta, "Suggestion saved.")
        propuesta = SugerenciaPlato.objects.get()
        self.assertEqual(propuesta.nombre_plato, "Cannoli caseros")
        self.assertEqual(propuesta.pelicula, self.pelicula)
        self.assertEqual(propuesta.comentario, "Test")
        self.assertEqual(list(self.pelicula.platos_maridados.all()), [self.otro])
        self.assertEqual(Plato.objects.count(), 2)
        self.assertEqual(Sugerencia.objects.count(), 0)
        self.client.get(f"/en/peliculas/{self.pelicula.pk}/")
        self.assertEqual(SugerenciaPlato.objects.count(), 1)

    def test_rechaza_nombres_invalidos_y_csrf(self):
        ruta = f"/peliculas/{self.pelicula.pk}/sugerir/"
        for valor in ("", "   ", "a" * 101):
            respuesta = self.client.post(ruta, {"nombre_plato": valor})
            self.assertTrue(respuesta.context["form"].errors)
        self.assertEqual(SugerenciaPlato.objects.count(), 0)
        self.assertEqual(Client(enforce_csrf_checks=True).post(ruta, {"nombre_plato": "Cannoli"}).status_code, 403)
        self.assertEqual(self.client.get("/peliculas/99999/sugerir/").status_code, 404)
        self.assertRedirects(self.client.post(ruta, {"nombre_plato": "Cannoli"}), f"/peliculas/{self.pelicula.pk}/")
        self.assertEqual(SugerenciaPlato.objects.get().comentario, "")

    def test_roles_conservan_sugerencias_originales_y_nuevas(self):
        call_command("preparar_roles", verbosity=0)
        for grupo, acciones in (("Consulta", {"view"}), ("Edición", {"view", "add", "change"})):
            codigos = set(Group.objects.get(name=grupo).permissions.values_list("codename", flat=True))
            self.assertEqual(codigos, {f"{a}_{m}" for a in acciones for m in ("pais", "plato", "pelicula", "sugerencia", "sugerenciaplato")})

    def test_carteles_sin_rotulos_y_detalle_traducido(self):
        for prefijo, titulo in (("", "El Padrino"), ("/en", "The Godfather")):
            for cabecera in ({}, {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}):
                respuesta = self.client.get(f"{prefijo}/peliculas/", {"q": "The Godfather"}, **cabecera)
                self.assertContains(respuesta, 'class="pelicula-caja"', count=1)
                self.assertContains(respuesta, 'el-padrino.jpg')
                self.assertContains(respuesta, f'alt="{titulo}"')
                self.assertNotContains(respuesta, 'class="pelicula-titulo-idioma"')
            self.assertContains(self.client.get(f"{prefijo}/peliculas/{self.pelicula.pk}/"), f"<h1>{titulo}</h1>", html=True)

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Pais, Plato, Pelicula, Sugerencia, SugerenciaPlato


class Command(BaseCommand):
    help = "Carga los datos de demostración en un catálogo vacío."

    @transaction.atomic
    def handle(self, *args, **options):
        modelos = (Pais, Plato, Pelicula, Sugerencia, SugerenciaPlato)

        if any(modelo.objects.exists() for modelo in modelos):
            self.stdout.write("El catálogo ya tiene datos. Se conserva.")
            return

        call_command("loaddata", "bocado_demo", verbosity=1)
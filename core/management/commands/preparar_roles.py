from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Prepara los grupos de la aplicación core."

    @transaction.atomic
    def handle(self, *args, **options):
        modelos = ("pais", "plato", "pelicula", "sugerencia")
        roles = {"Consulta": ("view",), "Edición": ("view", "add", "change")}
        for nombre, acciones in roles.items():
            grupo, _ = Group.objects.get_or_create(name=nombre)
            codigos = [f"{a}_{m}" for a in acciones for m in modelos]
            permisos = Permission.objects.filter(
                content_type__app_label="core", codename__in=codigos
            )
            grupo.permissions.set(permisos)
        self.stdout.write("Grupos Consulta y Edición preparados.")
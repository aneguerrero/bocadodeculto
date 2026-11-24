"""Traducciones del catálogo de demostración, sin modificar la base de datos."""
import json
import unicodedata
from pathlib import Path

from django.db.models import Q
from django.utils.translation import get_language

with Path(__file__).with_name("catalogo_en.json").open(encoding="utf-8") as archivo:
    CATALOGO_EN = json.load(archivo)


def traducir_catalogo(texto):
    if (get_language() or "es").startswith("en"):
        return CATALOGO_EN.get(texto, texto)
    return texto


def normalizar(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto.casefold())
                   if not unicodedata.combining(c))


def filtrar_catalogo(queryset, campo, q):
    """Acepta el nombre original o el inglés, independientemente del idioma activo."""
    if not q:
        return queryset
    termino = normalizar(q)
    equivalencias = [original for original, ingles in CATALOGO_EN.items()
                     if termino in normalizar(original) or termino in normalizar(ingles)]
    return queryset.filter(Q(**{f"{campo}__icontains": q}) | Q(**{f"{campo}__in": equivalencias}))

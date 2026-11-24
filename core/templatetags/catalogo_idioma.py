from django import template
from core.catalogo_i18n import traducir_catalogo

register = template.Library()
register.filter("catalogo", traducir_catalogo)

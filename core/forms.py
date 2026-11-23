from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Sugerencia


class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ["titulo_pelicula", "comentario"]
        labels = {
            "titulo_pelicula": _("Título de la película"),
            "comentario": _("Comentario opcional"),
        }
        widgets = {"comentario": forms.Textarea(attrs={"rows": 3})}
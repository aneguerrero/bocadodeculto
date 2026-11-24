"""Propuestas libres de platos desde una película del catálogo."""
from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.http import require_http_methods

from .models import Pelicula, SugerenciaPlato


class SugerenciaPlatoForm(forms.ModelForm):
    class Meta:
        model = SugerenciaPlato
        fields = ["nombre_plato", "comentario"]
        labels = {
            "nombre_plato": gettext_lazy("Nombre del plato"),
            "comentario": gettext_lazy("Comentario opcional"),
        }
        widgets = {
            "nombre_plato": forms.TextInput(),
            "comentario": forms.Textarea(attrs={"rows": 3}),
        }


@require_http_methods(["GET", "POST"])
def sugerir_plato(request, id):
    pelicula = get_object_or_404(Pelicula, pk=id)
    form = SugerenciaPlatoForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        propuesta = form.save(commit=False)
        propuesta.pelicula = pelicula
        propuesta.save()
        messages.success(request, _("Sugerencia guardada."))
        return redirect("detalle_pelicula", id=pelicula.pk)
    return render(request, "sugerencias/plato.html", {"pelicula": pelicula, "form": form})

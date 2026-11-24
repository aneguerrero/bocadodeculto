from django.contrib.staticfiles import finders
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views.decorators.vary import vary_on_headers

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from .forms import SugerenciaForm
from .catalogo_i18n import filtrar_catalogo

from .models import Pais, Pelicula, Plato


def portada(request):
    paises = Pais.objects.order_by("nombre").prefetch_related(
        Prefetch(
            "platos",
            queryset=(
                Plato.objects.select_related("pais_origen")
                .annotate(num_peliculas=Count("peliculas", distinct=True))
                .order_by("-num_peliculas", "nombre")
            ),
        )
    )

    platos_destacados = []
    for pais in paises:
        platos_del_pais = list(pais.platos.all())
        if platos_del_pais:
            platos_destacados.append(platos_del_pais[0])

    return render(
        request,
        "portada.html",
        {
            "platos_destacados": platos_destacados,
            # Las tres imágenes decorativas de portada enlazan con sus fichas reales.
            "plato_batido": Plato.objects.filter(nombre="Batido de 5 Dólares").first(),
            "plato_paella": Plato.objects.filter(nombre="Paella valenciana").first(),
            "plato_ramen": Plato.objects.filter(nombre="Ramen de Cerdo").first(),
            "total_paises": Pais.objects.count(),
            "total_platos": Plato.objects.count(),
            "total_peliculas": Pelicula.objects.count(),
        },
    )


@vary_on_headers("X-Requested-With")
def lista_platos(request):
    q = request.GET.get("q", "").strip()
    platos = (
        Plato.objects.select_related("pais_origen")
        .annotate(num_peliculas=Count("peliculas", distinct=True))
        .order_by("nombre")
    )
    if q:
        platos = filtrar_catalogo(platos, "nombre", q)
    parcial = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    plantilla = "platos/_tarjetas.html" if parcial else "platos/lista.html"
    return render(request, plantilla, {"platos": platos, "q": q})


def detalle_plato(request, id):
    plato = get_object_or_404(
        Plato.objects.select_related("pais_origen")
        .annotate(num_peliculas=Count("peliculas", distinct=True))
        .prefetch_related("peliculas__pais"),
        id=id,
    )
    return render(request, "platos/detalle.html", {"plato": plato})


@vary_on_headers("X-Requested-With")
def lista_paises(request):
    q = request.GET.get("q", "").strip()
    paises = Pais.objects.annotate(
        num_platos=Count("platos", distinct=True),
        num_peliculas=Count("peliculas", distinct=True),
    ).order_by("nombre")
    if q:
        paises = filtrar_catalogo(paises, "nombre", q)
    paises = list(paises)

    # Conserva los sellos ilustrados del catálogo y usa uno genérico para
    # países nuevos que todavía no tengan una imagen propia.
    for pais in paises:
        sello = f"images/sellos/sello-{slugify(pais.nombre)}.jpg"
        pais.imagen_sello = sello if finders.find(sello) else "images/sello.png"

    parcial = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    plantilla = "paises/_tarjetas.html" if parcial else "paises/lista.html"
    return render(request, plantilla, {"paises": paises, "q": q})


def detalle_pais(request, id):
    pais = get_object_or_404(
        Pais.objects.prefetch_related(
            Prefetch(
                "platos",
                queryset=Plato.objects.order_by("nombre").prefetch_related("peliculas"),
            ),
        ),
        id=id,
    )
    return render(request, "paises/detalle.html", {"pais": pais})


@vary_on_headers("X-Requested-With")
def lista_peliculas(request):
    q = request.GET.get("q", "").strip()
    peliculas = (
        Pelicula.objects.select_related("pais")
        .annotate(num_platos=Count("platos_maridados", distinct=True))
        .order_by("titulo")
    )
    if q:
        peliculas = filtrar_catalogo(peliculas, "titulo", q)
    parcial = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    plantilla = "peliculas/_tarjetas.html" if parcial else "peliculas/lista.html"
    return render(request, plantilla, {"peliculas": peliculas, "q": q})


def detalle_pelicula(request, id):
    pelicula = get_object_or_404(
        Pelicula.objects.select_related("pais").prefetch_related(
            "platos_maridados__pais_origen"
        ),
        id=id,
    )
    return render(request, "peliculas/detalle.html", {"pelicula": pelicula})


def sugerir_pelicula(request, id):
    plato = get_object_or_404(Plato, pk=id)
    datos = request.POST if request.method == "POST" else None
    form = SugerenciaForm(datos)
    if request.method == "POST" and form.is_valid():
        propuesta = form.save(commit=False)
        propuesta.plato = plato
        propuesta.save()
        messages.success(request, _("Sugerencia guardada."))
        return redirect("detalle_plato", id=plato.pk)
    return render(request, "sugerencias/nueva.html", {
        "plato": plato,
        "form": form,
    })

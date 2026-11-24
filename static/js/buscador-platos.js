const form = document.querySelector("#buscar");
const campo = document.querySelector("#q");
const resultados = document.querySelector("#resultados");
let ultimaPeticion = 0;

async function buscar(evento) {
    evento.preventDefault();
    const turno = ++ultimaPeticion;
    const url = new URL(form.action);
    if (campo.value.trim()) url.searchParams.set("q", campo.value.trim());
    try {
        const respuesta = await fetch(url, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
        if (!respuesta.ok) throw new Error("Error de búsqueda");
        const tarjetas = await respuesta.text();
        if (turno !== ultimaPeticion) return;
        resultados.innerHTML = tarjetas;
        history.replaceState(null, "", url);

        // El selector debe conservar el filtro nuevo, no el de la carga inicial.
        document.querySelectorAll('.selector-idioma input[name="next"]').forEach(input => {
            const destino = new URL(input.value, location.origin);
            destino.search = url.search;
            input.value = destino.pathname + destino.search;
        });
    } catch {
        if (turno === ultimaPeticion) location.assign(url);
    }
}

form.addEventListener("submit", buscar);
document.querySelector("#limpiar").addEventListener("click", evento => {
    campo.value = "";
    buscar(evento);
});

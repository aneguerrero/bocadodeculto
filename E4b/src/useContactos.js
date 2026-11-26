
import { ref } from 'vue';

export function useContactos() {

    const contactos = ref([]);
    let siguienteId = 1;

    function crearContacto(datos) {
        const nuevoContacto = {
            id: siguienteId++,
            nombre: datos.nombre,
            email: datos.email,
            telefono: String(datos.telefono)
        };

        contactos.value.push(nuevoContacto);
    }

    function borrarContacto(id) {
        contactos.value = contactos.value.filter(
            contacto => contacto.id !== id
        );
    }

    return {
        contactos,
        crearContacto,
        borrarContacto
    };
}

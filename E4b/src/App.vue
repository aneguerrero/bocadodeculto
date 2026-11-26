<script setup>
import { ref } from 'vue';
import { useContactos } from './useContactos.js';

// Obtenemos la lista y las funciones para gestionar contactos
const { contactos, crearContacto, borrarContacto } = useContactos();

// Datos del formulario
const nuevoContacto = ref({
    nombre: '',
    email: '',
    telefono: ''
});

// Función para añadir un contacto
function agregarContacto() {
    crearContacto({
        nombre: nuevoContacto.value.nombre,
        email: nuevoContacto.value.email,
        telefono: nuevoContacto.value.telefono
    });

    // Vaciamos el formulario después de añadirlo
    nuevoContacto.value = {
        nombre: '',
        email: '',
        telefono: ''
    };
}
</script>

<template>
    <div class="pagina-agenda">

        <!-- Cabecera de Bocado de Culto -->
        <header class="cabecera">
            <div class="banner">
                <img
                    src="/bocado/images/logo.png"
                    alt="Bocado de Culto"
                    class="logo"
                >
            </div>
        </header>

        <!-- Contenido principal -->
        <div class="contenedor-principal">
            <main class="fondo-menu">

                <!-- Título de la agenda -->
                <div class="encabezado-agenda">

                  <div class="encabezado-texto">
                      <h1 class="titulo-menu">
                           Agenda de contactos
                      </h1>

                      <p class="subtitulo-agenda">
                          Personas que siempre quieres tener a mano
                      </p>
                  </div>

                </div>

                <!-- Formulario -->
                <section class="bloque-agenda">

                    <h2>Añadir contacto</h2>

                    <form @submit.prevent="agregarContacto">

                        <div class="campos-formulario">

                            <div class="campo">
                                <label for="nombre">Nombre</label>
                                <input
                                    id="nombre"
                                    v-model="nuevoContacto.nombre"
                                    type="text"
                                    placeholder="Nombre del contacto"
                                    required
                                >
                            </div>

                            <div class="campo">
                                <label for="email">Email</label>
                                <input
                                    id="email"
                                    v-model="nuevoContacto.email"
                                    type="email"
                                    placeholder="correo@ejemplo.com"
                                    required
                                >
                            </div>

                            <div class="campo">
                                <label for="telefono">Teléfono</label>
                                <input
                                    id="telefono"
                                    v-model="nuevoContacto.telefono"
                                    type="text"
                                    placeholder="600123456"
                                    required
                                >
                            </div>

                        </div>

                        <button class="btn-principal" type="submit">
                            Añadir contacto
                        </button>

                    </form>

                </section>

                <!-- Lista de contactos -->
                <section class="bloque-agenda">

                    <h2>Mis contactos</h2>

                    <p v-if="contactos.length === 0" class="sin-contactos">
                        Todavía no tienes contactos en tu agenda.
                    </p>

                    <div v-else class="lista-contactos">

                        <article
                            v-for="contacto in contactos"
                            :key="contacto.id"
                            class="contacto-card"
                        >

                            <div class="contacto-contenido">

                                <div class="contacto-datos">
                                    <h3>{{ contacto.nombre }}</h3>
                                    <p>Email: {{ contacto.email }}</p>
                                    <p>Teléfono: {{ contacto.telefono }}</p>
                                </div>
                      
                                <button
                                    class="btn-borrar"
                                    type="button"
                                    @click="borrarContacto(contacto.id)"
                                >
                                    Borrar
                                </button>

                            </div>

                        </article>

                    </div>

                </section>

            </main>
        </div>

        <!-- Pie de página -->
        <footer class="pie-agenda">
          <div class="footer-contenido">
            <p class="footer-copy">
              Bocado de Culto · Agenda de contactos
            </p>
          </div>
        </footer>
    </div>
</template>


# Bocado de Culto - Agenda E4b

## Descripción

Agenda de contactos desarrollada con Vue 3 y Vite.
Utiliza Firebase Authentication y Cloud Firestore para almacenar los contactos de cada visitante.

## Tecnologías

- Vue 3
- Vite
- Firebase Authentication (autenticación anónima)
- Cloud Firestore
- VueFire

## Instalación y ejecución

Desde la carpeta E4b:

npm ci
npm run dev

## Compilación

npm run build

## Configuración de Firebase

Proyecto: Bocado De Culto

El archivo src/firebase.js contiene la configuración
de la aplicación web de Firebase.

Se utiliza autenticación anónima para identificar
a cada visitante.

Los contactos se almacenan en:

usuarios/{uid}/contactos/{id}

Cada visitante puede consultar, crear y eliminar
únicamente sus propios contactos.

## Reglas de seguridad

Las reglas están definidas en firestore.rules.

Para aplicarlas:
1. Abrir Firebase Console.
2. Entrar en Firestore Database.
3. Seleccionar Reglas.
4. Copiar el contenido de firestore.rules.
5. Pulsar Publicar.

## Pruebas realizadas

- Crear contactos: correcto.
- Persistencia tras recargar: correcto.
- Eliminar contactos: correcto.
- Aislamiento entre sesiones: correcto.
- Compilación inicial: correcta.
- npm audit tras actualizar dependencias: 0 vulnerabilidades.

## Publicación

URL de Netlify: pendiente de confirmar.

Validación HTML W3C: pendiente.
Validación CSS W3C: pendiente.
Pruebas en producción: pendientes.

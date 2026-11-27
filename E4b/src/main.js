import { createApp } from "vue";
import { VueFire } from "vuefire";
import { signInAnonymously } from "firebase/auth";
import { auth, firebaseApp } from "./firebase.js";
import App from "./App.vue";
import "./assets/agenda.css";

async function arrancar() {
  try {
    await auth.authStateReady();

    const usuario = auth.currentUser ||
      (await signInAnonymously(auth)).user;

    const app = createApp(App);

    app.use(VueFire, { firebaseApp });

    app.provide("uidAgenda", usuario.uid);

    app.mount("#app");

  } catch (error) {
    console.error(error.code || error.message);

    document.querySelector("#app").textContent =
      "No se pudo abrir la agenda. Comprueba la conexión y recarga.";
  }
}

arrancar();

import { inject } from "vue";
import { useCollection } from "vuefire";
import { collection, addDoc, deleteDoc, doc } from "firebase/firestore";
import { db } from "./firebase.js";

export function useContactos() {
  const uid = inject("uidAgenda");

  const lista = collection(db, "usuarios", uid, "contactos");

  const {
    data: contactos,
    pending: cargando,
    error
  } = useCollection(lista);

  async function crearContacto(datos) {
    await addDoc(lista, {
      nombre: datos.nombre,
      email: datos.email,
      telefono: datos.telefono
    });
  }

  async function borrarContacto(id) {
    await deleteDoc(doc(lista, id));
  }

  return {
    contactos,
    cargando,
    error,
    crearContacto,
    borrarContacto
  };
}

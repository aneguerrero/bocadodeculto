import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyBpWttldNQ24-vzIst-pfx9KCU7go_Gsd0",
  authDomain: "bocado-de-culto.firebaseapp.com",
  projectId: "bocado-de-culto",
  storageBucket: "bocado-de-culto.firebasestorage.app",
  messagingSenderId: "611705098931",
  appId: "1:611705098931:web:6996e1011b3ad3b9b916c6"
};

export const firebaseApp = initializeApp(firebaseConfig);
export const auth = getAuth(firebaseApp);
export const db = getFirestore(firebaseApp);

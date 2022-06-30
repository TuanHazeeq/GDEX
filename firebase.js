// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { initializeFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCVMU8xYMQ11S9NfcNy3jhAEMV97zJrZ9s",
  authDomain: "gifted-chat-app-2dbb8.firebaseapp.com",
  projectId: "gifted-chat-app-2dbb8",
  storageBucket: "gifted-chat-app-2dbb8.appspot.com",
  messagingSenderId: "404907895393",
  appId: "1:404907895393:web:84ffadcad81dd84db51820"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const auth = getAuth(app);
const db = initializeFirestore(app, {experimentalForceLongPolling: true});

export { db, auth };
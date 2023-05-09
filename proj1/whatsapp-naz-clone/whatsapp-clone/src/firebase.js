import firebase from 'firebase';

const firebaseConfig = {
    apiKey: "AIzaSyAaSuJTd4nv2K4lfwLjhn73tgyoYF9oX9g",
    authDomain: "whatsapp-clone-e8bbb.firebaseapp.com",
    projectId: "whatsapp-clone-e8bbb",
    storageBucket: "whatsapp-clone-e8bbb.appspot.com",
    messagingSenderId: "575454579726",
    appId: "1:575454579726:web:450afc9c51606c81b5c05f"
  };

  const firebaseApp = firebase.initializeApp(firebaseConfig);
  const db = firebaseApp.firestore();
  const auth = firebase.auth();
  const provider = new firebase.auth.GoogleAuthProvider();

  export { auth, provider };
  export default db;
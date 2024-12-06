import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

firebaseConfig = {
    "apiKey": "AIzaSyAUesDUcgX8JKDvboFdcaN6j9ki5zwZ4QM",
    "authDomain": "flask-chats.firebaseapp.com",
    "databaseURL": "https://flask-chats-default-rtdb.firebaseio.com",
    "projectId": "flask-chats",
    "storageBucket": "flask-chats.firebasestorage.app",
    "messagingSenderId": "276919289662",
    "appId": "1:276919289662:web:5ec0484a643104d4648e6f",
    "measurementId": "G-5PHTF493L3",
}


fire = pyrebase.initialize_app(firebaseConfig)

cred = credentials.Certificate("flask-chats-firebase-adminsdk-8de6x-4a8add8b97.json") 
firebase_admin.initialize_app(cred)
db = firestore.client()
tum_kullanicilar = db.collection("users").get()

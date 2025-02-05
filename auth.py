import requests
import streamlit as st
from firebase_admin import auth, firestore
from firebase_config import db  # Asegúrate de que este archivo está configurado correctamente.

# Tu API Key de Firebase (puedes encontrarla en la configuración del proyecto en Firebase)
FIREBASE_API_KEY = "AIzaSyAoqF2MEOZRu7OzRVqavj2Usra5LXMF_L0"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
CLIENT_ID = "191271828470-f5tu532iuu4bbduqjos554dgam78lhcm.apps.googleusercontent.com"

REDIRECT_URI = "http://localhost:8501/__/auth/handler"  # O la URL de tu aplicación en producción

def validar_usuario_firestore(usuario, clave):
    """Valida usuario y clave desde Firestore"""
    try:
        docs = db.collection('usuarios').where('user', '==', usuario).stream()
        for doc in docs:
            user_data = doc.to_dict()
            if user_data['password'] == clave:
                return user_data  # Retorna datos del usuario si es válido
        return None
    except Exception as e:
        st.error(f"Error en autenticación: {e}")
        return None




def generar_google_login():
    """Genera la URL para el inicio de sesión con Google."""
    url = (
        f"{GOOGLE_AUTH_URL}?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=token&"
        f"scope=email%20profile"
    )
    return url
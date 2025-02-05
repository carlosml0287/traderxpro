import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase solo si no está inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate("traderxpro-3377e-firebase-adminsdk-fbsvc-7598deb875.json")
    firebase_admin.initialize_app(cred)

# Instanciar el cliente de Firestore
db = firestore.client()

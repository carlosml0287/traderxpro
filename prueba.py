from firebase_config import db

def test_connection():
    try:
        docs = db.collection("usuarios").stream()
        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")
        print("✅ Conexión exitosa a Firestore")
    except Exception as e:
        print(f"❌ Error conectando a Firestore: {e}")

if __name__ == "__main__":
    test_connection()

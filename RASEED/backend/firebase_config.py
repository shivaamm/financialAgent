import firebase_admin
from firebase_admin import credentials, firestore, storage

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'raseed-e5140.firebasestorage.app'
    })

db = firestore.client()
storage_bucket = storage.bucket()

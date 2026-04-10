# database.py (FIREBASE FIRESTORE UPDATE)
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
from config import Config

class Database:
    def __init__(self):
        self.db = None

    async def connect(self):
        try:
            cred = credentials.Certificate(Config.FIREBASE_CRED_PATH)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("✅ Firebase Firestore Connected Successfully.")
        except Exception as e:
            print(f"⚠️ Firebase Connection Error: {e}\n(Make sure firebase.json exists)")

    async def add_user(self, user_id):
        if self.db:
            doc_ref = self.db.collection('users').document(str(user_id))
            await asyncio.to_thread(doc_ref.set, {'id': user_id}, merge=True)

    async def get_all_users(self):
        if self.db:
            docs = await asyncio.to_thread(self.db.collection('users').get)
            return [doc.to_dict().get('id') for doc in docs]
        return []

    async def get_stats(self):
        if not self.db: return 0, 0
        users = await asyncio.to_thread(self.db.collection('users').count().get)
        links = await asyncio.to_thread(self.db.collection('links').count().get)
        return users[0][0].value, links[0][0].value

    async def save_link(self, unique_id, message_id, expire_at=0):
        if self.db:
            data = {'message_id': message_id, 'expire_at': expire_at}
            await asyncio.to_thread(self.db.collection('links').document(unique_id).set, data)

    async def get_link(self, unique_id):
        if self.db:
            doc = await asyncio.to_thread(self.db.collection('links').document(unique_id).get)
            if doc.exists:
                return doc.to_dict()
        return None

    async def delete_link(self, unique_id):
        if self.db:
            await asyncio.to_thread(self.db.collection('links').document(unique_id).delete)

db = Database()
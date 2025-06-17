import os
import json
import base64
from firebase_admin import credentials, firestore, initialize_app

cred_data = os.environ.get("GOOGLE_CREDENTIALS")

if cred_data:
    decoded = base64.b64decode(cred_data).decode("utf-8")
    cred_json = json.loads(decoded)
    cred = credentials.Certificate(cred_json)
else:
    cred = credentials.Certificate("mensmentalhealth.json")

initialize_app(cred)

db = firestore.client()

def save_chat(session_id, user_msg, bot_msg):
    session_ref = db.collection('chat_sessions').document(session_id)
    session_ref.set({
        "history": firestore.ArrayUnion([{"user": user_msg, "bot": bot_msg}])
    }, merge=True)

def get_chat_history(session_id):
    try:
        session_ref = db.collection('chat_sessions').document(session_id)
        session_doc = session_ref.get()
        if session_doc.exists:
            data = session_doc.to_dict()
            return data.get("history", [])
        else:
            return []
    except Exception as e:
        raise RuntimeError(f"Failed to get chat history for {session_id}: {e}")


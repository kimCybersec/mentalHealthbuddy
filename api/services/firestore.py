import os
import json
import base64
from firebase_admin import credentials, firestore, initialize_app

cred_data = os.environ.get("GOOGLE_CREDENTIALS")

if cred_data:
    # 🔥 Decode from base64 to JSON string
    decoded = base64.b64decode(cred_data).decode("utf-8")
    cred_json = json.loads(decoded)
    cred = credentials.Certificate(cred_json)
else:
    # Optional fallback for local testing
    cred = credentials.Certificate("mensmentalhealth.json")

initialize_app(cred)

db = firestore.client()

def save_chat(session_id, user_message, bot_response):
    db.collection("chats").add({
        "session_id": session_id,
        "user": user_message,
        "bot": bot_response,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

def get_chat_history(session_id):
    docs = db.collection("chats").where("session_id", "==", session_id).order_by("timestamp").stream()
    return [{"user": doc.to_dict()['user'], "bot": doc.to_dict()['bot']} for doc in docs]

import os
import json
from firebase_admin import credentials, firestore, initialize_app

cred_data = os.environ.get("GOOGLE_CREDENTIALS")

if cred_data:
    cred_json = json.loads(cred_data)
    cred = credentials.Certificate(cred_json)
else:
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

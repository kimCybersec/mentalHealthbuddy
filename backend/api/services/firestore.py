import firebase_admin 
from firebase_admin import credentials, firestore 
import os 
import base64

if not firebase_admin._apps: 
    cred_data = base64.b64decode(os.getenv("GOOGLE_CREDENTIALS")) 
    cred = credentials.Certificate.from_service_account_info(eval(cred_data)) 
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_chat(session_id, user_message, bot_response): 
    db.collection("chats").add({ "session_id": session_id, "user": user_message, "bot": bot_response, "timestamp": firestore.SERVER_TIMESTAMP })

def get_chat_history(session_id): 
    docs = db.collection("chats").where("session_id", "==", session_id).order_by("timestamp").stream() 
    return [{"user": doc.to_dict()['user'], "bot": doc.to_dict()['bot']} for doc in docs]
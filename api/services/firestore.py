import firebase_admin
from firebase_admin import firestore, credentials
import os
from datetime import datetime

if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebase_admin.initialize_app(cred)
    
db = firestore.client()
chatCollection = "chatHistory"

def saveMessage(sessionId: str, role: str, content: str):    
    db.collection(chatCollection).document(sessionId).collection('messages').add({
        'timestamp': datetime.utcnow(),
        'role': role,
        'content': content,
    })
    

def getHistory(sessionId: str):
    docs = db.collection(chatCollection).document(sessionId).collection('messages').order_by('timestamp').stream()    
    return [{"role":doc.to_dict()['role'], "content": doc.to_dict()['content']} for doc in docs]

def clearHistory(sessionId: str):
    messages = db.collection(chatCollection).document(sessionId).collection('messages').stream()
    for message in messages:
        message.reference.delete()


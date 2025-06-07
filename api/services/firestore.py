import os
from google.cloud import firestore
from datetime import datetime
from typing import List, Dict, Optional
import uuid

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mensmentalhealth.json"

db = firestore.Client()
COLLECTIONNAME = "chatSessions"

def createSessionId() -> str:
    return str(uuid.uuid4())

def saveMessage(sessionId: str, role: str, content: str, lang: str = "en") -> None:
    doc_ref = db.collection(COLLECTIONNAME).document(sessionId).collection("messages").document()
    doc_ref.set({
        "role": role,
        "content": content,
        "lang": lang,
        "timestamp": datetime.utcnow()
    })

def getHistory(session_id: str) -> List[Dict]:
    messages_ref = db.collection(COLLECTIONNAME).document(session_id).collection("messages")
    messages = messages_ref.order_by("timestamp").stream()

    return [
        {
            "role": msg.get("role"),
            "content": msg.get("content")
        }
        for msg in (m.to_dict() for m in messages)
    ]
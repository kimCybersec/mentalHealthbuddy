from flask import Blueprint, request, jsonify
from api.services.openaiHelper import OpenAIClient
from api.services.safetyChecker import checkSafety
from api.services.firestore import saveMessage, getHistory, createSessionId
from api.middleware.rateLimiter import rateLimiter
from api.utils.logger import logger

chatBp = Blueprint("chat", __name__)
client = OpenAIClient()

@chatBp.route("/chat", methods=["POST"])
@rateLimiter
def chat():
    try:
        data = request.get_json()
        lang = data.get("language", "en")
        input = data.get("messages")
        sessionId = data.get("sessionId") or createSessionId()

        if not input:
            return jsonify({"error": "You haven't talked to me yet"}), 400
        
        saveMessage(sessionId, "user", input, lang)
        
        messages = getHistory(sessionId)
        
        result = client.generateResponse(messages, lang, sessionId)
        reply = result["reply"]
        
        saveMessage(sessionId, "assistant", reply, lang)
        
        return jsonify({
            "reply": reply,
            "sessionId": sessionId,
            "safety_triggered": result["safety_triggered"]
        })
    
    except Exception as e:
        logger.exception("chat route failed")
        return jsonify({"error": str(e)}), 500

@chatBp.route("/history/<session_id>", methods=["GET"])
def chatHistory():
    data = request.get_json()
    sessionId = data.get("sessionId")
    
    if not sessionId:
        return jsonify({"error": "Missing a sessionId"}), 400
    
    messages = getHistory(sessionId)
    return jsonify(messages)


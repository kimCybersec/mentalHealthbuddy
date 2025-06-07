from flask import Blueprint, request, jsonify
from api.services.openaiHelper import OpenAIClient
from api.services.safetyChecker import checkSafety, getCrisisResources
from api.services.firestore import store_chat, retrieve_chat, clear_chat
from api.middleware.rateLimiter import rate_limiter
from api.utils.logger import logger

chatBp = Blueprint("chat", __name__)
openai_client = OpenAIClient()

@chatBp.route("/chat", methods=["POST"])
@rate_limiter
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    session_id = data.get("session_id")

    if not session_id:
        return jsonify({"error": "Missing session ID"}), 400

    try:
        response = openai_client.generate_response(messages)
        
        if not response.get("safety_triggered", False):
            store_chat(session_id, messages[-1]["content"], response["reply"])
            return jsonify(response)
        else:
            crisis_info = getCrisisResources()
            return jsonify({
                **response,
                "crisis_resources": crisis_info
            }), 200
    except Exception as e:
        logger.exception("Error during /chat")
        return jsonify({"error": str(e)}), 500

@chatBp.route("/history/<session_id>", methods=["GET"])
def chat_history(session_id):
    try:
        history = retrieve_chat(session_id)
        return jsonify({"history": history}), 200
    except Exception as e:
        logger.exception("Error retrieving chat history")
        return jsonify({"error": "Could not retrieve history"}), 500

@chatBp.route("/clear/<session_id>", methods=["DELETE"])
def clear_session(session_id):
    try:
        clear_chat(session_id)
        return jsonify({"message": "Session cleared"}), 200
    except Exception as e:
        logger.exception("Error clearing session")
        return jsonify({"error": "Could not clear session"}), 500
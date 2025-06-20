from flask import Blueprint, request, jsonify 
from api.middleware.rateLimiter import limiter 
from api.services.firestore import save_chat, get_chat_history 
from api.services.openaiHelper import generate_response 
from api.utils.logger import logger

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('', methods=['POST']) 
@limiter 
def chat(): 
    try: 
        data = request.get_json() 
        messages = data.get("messages", []) 
        lang = data.get("lang", "en") 
        session_id = data.get("session_id", "anonymous")

        result = generate_response(messages, lang)
        save_chat(session_id, messages[-1]['content'], result['reply'])
        return jsonify(result)

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@chat_bp.route('/history/<session_id>', methods=['GET']) 
@limiter 
def history(session_id): 
    try: 
        logger.info(f"Fetching history for session: {session_id}")
        history = get_chat_history(session_id) 
        logger.info(f"History result: {history}")
        return jsonify({"history": history}) 
    
    except Exception as e: 
        logger.error(f"History error for session {session_id}: {str(e)}") 
        return jsonify({"error": str(e)}), 500

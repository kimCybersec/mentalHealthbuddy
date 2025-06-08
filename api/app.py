from flask import Flask
from flask_cors import CORS

from routes.chat import chat_bp
from utils.logger import logger

app = Flask(__name__)
CORS(app)

logger()

app.register_blueprint(chat_bp, url_prefix="/api/chat")

@app.route("/", methods=["GET"])
def index():
    return {"message": "Mental Health Chatbot API is running."}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

    @app.route('/')
    def index():
        return {"message": "Mental Health Bot API is running."}

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

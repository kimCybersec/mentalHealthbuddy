from flask import Flask 
from api.routes.chat import chat_bp 
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)

app.register_blueprint(chat_bp, url_prefix='/chat')
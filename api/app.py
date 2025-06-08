# app.py

from flask import Flask
from flask_cors import CORS
from api.routes.chat import chat_bp  # Adjust if your blueprint is in a different path
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(chat_bp, url_prefix='/api/chat')

@app.route('/')
def home():
    return {'message': 'Mental Health Chatbot API is live!'}

if __name__ == '__main__':
    app.run(debug=True)

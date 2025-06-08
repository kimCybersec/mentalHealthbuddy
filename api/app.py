from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp  
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_bp, url_prefix='/api/chat')

@app.route('/')
def home():
    return {'message': 'Mental Health Chatbot API is live!'}

if __name__ == '__main__':
    app.run(debug=True)

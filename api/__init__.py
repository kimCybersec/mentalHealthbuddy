from flask import Flask
from api.routes.chat import chatBp

def createApp():
    app = Flask(__name__)
    
    app.register_blueprint(chatBp, url_prefix='/chat')
    
    return app
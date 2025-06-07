from api.routes.chat import chatBp
from flask import Flask
from flask_cors import CORS

def createApp():
    app = Flask(__name__)
    app.secret_key = "rkd7f1a2e0c6b749d5a84f958c3b9f2ae087bbeb0f90f6a07c98e781f43f96fc02"
    CORS(app, supports_credentials=True)

    app.register_blueprint(chatBp)
    return app

app = createApp()
if __name__ == "__main__":
    app.run(debug=True)

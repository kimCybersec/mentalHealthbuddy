from .app import app 
from flask import send_from_directory

@app.route('/')
def serveIndex():
    return send_from_directory("frontend/templates", "index.html")

@app.route('/<path:path>')
def serveStatic(path):
    return send_from_directory("frontend/public", path)

if __name__ == "__main__":
    app.run()
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app,resources={r"/*":{"origins":"*"}})
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app,cors_allowed_origins="*")


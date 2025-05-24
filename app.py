from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import random 

app = Flask(__name__)
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
  return render_template('index.html')

@socketio.on("Connect")
def handle_connect():
    username = f"User{random.randint(1000,9999)}"
    # Using a reliable avatar service
    avatar_url = f"https://api.dicebear.com/7.x/bottts/svg?seed={username}"

    users[request.sid] = {
       "username": username, "avatar": avatar_url
    }

    emit("user_joined", {
       "username": username, "avatar": avatar_url
    }, broadcast=True)
    emit("set_username", {
       "username": username
    })


@socketio.on("disconnect")
def handdle_disconnect():
    username = users.pop(request.sid, None)
    if username:
        emit("user_Left", {
            "username": username["username"],
            "avatar": username["avatar"]
        }, broadcast=True)
        

@socketio.on("send_message")
def handle_Message(data):
    user = users.get(request.sid)
    if user:
        emit("new_message", {
            "message": data["message"],
            "username": user["username"],
            "avatar": user["avatar"]
        }, broadcast=True)
        
@socketio.on("update_username")
def handle_update_username(data):
    old_user_name = users[request.sid]["username"]
    users[request.sid]["username"] = data["username"]
    emit("username_updated", {
        "old_username": old_user_name,
        "new_username": data["username"]
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
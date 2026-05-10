from flask_socketio import emit, join_room, leave_room
from .extensions import socketio
from flask_login import current_user

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        join_room(f"user_{current_user.id}")
        print(f"User {current_user.id} connected and joined room.")

@socketio.on('join_note')
def handle_join_note(data):
    note_id = data.get('note_id')
    if note_id:
        join_room(f"note_{note_id}")
        emit('status', {'msg': f'Joined note room {note_id}'})

@socketio.on('send_message')
def handle_send_message(data):
    note_id = data.get('note_id')
    message = data.get('message')
    if note_id and message:
        # Emit to the note room for live chat/comments
        emit('new_message', {
            'user': current_user.username,
            'message': message,
            'avatar': current_user.avatar
        }, room=f"note_{note_id}")

def notify_user(user_id, message, link=None):
    socketio.emit('notification', {
        'message': message,
        'link': link
    }, room=f"user_{user_id}")

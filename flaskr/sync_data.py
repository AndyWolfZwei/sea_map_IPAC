from flask import current_app, g, session
from flask.cli import with_appcontext
from flask_socketio import emit
from flaskr import socketio
import random
import time

# @socketio.on('joined', namespace='/blog')
# def joined(message):
#     """Sent by clients when they enter a room.
#     A status message is broadcast to all people in the room."""
#     print(123)
#     # room = session.get('room')
#     emit('status', {'msg': random.randint(10)})

# @socketio.on('sync', namespace='/blog')
# def sync(message):
#     print(message['msg'])
#     time.sleep(5)
#     emit('status', {'msg': random.randint(10)})

@socketio.on('connect',namespace='/blog')
def handle_message(message):
    print('received message: ' + message)


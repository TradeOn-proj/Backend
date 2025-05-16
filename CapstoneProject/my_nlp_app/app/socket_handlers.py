from flask_socketio import SocketIO

def register_socketio_handlers(socketio : SocketIO):
    @socketio.on('message')
    def handle_message(msg):
        print('Message Received:', msg)
        socketio.send(msg)
from flask_socketio import SocketIO, emit
from flask import request

def register_socketio_handlers(socketio : SocketIO):
    @socketio.on('history')
    def view_messagehistory(data):
        roomid = data['roomid']

        emit('history', to=request.sid)

    @socketio.on('message')
    def handle_message(data):
        username = data['username']
        roomid = data['roomid']
        msg = data['msg']

        #db에 정보 저장

        msg_data = {'user' : username, 'msg' : msg}

        emit('message', msg_data, to=roomid)


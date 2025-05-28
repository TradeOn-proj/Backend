from flask_socketio import SocketIO, emit, join_room
from flask import request
from collections import defaultdict

chat_history = defaultdict(list)

def register_socketio_handlers(socketio : SocketIO):
    @socketio.on('join')
    def handle_join(data):
        username = data['username']
        roomId = data['roomid']
        join_room(roomId)

        # 입장 메시지
        emit('message', {
            'user': 'System',
            'msg': f'{username} joined the room.'
        }, to=roomId)

        # 이전 메시지 전달
        emit('chat_history', chat_history[roomId], to=request.sid)

    @socketio.on('message')
    def handle_message(data):
        username = data['username']
        roomId = data['roomid']
        msg = data['msg']

        #db에 정보 저장

        msg_data = {'user' : username, 'msg' : msg}
        chat_history[roomId].append(msg_data)

        emit('message', msg_data, to=roomId)


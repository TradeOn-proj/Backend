from flask import Blueprint, request, jsonify, render_template

bp_chat = Blueprint('chat', __name__, url_prefix= '/api/v1/chatrooms')

@bp_chat.route('', methods = ['GET'])
def view_chatrooms():
    userId = request.args.get("UserId")

    if not all([userId]):
        return jsonify({"message" : "userId 누락 또는 잘못된 요청"}), 400
    #db조회후 결과 찾기

    return jsonify({
        "chatrooms": [
        {
            "chatroomId": "string",
            "name": "string",
            "lastMessage": "string",
            "updatedAt": "2025-05-26T11:47:46.238Z"
        }
        ]
    }), 200

@bp_chat.route('', methods=['POST'])
def create_chatroom():
    data = request.get_json()

    participantIds = data.get("participantIds")
    relatedPostId = data.get("relatedPostId")
    name = data.get("name")

    if not all([participantIds, relatedPostId, name]):
        return jsonify({"message" : "필수 항목 누락 또는 유효하지 않은 요청"}), 400
    
    return jsonify({
        "chatroomId": "string",
        "name": "string",
        "createdAt": "2025-05-26T11:50:54.201Z"
    }), 201

@bp_chat.route('/<chatroomid>', methods = ['GET'])
def view_chatroomdetail(chatroomid):
    chatroomId = chatroomid

    #DB조회 없으면 404 오류

    return jsonify({
        "chatroomId": "string",
        "name": "string",
        "participants": [
            "string"
        ],
        "lastMessage": "string",
        "updatedAt": "2025-05-26T11:56:31.718Z"
    }), 200

@bp_chat.route('/<chatroomid>/messages', methods=['GET'])
def view_chatroommessages(chatroomid):
    chatroomId = chatroomid

    limit = request.args.get("limit", type=int)
    before = request.args.get("before")

    #db조회하고 없으면 404 오류

    return jsonify({
        "messages": [
        {
            "messageId": "string",
            "senderId": "string",
            "content": "string",
            "timestamp": "2025-05-26T12:00:44.933Z"
        }
        ]
    }), 200

@bp_chat.route('/<chatroomid>/messages', methods=['POST'])
def send_chatroommessages(chatroomid):
    chatroomId = chatroomid

    data = request.get_json()

    senderId = data.get("senderId")
    content = data.get("content")

    if not all([senderId, content]):
        return jsonify({"message" : "필드 누락 또는 형식 오류"}), 400
    
    #DB접근 후 없으면 404 오류

    return jsonify({
        "messageId": "string",
        "timestamp": "2025-05-26T12:09:16.665Z"
    }), 200

@bp_chat.route('/trade-promise', methods = ['POST'])
def promise_chatrooms():
    data = request.get_json()

    chatroomId = data.get("chatroomId")
    date = data.get("date")
    title = data.get("title")
    location = data.get("location")

    if not all([chatroomId, date, title, location]):
        return jsonify({"message" : "필드 누락 또는 형식 오류"}), 400
    
    #db조회 후 없으면 404 오류

    return jsonify({
        "promiseId": "string",
        "chatroomId": "string",
        "message": "string",
        "createdAt": "2025-05-26T12:17:09.051Z"
    }), 201
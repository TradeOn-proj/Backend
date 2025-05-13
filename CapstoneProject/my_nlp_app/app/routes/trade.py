from flask import Blueprint, request, jsonify

bp_trade = Blueprint('trade', __name__, url_prefix='/api/v1/trades')

@bp_trade.route('', methods = ['POST'])
def suggest_trade():
    data = request.get_json()

    proposing_item_id = data.get('proposing_item_id')
    target_post_id = data.get('target_post_id')

    if not all([proposing_item_id, target_post_id]):
        return jsonify({'400 Bad Request : "status error" : 잘못된 요청 데이터입니다다.'}), 400
    
    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 요청하신 게시물을 찾을 수 없습니다.'}), 404
    #이미 진행 중인 거래일시 409메세지 보내기

    #db접근해서 거래 등록하기

    return jsonify({
        'postid' : '새로 생성된 거래ID',
        'message' : '201 Created : "status success" : "교환 제안이 성공적으로 전송되었습니다!"'
    }), 201

@bp_trade.route('/<tradeid>/accept', methods=['PUT'])
def accept_trade(tradeid):

    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 해당 거래 제안을 찾을 수 없습니다.'}), 404

    data = request.get_json()

    accept_message = data.get('accept_message')

    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록

    return jsonify({
        'tradeid' : '수락된 거래 제안 ID',
        'current_status' : 'accepted',
        'message' : '200 OK : "status success" : "거래 제안을 수락했습니다. 상대방에게 알림이 전송됩니다."'
    }), 200

@bp_trade.route('/<tradeid>/reject', methods=['PUT'])
def reject_trade(tradeid):

    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 해당 거래 제안을 찾을 수 없습니다.'}), 404

    data = request.get_json()

    rejection_reason = data.get('rejection_reason')

    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록

    return jsonify({
        'tradeid' : '거절된 거래 제안 ID',
        'current_status' : 'rejected',
        'message' : '200 OK : "status success" : "거래 제안을 거절했습니다. 상대방에게 알림이 전송됩니다."'
    }), 200


@bp_trade.route('/<tradeid>/complete', methods=['PUT'])
def complete_trade(tradeid):

    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 해당 거래 제안을 찾을 수 없습니다.'}), 404

    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록

    return jsonify({
        'tradeid' : '완료된 거래 제안 ID',
        'user_confirmed' : 'true',
        'is_completed' : 'false',
        'message' : '200 OK : "status success" : "거래 완료를 확인했습니다. 상대방의 확인을 기다립니다."'
    }), 200
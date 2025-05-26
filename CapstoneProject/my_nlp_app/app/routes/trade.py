from flask import Blueprint, request, jsonify

bp_trade = Blueprint('trade', __name__, url_prefix='/api/v1/trades')

@bp_trade.route('/<tradeid>/accept', methods=['POST'])
def accept_trade(tradeid):
    tradeId = tradeid
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 해당 거래 제안을 찾을 수 없습니다.'}), 404

    data = request.get_json()

    userId = data.get("userId")

    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록

    return jsonify({
        "message": "Trade accepted successfully."
    }), 200

@bp_trade.route('/<tradeid>/complete', methods=['POST'])
def complete_trade(tradeid):
    tradeId = tradeid

    data = request.get_json()

    userId = data.get("userId")

    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 해당 거래 제안을 찾을 수 없습니다.'}), 404
    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록
    return jsonify({
        "status": "COMPLETED"
    }), 200

@bp_trade.route('/<tradeid>/review', methods=['POST'])
def reject_trade(tradeid):
    tradeId = tradeid

    data = request.get_json()

    reviewerId = data.get("reviewerId")
    rating = data.get("rating")
    comment = data.get("comment")

    if not all([reviewerId, rating, comment]):
        return jsonify({"error" : "잘못된 입력 또는 중복 리뷰"}), 400
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 해당 거래 제안을 찾을 수 없습니다.'}), 404

    return jsonify({
        "reviewId": "string"
    }), 200




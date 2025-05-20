# trade.py — Trade 모델 기반 거래 요청, 수락, 거절, 완료 API 구현

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.trade import Trade
from app.models.post import Post
from datetime import datetime

trade_bp = Blueprint("trade", __name__, url_prefix="/api/v1/trades")

# 거래 요청 생성 API — 인증 필요
@trade_bp.route('', methods=['POST'])
@jwt_required()
def create_trade():
    data = request.get_json()

    requester_id = get_jwt_identity()
    post_id = data.get("post_id")
    message = data.get("message", "")

    if not post_id:
        return jsonify({
            "status": "error",
            "message": "post_id는 필수입니다."
        }), 400

    trade = Trade(
        post_id=post_id,
        requester_id=requester_id,
        message=message,
        status="pending",
        created_at=datetime.utcnow()
    )

    db.session.add(trade)
    db.session.commit()

    return jsonify({
        "status": "success",
        "trade": {
            "id": trade.id,
            "post_id": trade.post_id,
            "requester_id": trade.requester_id,
            "status": trade.status,
            "message": trade.message,
            "created_at": trade.created_at.strftime('%Y-%m-%d %H:%M')
        }
    }), 201

# 거래 상태 변경 API (수락/거절/완료)
@trade_bp.route('/<int:trade_id>/<string:action>', methods=['PUT'])
@jwt_required()
def update_trade_status(trade_id, action):
    user_id = get_jwt_identity()
    trade = Trade.query.get(trade_id)

    if not trade:
        return jsonify({"status": "error", "message": "거래 요청을 찾을 수 없습니다."}), 404

    post = Post.query.get(trade.post_id)
    if not post or post.author_id != user_id:
        return jsonify({"status": "error", "message": "해당 거래를 변경할 권한이 없습니다."}), 403

    if action == 'accept':
        trade.status = 'accepted'
    elif action == 'reject':
        trade.status = 'rejected'
    elif action == 'complete':
        trade.status = 'completed'
    else:
        return jsonify({"status": "error", "message": "허용되지 않은 액션입니다."}), 400

    db.session.commit()

    return jsonify({"status": "success", "message": f"거래가 {action} 처리되었습니다."})

# 특정 게시글 거래 요청 목록 조회
@trade_bp.route('/post/<int:post_id>', methods=['GET'])
@jwt_required()
def get_trades_by_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get(post_id)
    if not post or post.author_id != user_id:
        return jsonify({"status": "error", "message": "해당 게시글에 접근할 수 없습니다."}), 403

    trades = Trade.query.filter_by(post_id=post_id).order_by(Trade.created_at.desc()).all()

    result = [{
        "trade_id": t.id,
        "requester_id": t.requester_id,
        "status": t.status,
        "message": t.message,
        "created_at": t.created_at.strftime('%Y-%m-%d')
    } for t in trades]

    return jsonify({"status": "success", "trades": result})

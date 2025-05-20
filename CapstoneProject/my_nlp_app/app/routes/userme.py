# userme.py — 사용자 개인 정보 및 탈퇴 기능 구현

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User

bp_userme = Blueprint('userme', __name__, url_prefix='/api/v1/users/me')

# 포인트 및 등급 조회
@bp_userme.route('/points-and-grade', methods=['GET'])
@jwt_required()
def view_pointandgrade():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"status": "error", "message": "사용자를 찾을 수 없습니다."}), 404

    # 등급 계산
    if user.points >= 3000:
        grade = "플래티넘"
    elif user.points >= 2000:
        grade = "골드"
    elif user.points >= 1000:
        grade = "실버"
    else:
        grade = "브론즈"

    return jsonify({
        "user_id": user.id,
        "points": user.points,
        "grade": grade,
        "grade_icon_url": f"{grade}_grade.png",
        "message": "200 OK : \"Status Success\" : \"해당유저의 포인트, 등급 현황입니다.\""
    }), 200

# 회원 탈퇴 기능
@bp_userme.route('/unregister', methods=['DELETE'])
@jwt_required()
def unregister():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"status": "error", "message": "사용자를 찾을 수 없습니다."}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "200 OK : \"status success\" : \"회원 탈퇴가 성공적으로 완료되었습니다!\""
    }), 200

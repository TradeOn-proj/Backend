# review.py — Review 모델 기반 리뷰 작성 및 조회 API 구현

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.review import Review
from datetime import datetime

review_bp = Blueprint("review", __name__, url_prefix="/api/v1/reviews")

# 리뷰 작성 API — 인증 필요
@review_bp.route('', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()

    reviewer_id = get_jwt_identity()
    user_id = data.get('user_id')  # 리뷰 대상자
    rating = data.get('rating')
    comment = data.get('comment', '')

    if not all([user_id, rating]):
        return jsonify({
            "status": "error",
            "message": "user_id와 rating은 필수입니다."
        }), 400

    review = Review(
        user_id=user_id,
        reviewer_id=reviewer_id,
        rating=rating,
        comment=comment,
        created_at=datetime.utcnow()
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        "status": "success",
        "review": {
            "id": review.id,
            "user_id": review.user_id,
            "reviewer_id": review.reviewer_id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.strftime('%Y-%m-%d %H:%M')
        }
    }), 201

# 특정 사용자 리뷰 목록 조회
@review_bp.route('/<int:userid>', methods=['GET'])
def get_user_reviews(userid):
    reviews = Review.query.filter_by(user_id=userid).order_by(Review.created_at.desc()).all()

    result = [{
        "review_id": r.id,
        "reviewer_id": r.reviewer_id,
        "rating": r.rating,
        "comment": r.comment,
        "date": r.created_at.strftime('%Y-%m-%d')
    } for r in reviews]

    return jsonify({
        "status": "success",
        "user_id": userid,
        "reviews": result
    }), 200

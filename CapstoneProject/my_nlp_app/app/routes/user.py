# user.py — User 모델 기반 회원가입, 로그인, 프로필, 추천 API 연동

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User
from app.models.post import Post
from app.models.review import Review

user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')

# 회원가입 API
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"msg": "필수 입력 항목이 누락되었습니다."}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "이미 존재하는 사용자입니다."}), 409

    hashed_pw = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "회원가입 완료"}), 201

# 로그인 API
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "사용자 이름 또는 비밀번호가 올바르지 않습니다."}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200

# 추천 게시물 API
@user_bp.route('/<int:userid>/recommended-posts', methods=['GET'])
def recommend(userid):
    keyword = request.args.get('keyword')
    category = request.args.get('category')
    limit = request.args.get('limit', default=5, type=int)

    if not keyword or not category:
        return jsonify({"msg": "keyword와 category는 필수입니다."}), 400

    posts = Post.query.filter(
        Post.keyword.ilike(f"%{keyword}%"),
        Post.category == category
    ).order_by(Post.created_at.desc()).limit(limit).all()

    result = [{
        "postid": p.id,
        "title": p.title,
        "thumbnail_image_url": p.thumbnail_image_url,
        "description": p.description,
        "author": p.author_id,
        "keyword": p.keyword,
        "category": p.category,
        "viewing": 0,  # 조회수 필드 아직 없음
        "recommendation_score": 1.0 - (i * 0.1)
    } for i, p in enumerate(posts)]

    return jsonify({"status": "success", "results": result}), 200

# 사용자 프로필 조회 API
@user_bp.route('/<int:userid>/profile', methods=['GET'])
def user_profile(userid):
    user = User.query.get(userid)
    if not user:
        return jsonify({"msg": "사용자를 찾을 수 없습니다."}), 404

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile_image_url": user.profile_image_url or "default.jpg",
            "registeredAt": user.created_at.strftime('%Y-%m-%d') if user.created_at else "",
            "current_points": user.points,
            "current_grade": user.grade or "브론즈",
            "grade_icon_url": f"{user.grade.lower()}_grade.png",
            "total_trades": 0,
            "completed_trades": 0,
            "cancellation_count": 0,
            "cancellation_warning": "false"
        }
    })

# 사용자 리뷰 목록 조회 API
@user_bp.route('/<int:userid>/reviews', methods=['GET'])
def user_review(userid):
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

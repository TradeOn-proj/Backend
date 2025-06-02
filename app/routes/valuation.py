# app/routes/valuation.py

import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from app.models.valuation_post import ValuationPost
from app.models.valuation_opinion import ValuationOpinion

bp_valuation = Blueprint('valuation', __name__, url_prefix='/api/v1/valuations')

# ----------------------
# 업로드된 파일 저장 설정
# ----------------------
# 실제 파일 업로드 시 저장될 로컬 디렉터리 경로 (Flask static 폴더 밑으로 두는 예시)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
# 허용할 확장자 목록
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    파일 이름에 허용된 확장자가 있는지 확인
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ------------------------------------------------
# GET: 가치 평가 게시글 목록 조회 (페이지네이션 + 카테고리 필터)
# ------------------------------------------------
@bp_valuation.route('', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_valuation_posts():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    category = request.args.get('category', type=str)

    query = ValuationPost.query
    if category:
        query = query.filter_by(category=category)

    pagination = query.order_by(
        ValuationPost.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    posts = []
    for post in pagination.items:
        opinions = [op.price for op in post.opinions if op.price is not None]
        total_evaluations = len(opinions)
        avg_price = sum(opinions) / total_evaluations if total_evaluations else 0

        posts.append({
            'postId': post.id,
            'title': post.title,
            'category': post.category,
            'totalEvaluations': total_evaluations,
            'averagePrice': avg_price,
            'createdAt': post.created_at.strftime('%Y-%m-%d %H:%M'),
            'image': post.image_url  # 문자열 URL
        })

    return jsonify({
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'posts': posts
    }), 200


# ------------------------------------------------
# POST: 가치 평가 게시글 작성 (JSON 또는 multipart/form-data 둘 다 처리)
# ------------------------------------------------
@bp_valuation.route('', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_valuation_post():
    # 1) 먼저, multipart/form-data로 실제 이미지 파일이 올라왔는지 확인
    image_url = None

    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            # 안전한 파일명으로 변환
            filename = secure_filename(file.filename)
            # 업로드 디렉터리가 없으면 생성
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            # 파일 저장
            file.save(save_path)
            # 예시: Flask static 폴더에서 /static/uploads/ 아래로 서빙한다고 가정
            # 이렇게 하면 브라우저에서 "https://<도메인>/static/uploads/<filename>" 으로 접근 가능
            image_url = f"/static/uploads/{filename}"
        else:
            return jsonify({'msg': '허용되지 않는 파일 형식입니다. (png, jpg, jpeg, gif만 가능)'}), 400

        # multipart/form-data로 넘어왔으므로, 텍스트 필드는 request.form 에서 가져오기
        form = request.form
    else:
        # JSON(application/json) 요청일 때
        form = request.get_json() or {}
        image_candidate = form.get('image')
        if image_candidate is not None:
            if not isinstance(image_candidate, str):
                return jsonify({'msg': 'image는 문자열(URL) 형태여야 합니다.'}), 400
            image_url = image_candidate

    # 2) 텍스트 필드 추출
    title = form.get('title')
    description = form.get('description')
    category = form.get('category')
    user_id = int(get_jwt_identity())

    if not title or not description or not category:
        return jsonify({'msg': 'title, description, category 필수'}), 400

    # 3) 새 게시글 객체 생성 & DB 저장
    new_post = ValuationPost(
        title=title,
        description=description,
        category=category,
        user_id=user_id,
        created_at=datetime.utcnow(),
        image_url=image_url  # 이미지가 없으면 None, 있으면 위에서 URL로 세팅됨
    )
    db.session.add(new_post)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ValuationPost 생성 오류: {e}")
        return jsonify({'msg': '서버 오류가 발생했습니다.'}), 500

    return jsonify({
        'postId': new_post.id,
        'title': new_post.title,
        'description': new_post.description,
        'category': new_post.category,
        'createdAt': new_post.created_at.strftime('%Y-%m-%d %H:%M'),
        'image': new_post.image_url
    }), 201


# ------------------------------------------------
# GET: 가치 평가 게시글 상세 조회
# ------------------------------------------------
@bp_valuation.route('/<int:postid>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_valuation_post(postid):
    post = ValuationPost.query.get(postid)
    if not post:
        return jsonify({'msg': '게시글을 찾을 수 없습니다.'}), 404

    opinions = [op.price for op in post.opinions if op.price is not None]
    avg_price = sum(opinions) / len(opinions) if opinions else 0
    total_evaluations = len(opinions)

    return jsonify({
        'postId': post.id,
        'title': post.title,
        'description': post.description,
        'category': post.category,
        'averagePrice': avg_price,
        'totalEvaluations': total_evaluations,
        'createdAt': post.created_at.strftime('%Y-%m-%d %H:%M'),
        'image': post.image_url
    }), 200


# ------------------------------------------------
# DELETE: 가치 평가 게시글 삭제
# ------------------------------------------------
@bp_valuation.route('/<int:postid>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_valuation_post(postid):
    post = ValuationPost.query.get(postid)
    if not post:
        return jsonify({'msg': '게시글을 찾을 수 없습니다.'}), 404

    current_user = int(get_jwt_identity())
    if post.user_id != current_user:
        return jsonify({'msg': '권한이 없습니다.'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'msg': '게시글 삭제 성공'}), 200


# ------------------------------------------------
# POST: 평가 의견 등록
# ------------------------------------------------
@bp_valuation.route('/<int:postid>/price', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_valuation_opinion(postid):
    post = ValuationPost.query.get(postid)
    if not post:
        return jsonify({'msg': '게시글을 찾을 수 없습니다.'}), 404

    data = request.get_json() or {}
    price = data.get('price')
    user_id = int(get_jwt_identity())

    if price is None:
        return jsonify({'msg': 'price 필수'}), 400

    existing = ValuationOpinion.query.filter_by(post_id=postid, user_id=user_id).first()
    if existing:
        return jsonify({'msg': '이미 평가한 게시글입니다.'}), 400

    new_opinion = ValuationOpinion(
        post_id=postid,
        user_id=user_id,
        price=price,
        created_at=datetime.utcnow()
    )
    db.session.add(new_opinion)
    db.session.commit()

    return jsonify({'msg': '의견 등록 성공'}), 201


# ------------------------------------------------
# GET: 게시글의 평균 가격 조회
# ------------------------------------------------
@bp_valuation.route('/<int:postid>/average', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_valuation_average(postid):
    post = ValuationPost.query.get(postid)
    if not post:
        return jsonify({'msg': '게시글을 찾을 수 없습니다.'}), 404

    opinions = [op.price for op in post.opinions if op.price is not None]
    valid_count = len(opinions)
    avg_price = sum(opinions) / valid_count if valid_count else 0

    return jsonify({
        'postId': post.id,
        'validCount': valid_count,
        'averagePrice': avg_price
    }), 200

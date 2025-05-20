# valuation_post.py — ValuationPost + ValuationOpinion 모델 기반 평가 게시물 및 의견 CRUD 구현

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.valuation_post import ValuationPost
from app.models.valuation import ValuationOpinion
from datetime import datetime

bp_valuation = Blueprint('valuation', __name__, url_prefix='/api/v1/valuation-posts')

# 가치 평가 게시물 목록 조회 (페이징 미적용 버전)
@bp_valuation.route('', methods=['GET'])
def view_valuation():
    posts = ValuationPost.query.order_by(ValuationPost.created_at.desc()).all()
    result = []
    for p in posts:
        result.append({
            "id": p.id,
            "title": p.title,
            "item_description_summary": p.item_description[:30],
            "author": {
                "id": p.author_id,
                "username": p.author.username if p.author else ""
            },
            "thumbnail_image_url": p.thumbnail_image_url,
            "opinion_count": len(p.opinions),
            "createdAt": p.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        })
    return jsonify({
        "valuation_posts": result,
        "total_count": len(result),
        "current_page": 1,
        "total_pages": 1,
        "page_size": len(result)
    })

# 가치 평가 게시물 작성
@bp_valuation.route('', methods=['POST'])
@jwt_required()
def post_valuation():
    data = request.get_json()
    user_id = get_jwt_identity()

    title = data.get('title')
    content = data.get('content')
    item_id = data.get('item_id')
    item_description = data.get('item_description')
    image_urls = data.get('image_urls')

    if not all([title, content, item_id, item_description, image_urls]):
        return jsonify({"status": "error", "message": "입력값 누락"}), 400

    post = ValuationPost(
        title=title,
        content=content,
        item_id=item_id,
        item_description=item_description,
        thumbnail_image_url=image_urls[0],
        author_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({
        "postid": post.id,
        "message": "가치 평가 게시물이 성공적으로 등록되었습니다."
    }), 201

# 가치 평가 게시물 상세 조회
@bp_valuation.route('/<int:postid>', methods=['GET'])
def view_valuation_detail(postid):
    post = ValuationPost.query.get(postid)
    if not post:
        return jsonify({"status": "error", "message": "게시물을 찾을 수 없습니다."}), 404

    opinions = ValuationOpinion.query.filter_by(post_id=post.id).all()
    opinion_result = [{
        "id": op.id,
        "post_id": op.post_id,
        "author": {
            "id": op.user_id,
            "username": op.user.username if op.user else ""
        },
        "content": op.content,
        "createdAt": op.created_at.strftime('%Y-%m-%d')
    } for op in opinions]

    return jsonify({
        "valuation_post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": {
                "id": post.author_id,
                "username": post.author.username if post.author else "",
                "profile_image_url": post.author.profile_image_url if post.author else ""
            },
            "images": [post.thumbnail_image_url],
            "createdAt": post.created_at.strftime('%Y-%m-%d'),
            "updatedAt": post.updated_at.strftime('%Y-%m-%d'),
            "views": post.views,
            "opinion_count": len(opinions)
        },
        "opinions": opinion_result
    })

# 가치 평가 댓글 등록
@bp_valuation.route('/<int:postid>/opinions', methods=['POST'])
@jwt_required()
def create_valuation_opinion(postid):
    data = request.get_json()
    user_id = get_jwt_identity()
    content = data.get('content')

    if not content:
        return jsonify({"status": "error", "message": "내용이 필요합니다."}), 400

    opinion = ValuationOpinion(
        post_id=postid,
        user_id=user_id,
        content=content,
        created_at=datetime.utcnow()
    )
    db.session.add(opinion)
    db.session.commit()

    return jsonify({
        "opinion_id": opinion.id,
        "message": "의견이 성공적으로 등록되었습니다."
    }), 201

# 가치 평가 댓글 삭제
@bp_valuation.route('/<int:postid>/opinions/<int:opinion_id>', methods=['DELETE'])
@jwt_required()
def delete_valuation_opinion(postid, opinion_id):
    user_id = get_jwt_identity()
    opinion = ValuationOpinion.query.filter_by(id=opinion_id, post_id=postid, user_id=user_id).first()
    if not opinion:
        return jsonify({"status": "error", "message": "삭제할 수 있는 댓글이 없습니다."}), 404

    db.session.delete(opinion)
    db.session.commit()

    return jsonify({"message": "댓글이 성공적으로 삭제되었습니다."})

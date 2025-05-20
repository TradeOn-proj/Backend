# post.py — Post 모델 기반 게시글 등록, 수정, 삭제, 조회 API 구현 및 DB 연동

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.post import Post
from datetime import datetime

post_bp = Blueprint("post", __name__, url_prefix="/api/v1/posts")

# 게시글 등록 API — 인증 필요
@post_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()

    author_id = get_jwt_identity()
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    keyword = data.get('keyword')
    thumbnail_image_url = data.get('thumbnail_image_url')

    if not all([title, description]):
        return jsonify({
            "status": "error",
            "message": "title과 description은 필수입니다."
        }), 400

    post = Post(
        title=title,
        description=description,
        author_id=author_id,
        category=category,
        keyword=keyword,
        thumbnail_image_url=thumbnail_image_url,
        created_at=datetime.utcnow()
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        "status": "success",
        "post": {
            "id": post.id,
            "title": post.title,
            "author_id": post.author_id,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M')
        }
    }), 201

# 게시글 목록 조회 API (옵션)
@post_bp.route('', methods=['GET'])
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    result = [{
        "id": p.id,
        "title": p.title,
        "author_id": p.author_id,
        "category": p.category,
        "keyword": p.keyword,
        "created_at": p.created_at.strftime('%Y-%m-%d')
    } for p in posts]

    return jsonify({
        "status": "success",
        "count": len(result),
        "posts": result
    }), 200

# 게시글 상세 조회
@post_bp.route('/<int:postid>', methods=['GET'])
def get_post(postid):
    post = Post.query.get(postid)
    if not post:
        return jsonify({"status": "error", "message": "게시글을 찾을 수 없습니다."}), 404

    return jsonify({
        "id": post.id,
        "title": post.title,
        "description": post.description,
        "author_id": post.author_id,
        "category": post.category,
        "keyword": post.keyword,
        "thumbnail_image_url": post.thumbnail_image_url,
        "created_at": post.created_at.strftime('%Y-%m-%d %H:%M')
    })

# 게시글 수정
@post_bp.route('/<int:postid>', methods=['PUT'])
@jwt_required()
def update_post(postid):
    post = Post.query.get(postid)
    user_id = get_jwt_identity()

    if not post:
        return jsonify({"status": "error", "message": "게시글을 찾을 수 없습니다."}), 404
    if post.author_id != user_id:
        return jsonify({"status": "error", "message": "작성자만 수정할 수 있습니다."}), 403

    data = request.get_json()
    post.title = data.get("title", post.title)
    post.description = data.get("description", post.description)
    post.category = data.get("category", post.category)
    post.keyword = data.get("keyword", post.keyword)
    post.thumbnail_image_url = data.get("thumbnail_image_url", post.thumbnail_image_url)

    db.session.commit()

    return jsonify({"status": "success", "message": "게시글이 수정되었습니다."})

# 게시글 삭제
@post_bp.route('/<int:postid>', methods=['DELETE'])
@jwt_required()
def delete_post(postid):
    post = Post.query.get(postid)
    user_id = get_jwt_identity()

    if not post:
        return jsonify({"status": "error", "message": "게시글을 찾을 수 없습니다."}), 404
    if post.author_id != user_id:
        return jsonify({"status": "error", "message": "작성자만 삭제할 수 있습니다."}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({"status": "success", "message": "게시글이 삭제되었습니다."})

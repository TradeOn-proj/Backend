from flask import Blueprint, request, jsonify

bp_post = Blueprint('post', __name__, url_prefix='/api/v1/posts')

@bp_post.route('', methods=['GET'])
def search_post():
    
    category = request.args.get("category")
    limit = request.args.get("limit", type = int)
    offset = request.args.get("offset", type = int)

        
    #db조회후 결과 찾기

    return jsonify({
        "postId": "string",
        "title": "string",
        "category": "string",
        "price": 0,
        "createdAt": "2025-05-25T12:08:59.068Z"   
    }), 200

@bp_post.route('', methods=['POST'])
def register_post():
    data = request.get_json()

    userId = data.get("userId")
    title = data.get("title")
    description = data.get("description")
    category = data.get("category")
    price = data.get("price")

    if not all([userId, title, description, category, price]):
        return jsonify({"필수 필드 누락"}), 400

    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록

    return jsonify({
        "postId" : "string",    
    }), 201

@bp_post.route('/recommend', methods=['GET'])
def post_recommend():
    userId = request.args.get("userId")

    #DB조회해서 유저 찾고 없으면 오류 반환

    return jsonify({
        "postId": "string",
        "title": "string",
        "category": "string",
        "price": 0
    }), 200

@bp_post.route('/<postid>', methods=['GET'])
def view_post(postid):
    postId = postid
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 요청하신 게시물을 찾을 수 없습니다.'}), 404

    return jsonify({      
        "postId": "string",
        "title": "string",
        "description": "string",
        "category": "string",
        "price": 0,
        "createdAt": "2025-05-25T12:27:38.805Z"
    }), 200

@bp_post.route('/<postid>', methods=['PUT'])
def update_post(postid):
    postId = postid
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 요청하신 게시물을 찾을 수 없습니다.'}), 404

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    category = data.get("category")
    price = data.get("price")
    
    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록

    return jsonify({"게시물 수정 성공"}), 200

@bp_post.route('/<postid>', methods=['DELETE'])
def delete_post(postid):
    postId = postid
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 요청하신 게시물을 찾을 수 없습니다.'}), 404

    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 삭제

    return jsonify({"삭제 성공"}), 200
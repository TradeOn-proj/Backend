from flask import Blueprint, request, jsonify

bp_post = Blueprint('post', __name__, url_prefix='/api/v1/posts')

@bp_post.route('', methods=['GET'])
def search_post():
    
    keyword = request.args.get('keyword')
    category = request.args.get('category')
    page = request.args.get('page', type = int)
    size = request.args.get('size', type = int)
    sort_by = request.get('sort_by')
    sort_order = request.get('sort_order')

    if not all([keyword, category, page, size, sort_by, sort_order]):
        return jsonify({'400 Bad Request : "status error" : 잘못된 검색 조건입니다.'}), 400
        
    #db조회후 결과 찾기

    return jsonify({
        'postid' : '게시물id',
        'title' : '제목',
        'thumbnail_image_url' : 'example.png',
        'description' : '설명',
        'author' : '작성자정보',
        'keyword' : '게시물 키워드',
        'category' : '게시물 카테고리',
        'viewing' : '게시물 조회수',
        'current_page' : '현재 페이지',
        'page_size' : '페이지 게시물 수',
        'next_page_to' : '다음 페이지'    
    })

@bp_post.route('', methods=['POST'])
def register_post():
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')
    keyword = data.get('keyword')
    desired_items = data.get('desired_items')
    category = data.get('category')
    thumbnail_image_url = data.get('thumbnail_image_url')

    if not all([title, content, keyword, desired_items, category, thumbnail_image_url]):
        return jsonify({'400 Bad Request : "status error" : 필수 입력값이 누락되었거나 형식이 올바르지 않습니다.'}), 400

    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록

    return jsonify({
        'postid' : '게시물ID',
        'message' : '201 Created : "status success" : "게시물이 성공적으로 등록되었습니다!"'
    }), 201


@bp_post.route('/<postid>', methods=['GET'])
def view_post(postid):
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 요청하신 게시물을 찾을 수 없습니다.'}), 404

    return jsonify({
        'postid' : '게시물id',
        'title' : '제목',
        'thumbnail_image_url' : 'example.png',
        'content' : '게시물 전체내용용',
        'author' : '작성자정보',
        'keyword' : '게시물 키워드',
        'category' : '게시물 카테고리',
        'viewing' : '게시물 조회수',
        'status' : '게시물 현재 상태',
        'createAt' : '게시물 생성 일지',
        'updateAt' : '게시물 최종수정일',
    })

@bp_post.route('/<postid>', methods=['PUT'])
def update_post(postid):
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 요청하신 게시물을 찾을 수 없습니다.'}), 404

    data = request.get_json()

    title = data.get('title')
    content = data.get('content')
    keyword = data.get('keyword')
    desired_items = data.get('desired_items')
    category = data.get('category')
    thumbnail_image_url = data.get('thumbnail_image_url')
    status = data.get('status')

    if not all([title, content, keyword, desired_items, category, thumbnail_image_url, status]):
        return jsonify({'400 Bad Request : "status error" : 필수 입력값이 누락되었거나 형식이 올바르지 않습니다.'}), 400
    
    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 등록

    return jsonify({
        'postid' : '수정된 게시물ID',
        'message' : '200 OK : "status success" : "게시물이 성공적으로 수정되었습니다!"'
    }), 200

@bp_post.route('/<postid>', methods=['DELETE'])
def delete_post(postid):
    #db접근해서 게시물 찾기
    #접근 불가할 시
    #return jsonify({'404 Not Found : "status error" : 요청하신 게시물을 찾을 수 없습니다.'}), 404

    #토큰 기능 구현시 권한여부 확인 할것
    #db접근해서 삭제

    return jsonify({
        'message' : '200 OK : "status success" : "게시물이 성공적으로 삭제제되었습니다!"'
    }), 200
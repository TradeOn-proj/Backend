from flask import Blueprint, request, jsonify

bp_valuation = Blueprint('valuation', __name__, url_prefix='/api/v1/valuation-posts')

@bp_valuation.route('', methods =['GET'])
def view_valuation():

    #뭘 파라미터로 받는지 모르겠음
    
    return jsonify({
        'valuation_posts' : [
            {
                'id' : 101,
                'title' : '게시물 제목',
                'item_description_summary' : '물품 설명하기',
                'author' : {
                    'id' : 1,
                    'username' : 'user1'
                },
                'thumbnail_image_url' : 'chair_thumb.jpg',
                'opinion_count' : 15,
                'createdAt' : '2023-11-01T10:00:00Z'
            }
        ],
        'total_count' : 50,
        'current_page': 1,
        'total_pages':5,
        'page_size':10       
    })

@bp_valuation.route('', methods =['POST'])
def post_valuation():
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')
    item_id = data.get('item_id')
    item_description = data.get('item_description')
    image_urls = data.get('image_urls')

    if not all([title, content, item_id, item_description, image_urls]):
        return jsonify({'400 Bad Request : "status error" : 잘못된 요청 데이터 형식식입니다.'}), 400
    
    #토큰, 권한 확인
    #DB 등록
    return jsonify({
        'postid' : '새로 생성된 가치 평가 게시물 ID',
        'message' : '201 Created : "status success" : "가치 평가 게시물이 성공적으로 등록되었습니다!"'
    }), 201


@bp_valuation.route('/<postid>',methods=['GET'])
def view_valuation_detail(postid):

    #DB조회 후 없으면 에러 반환
    #DB조회 후 게시물 정보 가져오기기

    return jsonify({
        'valuation_post' :{
            'id' : 101,
            'title' : '게시물 제목',
            'content' : '게시물 본문',
            'author':{
                'id' : 1,
                'username' : 'user1',
                'profile_image_url' : '...'
            },
            'images' : ['img1.jpg', 'img2.jpg'],
            'createdAt' : '2023-11-01',
            'updatedAt' : '2023-11-01',
            'views' : 120,
            'opinion_count' : 15
        },
        'opinions' : [
            {
                'id' : 1001,
                'post_id' : 101,
                'author':{
                'id' : 5,
                'username' : 'user5'
                },
                'content' : '댓글 내용',
                'createdAt' : '2023-11-01'
            }
            ]
    })

@bp_valuation.route('/<postid>/opinions',methods=['POST'])
def delete_valuation_opinion(postid):
    data = request.get_json()

    content = data.get('content')

    if not all([content]):
        return jsonify({'400 Bad Request : "status error" : 잘못된 입력 형태입니다.'}), 400
    
    #토큰, 권한 확인
    #DB조회 후 게시물 확인
    #DB등록

    return jsonify({
        'opinion_id' : '댓글 고유 ID',
        'message' : '201 Created : "status success" : "의견이 성공적으로 등록되었습니다!"'
    })

@bp_valuation.route('/<postid>/opinions/<opinion_id>',methods=['DELETE'])
def post_valuation_opinion(postid, opinion_id):
    #권한, 토큰 확인
    #DB조회
    #DB데이터 삭제

    return jsonify({
        'message' : '200 OK : "status success" : "댓글이 성공적으로 삭제제되었습니다!"' 
    })
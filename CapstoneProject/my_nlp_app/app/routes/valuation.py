from flask import Blueprint, request, jsonify

bp_valuation = Blueprint('valuation', __name__, url_prefix='/api/v1/valuations')

@bp_valuation.route('', methods =['GET'])
def view_valuation():

    category = request.args.get("category")
    
    return jsonify({
        [
        {
            "postId": "string",
            "title": "string",
            "averagePrice": 0,
            "createdAt": "2025-05-25T13:04:08.370Z"
        }
        ] 
    })

@bp_valuation.route('', methods =['POST'])
def post_valuation():
    data = request.get_json()

    userId = data.get("userId")
    title = data.get("title")
    description = data.get("description")

    if not all([userId, title, description]):
        return jsonify({"필드 누락"}), 400
    
    #토큰, 권한 확인
    #DB 등록
    return jsonify({
        "postId": "string"
    }), 201


@bp_valuation.route('/<postid>',methods=['GET'])
def view_valuation_detail(postid):
    postId = postid

    #DB조회 후 없으면 에러 반환, 404
    #DB조회 후 게시물 정보 가져오기기

    return jsonify({
        "postId": "string",
        "title": "string",
        "description": "string",
        "averagePrice": 0,
        "totalEvaluations": 0,
        "createdAt": "2025-05-25T13:09:23.406Z"
    }), 200

@bp_valuation.route('/<postid>/price', methods = ['POST'])
def valuation_price(postid):
    postId = postid

    #DB 조회하고 없으면 404 오류

    data = request.get_json()

    userId = data.get("userId")
    price = data.get("price")

    return jsonify({"평가 등록 완료"}), 200

@bp_valuation.route('/<postid>/average', methods = ['GET'])
def valuation_average(postid):
    postId = postid

    #DB 조회하고 없으면 404 오류

    return jsonify({
        "postId": "string",
        "validCount": 0,
        "averagePrice": 0
    }), 200
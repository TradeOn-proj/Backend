from flask import Blueprint, request, jsonify

bp_user = Blueprint('user', __name__, url_prefix= '/api/v1/users')

@bp_user.route('/register', methods = ['POST'])
def register():
    data = request.get_json()

    username = data.get("username")
    password =data.get("password")

    if not all([username, password]):
        return jsonify({"잘못된 요청(필드 누락 또는 형식오류)"}), 400
    
    #데이터베이스 중복 확인 조건
    #return jsonify({ '409 Conflict : "status error" : 이미 사용 중인 사용자 이름 또는 이메일입니다.'}), 409
    #DB접근하고 정보 저장
    #나중에 토큰 생성하고 넘겨줄것
    return jsonify({
        "token" : "string"
    }
    ), 200

@bp_user.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not all([username, password]):
        return jsonify({"잘못된 요청(필드 누락 또는 형식오류)"}), 400
    
    #유저 찾기
    #유저 찾기 실패 또는 password 불일치일때
    #return jsonify({'401 Unauthorized : "status error" : 사용자 이름 또는 비밀번호가 올바르지 않습니다.'}), 401

    return jsonify({
        "token" : "string"
    }
    ), 200

@bp_user.route('/logout', methods=['POST'])
def log_out():
    data = request.get_json()

    userId = data.get("userId")

    if not all([userId]):
        return jsonify({"잘못된 요청(필드 누락 또는 형식오류)"}), 400
    
    #유저 찾기
    #유저 못 찾을 시 오류, 찾을 시 삭제

    return jsonify({
        "message" : "User successfully deleted"
    }
    ), 200

@bp_user.route('/<userid>/profile', methods=['GET'])
def user_profile(userid):
    userId = userid
    #토큰,권한 확인
    #DB에서 유저 검색 없으면 404 오류

    return jsonify({
        "nickname": "string",
        "grade": "string",
        "points": 0
    }), 200


@bp_user.route('/<userid>/trades',methods=['GET'])
def user_trade_history(userid):
    userId = userid
    #토큰,권한 확인
    #DB에서 유저 검색 없으면 404 오류

    return jsonify([
        {
        "tradeId": "string",
        "title": "string",
        "status": "string",
        "completedAt": "2025-05-25T12:45:50.787Z"
    }
    ]
    ), 200

@bp_user.route('/<userid>/reviews',methods=['GET'])
def user_review(userid):
    userId = userid
    #토큰,권한 확인
    #DB에서 유저 검색 없으면 404 오류

    return jsonify([
        {
        "reviewId": "string",
        "reviewer": "string",
        "rating": 0,
        "comment": "string",
        "createdAt": "2025-05-25T12:47:23.900Z"
    }
    ]
    ), 200

@bp_user.route('/<userid>/points', methods=['PATCH'])
def user_points(userid):
    userId = userid

    data = request.get_json()

    amount = data.get("amount")

    if not all([amount]):
        return jsonify({"잘못된 요청"}), 400
    
    #DB 접근해서 수정

    return jsonify({"포인트 수정 성공"}), 200

@bp_user.route('/<userid>/delete', methods=['DELETE'])
def user_delete(userid):
    userId = userid

    #DB 조회 후 없으면 404 오류

    #DB 조회 후 삭제
    return jsonify({"탈퇴 성공"}), 200

@bp_user.route('/<userid>/grade',methods=['GET'])
def user_grade(userid):
    userId = userid

    return jsonify({
        "points": 0,
        "grade": "string",
        "gradeIconUrl": "string"
    }
    ), 200
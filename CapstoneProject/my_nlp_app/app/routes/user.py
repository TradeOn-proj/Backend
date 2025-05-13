from flask import Blueprint, request, jsonify

bp_user = Blueprint('user', __name__, url_prefix= '/api/v1/users')

@bp_user.route('/register', methods = ['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password =data.get('password')
    email = data.get('email')

    if not all([username, password, email]):
        return jsonify({'400 Bad Request : "status error" : 잘못된 입력 형태입니다. 이메일 형식을 확인해주세요.'}), 400
    
    #데이터베이스 중복 확인 조건
    #return jsonify({ '409 Conflict : "status error" : 이미 사용 중인 사용자 이름 또는 이메일입니다.'}), 409
    #DB접근하고 정보 저장
    #나중에 토큰 생성하고 넘겨줄것
    return jsonify({'user':{
        'id' : 1,
        'name' : 'user_id',
        'email' : 'user@example.com'
    }
    })

@bp_user.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'400 Bad Request : "status error" : 잘못된 입력 형태입니다. 사용자 이름과 비밀번호를를 확인해주세요.'}), 400
    
    #유저 찾기
    #유저 찾기 실패 또는 password 불일치일때
    #return jsonify({'401 Unauthorized : "status error" : 사용자 이름 또는 비밀번호가 올바르지 않습니다.'}), 401

    return jsonify({'user':{
        'id' : 1,
        'name' : 'existing_user_id',
        'email' : 'user@example.com'
    }
    })

@bp_user.route('/<userid>/recommended-posts', methods=['GET'])
def recommend(userid):
    data = request.get_json()

    keyword = data.get('keyword')
    category = data.get('category')
    limit = data.get('limit')

    if not all([keyword, category, limit]):
        return jsonify({'400 Bad Request : "status error" : 잘못된 검색 조건입니다.'}), 400


    #입력 정보 토대로 추천 리스트 생성

    return jsonify({
        'postid' : '게시물id',
        'title' : '제목',
        'thumbnail_image_url' : 'example.png',
        'description' : '설명',
        'author' : '작성자정보',
        'keyword' : '게시물 키워드',
        'category' : '게시물 카테고리',
        'viewing' : '게시물 조회수',
        'recommendation_score': '추천 점수'
    })

@bp_user.route('/<userid>/profile', methods=['GET'])
def user_profile(userid):
    #토큰,권한 확인
    #DB에서 유저 검색

    return jsonify({
        'user' : {
            'id' : '유저 고유 ID',
            'username' : 'comeon0927',
            'email' : 'user1@example.com',
            'profile_image_url' : 'user1.jpg',
            'registeredAt' : '2022-01-15',
            'current_points' : 1500,
            'current_grade' : '실버',
            'grade_icon_url' : 'silver_grade.png',
            'total_trades' : 30,
            'completed_trades' : 25,
            'cancellation_count' : 3,
            'cancellation_warning' : 'false'
        }
    })


@bp_user.route('/<userid>/trade-history',methods=['GET'])
def user_trade_history(userid):
    return "trade_history", 200

@bp_user.route('/<userid>/reviews',methods=['GET'])
def user_review(userid):
    return "reviews", 200

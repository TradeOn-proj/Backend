from flask import Blueprint, request, jsonify

bp_review = Blueprint('review', __name__, url_prefix='/api/v1/reviews')

@bp_review.route('', methods =['POST'])
def post_review():
    data = request.get_json()

    trade_id = data.get('trade_ID')
    reviewed_user_id = data.get('reviewed_user_id')
    rating = data.get('rating')
    comment = data.get('comment')

    if not all([trade_id, reviewed_user_id, rating, comment]):
        return jsonify({'400 Bad Request : "status error" : 잘못된 요청 데이터 형식입니다.'}), 400
    
    #DB조회 후 관련 오류 반환
    #토큰 확인 구현할 것
    #권한 확인 할 것
    #DB에 데이터 삽입

    return jsonify({
        'review_ID' : '후기 고유 ID',
        'reviewed_user_id' : '후기 작성 대상 사용자의 ID',
        'message' : '200 OK : "Status Success" : "후기가 성공적으로 작성되었습니다."'
    })
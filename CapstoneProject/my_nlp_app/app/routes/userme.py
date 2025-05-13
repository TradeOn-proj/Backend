from flask import Blueprint, request, jsonify

bp_userme = Blueprint('userme', __name__, url_prefix='/api/v1/users/me')

@bp_userme.route('/points-and-grade', methods=['GET'])
def view_pointandgrade():
    #db조회, 권한 확인, 토큰 확인 구현할것

    return jsonify({
        'user_id' : '사용자 id',
        'points' : 0000,
        'grade' : 'gold',
        'grade_icon_url' : 'Gold_grade.png',
        'message' : '200 OK : "Status Success" : "해당유저의 포인트, 등급 현황입니다."'
    }),200

@bp_userme.route('/unregister', methods=['DELETE'])
def unregister():
    #권한, 토큰 확인
    #DB조회
    #DB데이터 삭제

    return jsonify({
        'message' : '200 OK : "status success" : "회원 탈퇴가 성공적으로 완료되었습니다!"' 
    })
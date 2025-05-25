from flask import Blueprint, request, jsonify

bp_analytics = Blueprint('analytics', __name__, url_prefix='/api/v1/analytics')

@bp_analytics.route('/user/<userid>', methods = ['GET'])
def analyze_user(userid):
    userId = userid

    #DB 조회하고 사용자 없으면 400, 거래 내역 없으면 404

    return jsonify({
        "results": [
        {
            "userId": "string",
            "totalTrades": 0,
            "successfulTrades": 0,
            "successRate": 0,
            "averageRating": 0,
            "monthlyTradeCounts": [
            {       
                "month": "2024-12",
                "count": 0
            }
             ],
            "monthlyAverageRatings": [
            {
                "month": "2024-12",
                "averageRating": 0
                }
            ]
        }
        ]
    }), 200

@bp_analytics.route('/user/<userid>', methods = ['PUT'])
def analyze_update(userid):
    userId = userid

    data = request.get_json()

    totalTrades = data.get("totalTrades")
    successfulTrades = data.get("successfulTrades")
    averageRating = data.get("averageRating")

    if not all([totalTrades, successfulTrades, averageRating]):
        return jsonify({"잘못된 요청(필드 누락 또는 형식오류)"}), 400

    #DB 조회하고 사용자 없으면 404

    return jsonify({"거래 데이터 업데이트 성공"}), 200
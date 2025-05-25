from flask import Blueprint, request, jsonify

bp_post = Blueprint('search', __name__, url_prefix='/api/v1/search')

@bp_post.route('', methods=['GET'])
def search_post():
    
    keyword = request.args.get("keyword")
    category = request.args.get("category")
    limit = request.args.get("limit", type = int)
    offset = request.args.get("offset", type = int)

    if not all([keyword]):
        return jsonify({"error": "Keyword is required and must be a string."}), 400
    
    #db조회후 결과 찾기

    return jsonify({
        "results": [
        {
            "postId": "string",
            "title": "string",
            "description": "string",
            "category": "string",
             "createdAt": "2025-05-25T13:02:24.944Z"
        }
        ]
    }), 200
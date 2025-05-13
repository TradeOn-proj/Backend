from flask import Blueprint, request, jsonify

test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return 'message : TEST GET 요청입니다'

    elif request.method == 'POST':

        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field'}), 400
    
        text = data['text']

        return jsonify({
        'prediction': "OK",
        'confidence': 1
        })
# app/swagger.py

import os
from flask import Blueprint, send_from_directory

swagger_bp = Blueprint(
    'swagger_bp',
    __name__,
    url_prefix='/docs'  # 클라이언트에서 '/docs' 로 접속했을 때 Swagger UI 로 연결
)

# swagger/dist 디렉터리 경로 (위 init 파일과 동일하게 설정)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SWAGGER_DIR = os.path.join(BASE_DIR, "..", "swagger", "dist")

@swagger_bp.route('/<path:filename>')
def serve_swagger_files(filename):
    """
    /docs/<filename> 요청 시 swagger/dist/<filename> 파일을 반환
    예: GET /docs/index.html → swagger/dist/index.html
    """
    return send_from_directory(SWAGGER_DIR, filename)

@swagger_bp.route('', defaults={'filename': 'index.html'})
@swagger_bp.route('/')
def serve_swagger_index(filename):
    """
    /docs 또는 /docs/ 요청 시, swagger/dist/index.html 반환
    """
    return send_from_directory(SWAGGER_DIR, filename)
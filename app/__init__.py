# app/__init__.py

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy import text
from flask_socketio import SocketIO
from datetime import timedelta

load_dotenv()

# ── 확장 객체 정의 ───────────────────────────────────────────────
socket_io = SocketIO(async_mode='threading', cors_allowed_origins="*")
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

# ── 앱 생성 함수 ─────────────────────────────────────────────────
def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Swagger UI 정적 파일이 위치한 디렉터리
    SWAGGER_DIR = os.path.join(BASE_DIR, "..", "swagger", "dist")
    # openapi.yaml 파일이 루트(또는 상위) 디렉터리에 있다면 그 경로
    OPENAPI_DIR = os.path.join(BASE_DIR, "..")

    # 1) Flask 기본 static_folder 사용 (기본값이 'static' 이므로 따로 지정 불필요)
    #    → app/static/<파일들> 이 /static/<파일들> URL로 자동 서빙됨
    app = Flask(__name__)

    # 2) 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=4)

    # 3) 확장 기능 초기화
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    socket_io.init_app(app)
    # CORS: 모든 "/api/*" 경로에 대해, 어떤 Origin이든(*) 허용, 쿠키/토큰 포함 허용
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # 4) Socket.IO 핸들러 등록 (기존 코드 유지)
    from app.socket_handlers import register_socketio_handlers
    register_socketio_handlers(socket_io)

    # 5) 블루프린트 등록 (기존 라우트들)
    from app.routes.user import user_bp
    from app.routes.post import bp_post
    from app.routes.trade import bp_trade
    from app.routes.search import search_bp
    from app.routes.valuation import bp_valuation
    from app.routes.test import test_bp
    from app.routes.analytics import bp_analytics
    from app.routes.chat import bp_chat

    app.register_blueprint(user_bp)
    app.register_blueprint(bp_post)
    app.register_blueprint(bp_trade)
    app.register_blueprint(bp_valuation)
    app.register_blueprint(test_bp)
    app.register_blueprint(bp_analytics)
    app.register_blueprint(bp_chat)
    app.register_blueprint(search_bp)

    # ── Swagger UI 서빙용 Blueprint 등록 (추가) ──────────────────────
    #    아래 swagger_bp는 별도 파일(app/swagger.py)에 정의되어야 합니다.
    from app.swagger import swagger_bp
    app.register_blueprint(swagger_bp)

    # 6) openapi.yaml 파일을 루트에서 직접 노출 (기존 코드 유지)
    @app.route('/openapi.yaml')
    def openapi_spec():
        return send_from_directory(OPENAPI_DIR, 'openapi.yaml')

    # 7) DB 연결 확인용 핑 (기존 코드 유지)
    @app.route("/ping")
    def ping():
        try:
            db.session.execute(text("SELECT 1"))
            return "✅ RDS 연결 성공", 200
        except Exception as e:
            return f"❌ RDS 연결 실패: {str(e)}", 500

    return app

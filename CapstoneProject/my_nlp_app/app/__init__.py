from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

from sqlalchemy import text

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app)

    # 블루프린트 등록 (상대 경로 import 사용)
    from app.routes.user import user_bp
    from app.routes.post import post_bp
    from app.routes.trade import trade_bp
    from app.routes.review import review_bp
    from app.routes.userme import userme_bp
    from app.routes.valuation import valuation_bp
    from app.routes.test import test_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(userme_bp)
    app.register_blueprint(valuation_bp)
    app.register_blueprint(test_bp)

    @app.route("/ping")
    def ping():
        try:
            db.session.execute(text("SELECT 1"))
            return "✅ RDS 연결 성공", 200
        except Exception as e:
            return f"❌ RDS 연결 실패: {str(e)}", 500

    return app

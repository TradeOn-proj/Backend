from flask import Flask
from flask_socketio import SocketIO

socket_io  = SocketIO(cors_allowed_origins= "*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    from app.routes.test import test_bp
    from app.routes.user import bp_user
    from app.routes.post import bp_post
    from app.routes.review import bp_review
    from app.routes.trade import bp_trade
    from app.routes.valuation import bp_valuation
    from app.routes.userme import bp_userme
    from app.routes.chat import bp_chat

    app.register_blueprint(test_bp)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_post)
    app.register_blueprint(bp_review)
    app.register_blueprint(bp_trade)
    app.register_blueprint(bp_valuation)
    app.register_blueprint(bp_userme)
    app.register_blueprint(bp_chat)
    
    socket_io.init_app(app)

    return app
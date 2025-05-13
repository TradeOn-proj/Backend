from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.test import test_bp
    from app.routes.user import bp_user
    from app.routes.post import bp_post
    from app.routes.review import bp_review
    from app.routes.trade import bp_trade
    from app.routes.valuation import bp_valuation
    from app.routes.userme import bp_userme

    app.register_blueprint(test_bp)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_post)
    app.register_blueprint(bp_review)
    app.register_blueprint(bp_trade)
    app.register_blueprint(bp_valuation)
    app.register_blueprint(bp_userme)
    

    return app
# models/user.py — User 모델 정의

from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    profile_image_url = db.Column(db.String(255), nullable=True)
    points = db.Column(db.Integer, default=0)
    grade = db.Column(db.String(20), default='브론즈')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 관계 설정 (역참조용)
    posts = db.relationship('Post', backref='author', lazy=True)
    trades = db.relationship('Trade', backref='requester', lazy=True, foreign_keys='Trade.requester_id')
    reviews_written = db.relationship('Review', backref='reviewer', lazy=True, foreign_keys='Review.reviewer_id')
    reviews_received = db.relationship('Review', backref='target_user', lazy=True, foreign_keys='Review.user_id')
    valuation_posts = db.relationship('ValuationPost', backref='author', lazy=True)
    valuation_opinions = db.relationship('ValuationOpinion', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

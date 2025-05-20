from app import db
from datetime import datetime
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    keyword = db.Column(db.String(50), nullable=True)
    thumbnail_image_url = db.Column(db.String(255), nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trades = db.relationship('Trade', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post {self.title}>'
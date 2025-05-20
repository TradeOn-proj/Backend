from app import db
from datetime import datetime

class ValuationPost(db.Model):
    __tablename__ = 'valuation_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    item_id = db.Column(db.String(100), nullable=False)
    item_description = db.Column(db.Text, nullable=False)
    thumbnail_image_url = db.Column(db.String(255), nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    opinions = db.relationship('ValuationOpinion', backref='valuation_post', lazy=True)

    def __repr__(self):
        return f'<ValuationPost {self.title}>'

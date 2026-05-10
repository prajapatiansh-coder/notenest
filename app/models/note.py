from datetime import datetime
from ..extensions import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False, index=True)
    semester = db.Column(db.String(20), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(100), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    downloads = db.Column(db.Integer, default=0, index=True)
    ai_summary = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    # Relationships
    likes = db.relationship('Like', backref='note', lazy=True, cascade="all, delete-orphan")
    bookmarks = db.relationship('Bookmark', backref='note', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='note', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Note {self.title}>'

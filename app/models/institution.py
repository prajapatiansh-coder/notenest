from datetime import datetime
from ..extensions import db

class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100), unique=True, nullable=True)  # e.g., 'university.edu'
    branding_color = db.Column(db.String(20), default='#667eea')
    logo = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('InstitutionMember', backref='institution', lazy=True)
    notes = db.relationship('Note', backref='institution', lazy=True)

class InstitutionMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
    role = db.Column(db.String(20), default='student')  # 'student', 'moderator', 'admin'
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class InstitutionSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
    ai_enabled = db.Column(db.Boolean, default=True)
    max_upload_size = db.Column(db.Integer, default=16)  # in MB
    allow_external_sharing = db.Column(db.Boolean, default=True)

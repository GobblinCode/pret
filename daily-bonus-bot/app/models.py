from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GamblingSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    login_url = db.Column(db.String(500))
    username_selector = db.Column(db.String(200))
    password_selector = db.Column(db.String(200))
    login_button_selector = db.Column(db.String(200))
    bonus_claim_selector = db.Column(db.String(200))
    username = db.Column(db.String(100))
    password_encrypted = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    additional_steps = db.Column(db.Text)  # JSON string for complex navigation
    cookies = db.Column(db.Text)  # JSON string for session cookies
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    claims = db.relationship('ClaimLog', backref='site', lazy=True, cascade='all, delete-orphan')

class ClaimLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('gambling_site.id'), nullable=False)
    status = db.Column(db.String(20))  # success, failed, pending
    message = db.Column(db.Text)
    screenshot_path = db.Column(db.String(500))
    claimed_at = db.Column(db.DateTime, default=datetime.utcnow)
    bonus_amount = db.Column(db.String(50))  # Store as string to handle various formats
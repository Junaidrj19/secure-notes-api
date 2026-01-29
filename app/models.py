from .config import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String(60),unique= True,nullable = False)
    password = db.Column(db.String(100),nullable = False)
    notes = db.relationship(
        "Note",
        back_populates="users",
        cascade="all,delete-orphan"
        )

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable = False)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    users = db.relationship("User",back_populates="notes")
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable = False)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
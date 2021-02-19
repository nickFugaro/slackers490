# models.py
import flask_sqlalchemy
from app import db


class MessageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String(300))
    users = db.Column(db.String(50))
    tokenid = db.Column(db.String)
    email = db.Column(db.String(120))
    image = db.Column(db.String)
    
    def __init__(self, messages, users, tokenid, email, image):
        self.messages = messages
        self.users = users
        self.tokenid = tokenid
        self.email = email
        self.image = image
        
    def __repr__(self):
        return '<Messages: %s>' % self.messages 


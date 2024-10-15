from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_login import UserMixin
from datetime import datetime
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    admin = db.relationship('Admin', backref = 'user', uselist = False)
    sponsor = db.relationship('Sponsor', backref = 'user', uselist = False)
    influencer = db.relationship('Influencer', backref = 'user', uselist = False)
    is_on_hold = db.Column(db.Boolean, default=False)

    def is_profile_complete(self):
        if self.role == 'sponsor':
            return self.sponsor is not None and all([self.sponsor.company_name, self.sponsor.industry, self.sponsor.budget])
        elif self.role == 'influencer':
            return self.influencer is not None and all([self.influencer.name, self.influencer.category, self.influencer.niche, self.influencer.reach])
        return False

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150))
    company_name = db.Column(db.String(150))
    industry = db.Column(db.String(150))
    budget = db.Column(db.Float)
    campaigns = db.relationship('Campaign', backref = 'sponsor', lazy = True)

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150))
    category = db.Column(db.String(150))
    niche = db.Column(db.String(150))
    reach = db.Column(db.Integer)
    ad_requests = db.relationship('AdRequest', backref = 'influencer')
    instagram_handle = db.Column(db.String(150), nullable=True)
    profile_picture = db.Column(db.String(300), nullable=True)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    visibility = db.Column(db.String(50))
    goals = db.Column(db.Text)
    ad_requests = db.relationship('AdRequest', backref = 'campaign')
    is_on_hold = db.Column(db.Boolean, default=False)

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    status = db.Column(db.String(50))
    is_on_hold = db.Column(db.Boolean, default=False)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_message_at = db.Column(db.DateTime, index=True)

    user1 = db.relationship('User', foreign_keys=[user1_id], backref='conversations_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='conversations_as_user2')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    conversation = db.relationship('Conversation', backref='messages')
    sender = db.relationship('User', backref='sent_messages')

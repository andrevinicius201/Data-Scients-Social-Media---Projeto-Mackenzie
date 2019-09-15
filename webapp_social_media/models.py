from datetime import datetime
from flask import current_app
from webapp_social_media import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    data_nasc = db.Column(db.String(120), nullable=False)
    start_work_date = db.Column(db.String(120), nullable=False)
    work_state = db.Column(db.String(120), nullable=False)
    work_city = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.Float(120), nullable=False)
    instruction = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    card_number = db.Column(db.Float(120), nullable=True)
    card_name = db.Column(db.String(120), nullable=True)
    expiration_date = db.Column(db.String(120), nullable=True)
    cvv = db.Column(db.String(120), nullable=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(120), nullable=False)
    interests = db.relationship(
        'InterestTopicUser', backref='interested', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.image_file}', '{self.user_type}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class InterestTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    users_topics_id = db.relationship('InterestTopicUser',
                               backref='topic', lazy=True)

    def __repr__(self):
        return f"InterestTopic('{self.label}')"


class InterestTopicUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.String(100), db.ForeignKey(
        'interest_topic.label'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"InterestTopicUser('{self.topic_id}', '{self.user_id}')"

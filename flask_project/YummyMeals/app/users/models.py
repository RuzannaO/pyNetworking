from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import validates

from .. import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    comment = db.relationship('UserComments', backref='author', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    def check_admin_rights(self):
        if self.is_admin:
            return True
        return False

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}','{self.username}'," \
               f"'{self.email}','{self.image_file}')"


class UserFavorite(db.Model):
    __tablename__ = 'user__favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    meal = db.relationship('Meal', backref="userfavorite")
    user = db.relationship('User')

    def __repr__(self):
        return f"UserFavorite('{self.user_id}','{self.meal_id}')"


class UserComments(db.Model):
    __tablename__ = 'user_comments'

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey(
        'meal.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal = db.relationship('Meal', backref="usercomments")
    user = db.relationship('User')

    def __repr__(self):
        return f"UserComments('{self.id}','{self.content}'," \
               f"'{self.meal_id}','{self.user_id}')"


class SupportMessage(db.Model):
    __tablename__ = 'support__message'

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')


    def __repr__(self):
        return f"Support Message-'{self.id}','{self.user.id}','{self.content}'"


class UserFavoriteCategory(db.Model):
    __tablename__ = 'user__favorite__category'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
    user = db.relationship('User')

    def __repr__(self):
        return f"User_Favorite_Category('{self.user_id}','{self.category_id}')"


class Friendship(db.Model):
    __tablename__ = 'friendship'

    id = db.Column(db.Text, primary_key=True)
    requesting_user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)
    receiving_user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)
    status = db.Column(
        db.Boolean,
        default=False)
    request_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now)
    approve_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now)
    sender = db.relationship(
        User,
        foreign_keys=[requesting_user_id],
        backref='sent')
    receiver = db.relationship(
        User,
        foreign_keys=[receiving_user_id],
        backref='received')



class UserActivities(db.Model):
    __tablename__ = 'user_activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    comments = db.Column(db.Integer, nullable=False, default=0)
    favorite_meals = db.Column(db.Integer, nullable=False, default=0)
    favorite_categories = db.Column(db.Integer, nullable=False, default=0)
    meal_author = db.Column(db.Integer, nullable=False, default=0)
    friendship = db.Column(db.Integer, nullable=False, default=0)
    support_message = db.Column(db.Integer, nullable=False, default=0)
    profile_pict = db.Column(db.Integer, nullable=False, default=0)
    login = db.Column(db.Integer, nullable=False, default=0)
    pwd_reset = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship('User')
    
    @validates('comments','favorite_meals','')
    def update_state(self , key, value):
        self.total = 0
        for_comments = self.commants * 10
        for_favorite_meals = self.favorite_meals * 20
        self.total += for_comments + for_favorite_meals
        return 1

class UserMessages(db.Model):
    __tablename__ = 'user_messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)
    reciver_user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)
    sender = db.relationship(
        User,
        foreign_keys=[sender_user_id],
        backref='message_sender')
    receiver = db.relationship(
        User,
        foreign_keys=[reciver_user_id],
        backref='message_reciever')
    send_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)

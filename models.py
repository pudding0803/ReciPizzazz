import pytz
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(110), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Taipei')))

    recipes = relationship("Recipe", backref="user")


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    token = db.Column(db.String(30), unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Taipei')))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Taipei')))


class Followership(db.Model):
    __tablename__ = 'followerships'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint('follower_id', 'followed_id'),
    )


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    liking = db.Column(db.Boolean, nullable=False, default=True)
    following = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Taipei')))

    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id'),
    )


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    marking = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Taipei')))

    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id'),
    )

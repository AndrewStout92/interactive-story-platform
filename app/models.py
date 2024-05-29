from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# User model for handling user data and authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for User model
    username = db.Column(db.String(150), unique=True, nullable=False)  # Username field, must be unique and non-nullable
    password_hash = db.Column(db.String(150), nullable=False)  # Password hash field, non-nullable

    # Method to set password, hashes the password before storing it
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check password, verifies the password against the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Story model for handling story data
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for Story model
    title = db.Column(db.String(200), nullable=False)  # Title field, non-nullable
    chapters = db.relationship('Chapter', backref='story', lazy=True)  # Relationship to Chapter model


# Chapter model for handling chapter data within a story
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for Chapter model
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)  # Foreign key to Story model, non-nullable
    content = db.Column(db.Text, nullable=False)  # Content field, non-nullable
    # Relationship to Choice model, specifying the foreign key to avoid ambiguity
    choices = db.relationship('Choice', backref='chapter', lazy=True, foreign_keys='Choice.chapter_id')


# Choice model for handling choices within a chapter
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for Choice model
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)  # Foreign key to Chapter model, non-nullable
    choice_text = db.Column(db.String(200), nullable=False)  # Text of the choice, non-nullable
    next_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))  # Foreign key to the next Chapter model
    # Explicit relationship to the Chapter model for next chapter reference
    next_chapter = db.relationship('Chapter', foreign_keys=[next_chapter_id])



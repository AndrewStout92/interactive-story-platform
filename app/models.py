from . import db


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    chapters = db.relationship('Chapter', backref='story', lazy=True)


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    choices = db.relationship('Choice', backref='chapter', lazy=True, foreign_keys='Choice.chapter_id')


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    choice_text = db.Column(db.String(200), nullable=False)
    next_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    next_chapter = db.relationship('Chapter', foreign_keys=[next_chapter_id])


from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from .models import db, Story, Chapter, Choice, User
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Received registration data: {data}")
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"msg": "Username already exists"}), 400
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User registered successfully"}), 200
    return render_template('register.html')


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Received login data: {data}")
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/')
def home():
    return "Welcome to the Interactive Storytelling Platform!"


@main.route('/create_story', methods=['GET', 'POST'])
@login_required
def create_story():
    if request.method == 'POST':
        title = request.form['title']
        new_story = Story(title=title)
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('main.list_stories'))
    return render_template('create_story.html')


@main.route('/story/<int:story_id>/create_chapter', methods=['GET', 'POST'])
@login_required
def create_chapter(story_id):
    if request.method == 'POST':
        content = request.form['content']
        new_chapter = Chapter(story_id=story_id, content=content)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for('main.list_chapters', story_id=story_id))
    return render_template('create_chapter.html', story_id=story_id)


@main.route('/stories/json', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    return jsonify([{'id': story.id, 'title': story.title} for story in stories])


@main.route('/story/<int:story_id>/chapters/json', methods=['GET'])
def get_chapters(story_id):
    chapters = Chapter.query.filter_by(story_id=story_id).all()
    return jsonify([{'id': chapter.id, 'content': chapter.content} for chapter in chapters])


@main.route('/choice', methods=['POST'])
def create_choice():
    data = request.get_json()
    print(f"Received data: {data}")
    if 'chapter_id' not in data or 'choice_text' not in data or 'next_chapter_id' not in data:
        return jsonify({'error': 'Chapter ID, choice text, and next chapter ID are required'}), 400
    new_choice = Choice(
        chapter_id=data['chapter_id'],
        choice_text=data['choice_text'],
        next_chapter_id=data['next_chapter_id']
    )
    db.session.add(new_choice)
    db.session.commit()
    return jsonify({'id': new_choice.id, 'choice_text': new_choice.choice_text})


@main.route('/stories', methods=['GET'])
def list_stories():
    stories = Story.query.all()
    return render_template('list_stories.html', stories=stories)


@main.route('/story/<int:story_id>/chapters', methods=['GET'])
def list_chapters(story_id):
    chapters = Chapter.query.filter_by(story_id=story_id).all()
    return render_template('list_chapters.html', chapters=chapters, story_id=story_id)












from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from .models import db, Story, Chapter, Choice, User
import logging
from flask_login import login_user, logout_user, login_required, current_user

# Logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Create a blueprint for organizing routes
main = Blueprint('main', __name__)

# Route for handling user login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.list_stories'))
        flash('Invalid username or password')
    return render_template('login.html')

# Route for handling user logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Route for the home page
@main.route('/')
def home():
    return "Welcome to the Interactive Storytelling Platform!"


# Route for creating a new story
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

# Route for creating a new chapter in a story
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

# Route to get all stories in JSON format
@main.route('/stories/json', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    return jsonify([{'id': story.id, 'title': story.title} for story in stories])


# Route to get all chapters of a specific story in JSON format
@main.route('/story/<int:story_id>/chapters/json', methods=['GET'])
def get_chapters(story_id):
    chapters = Chapter.query.filter_by(story_id=story_id).all()
    return jsonify([{'id': chapter.id, 'content': chapter.content} for chapter in chapters])

# Route to create a new choice for a chapter
@main.route('/choice', methods=['POST'])
def create_choice():
    data = request.get_json()
    logging.debug(f'Received data: {data}')
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

# Route to list all stories
@main.route('/stories', methods=['GET'])
def list_stories():
    stories = Story.query.all()
    return render_template('list_stories.html', stories=stories)


# Route to list all chapters of a specific story
@main.route('/story/<int:story_id>/chapters', methods=['GET'])
def list_chapters(story_id):
    chapters = Chapter.query.filter_by(story_id=story_id).all()
    return render_template('list_chapters.html', chapters=chapters, story_id=story_id)











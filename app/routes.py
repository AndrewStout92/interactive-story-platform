from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from .models import db, Story, Chapter, Choice, User  # Ensure User model is imported
import logging
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Set up logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Create a blueprint for organizing routes
main = Blueprint('main', __name__)

# Initialize Flask-Login for user session management
login_manager = LoginManager()
login_manager.login_view = 'main.login'


# Define the user loader function required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Route for handling login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from form
        username = request.form['username']
        password = request.form['password']
        # Query the user by username
        user = User.query.filter_by(username=username).first()
        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)  # Log the user in
            return redirect(url_for('main.list_stories'))  # Redirect to stories list
        flash('Invalid username or password')  # Flash error message
    return render_template('login.html')  # Render the login template


# Route for handling logout
@main.route('/logout')
@login_required  # Ensure user is logged in to access this route
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('main.login'))  # Redirect to login page


# Home route for basic welcome message
@main.route('/')
def home():
    return "Welcome to the Interactive Storytelling Platform!"


# Route for creating a new story
@main.route('/story', methods=['POST'])
def create_story():
    data = request.get_json()  # Get JSON data from request
    logging.debug(f'Received data: {data}')  # Log the received data
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400  # Return error if title is missing
    new_story = Story(title=data['title'])  # Create a new story instance
    db.session.add(new_story)  # Add the story to the session
    db.session.commit()  # Commit the session to save the story
    return jsonify({'id': new_story.id, 'title': new_story.title})  # Return the new story's details


# Route for creating a new chapter
@main.route('/chapter', methods=['POST'])
def create_chapter():
    data = request.get_json()  # Get JSON data from request
    logging.debug(f'Received data: {data}')  # Log the received data
    if 'story_id' not in data or 'content' not in data:
        return jsonify({'error': 'Story ID and content are required'}), 400  # Return error if story_id or content is missing
    new_chapter = Chapter(story_id=data['story_id'], content=data['content'])  # Create a new chapter instance
    db.session.add(new_chapter)  # Add the chapter to the session
    db.session.commit()  # Commit the session to save the chapter
    return jsonify({'id': new_chapter.id, 'content': new_chapter.content})  # Return the new chapter's details


# Route for fetching all stories as JSON
@main.route('/stories/json', methods=['GET'])
def get_stories():
    stories = Story.query.all()  # Query all stories
    return jsonify([{'id': story.id, 'title': story.title} for story in stories])  # Return stories as JSON


# Route for fetching chapters of a specific story as JSON
@main.route('/story/<int:story_id>/chapters/json', methods=['GET'])
def get_chapters(story_id):
    chapters = Chapter.query.filter_by(story_id=story_id).all()  # Query chapters by story_id
    return jsonify([{'id': chapter.id, 'content': chapter.content} for chapter in chapters])  # Return chapters as JSON


# Route for creating a new choice for a chapter
@main.route('/choice', methods=['POST'])
def create_choice():
    data = request.get_json()  # Get JSON data from request
    logging.debug(f'Received data: {data}')  # Log the received data
    if 'chapter_id' not in data or 'choice_text' not in data or 'next_chapter_id' not in data:
        return jsonify({'error': 'Chapter ID, choice text, and next chapter ID are required'}), 400  # Return error if any field is missing
    new_choice = Choice(
        chapter_id=data['chapter_id'],
        choice_text=data['choice_text'],
        next_chapter_id=data['next_chapter_id']
    )  # Create a new choice instance
    db.session.add(new_choice)  # Add the choice to the session
    db.session.commit()  # Commit the session to save the choice
    return jsonify({'id': new_choice.id, 'choice_text': new_choice.choice_text})  # Return the new choice's details


# Route for listing stories and rendering the stories template
@main.route('/stories', methods=['GET'])
def list_stories():
    stories = Story.query.all()  # Query all stories
    return render_template('stories.html', stories=stories)  # Render the stories template with stories data


# Route for listing chapters of a specific story and rendering the chapters template
@main.route('/story/<int:story_id>/chapters', methods=['GET'])
def list_chapters(story_id):
    chapters = Chapter.query.filter_by(story_id=story_id).all()  # Query chapters by story_id
    return render_template('chapters.html', chapters=chapters)  # Render the chapters template with chapters data


# Route to render the form for creating a new story
@main.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if request.method == 'POST':
        title = request.form['title']
        new_story = Story(title=title)
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('main.list_stories'))
    return render_template('create_story.html')


# Route to render the form for creating a new chapter
@main.route('/story/<int:story_id>/create_chapter', methods=['GET', 'POST'])
def create_chapter(story_id):
    if request.method == 'POST':
        content = request.form['content']
        new_chapter = Chapter(story_id=story_id, content=content)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for('main.list_chapters', story_id=story_id))
    return render_template('create_chapter.html', story_id=story_id)








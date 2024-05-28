from flask import Blueprint, request, jsonify
from .models import db, Story, Chapter, Choice
import logging

logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return "Welcome to the Interactive Storytelling Platform!"


@main.route('/story', methods=['POST'])
def create_story():
    data = request.get_json()
    logging.debug(f'Received data: {data}')
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    new_story = Story(title=data['title'])
    db.session.add(new_story)
    db.session.commit()
    return jsonify({'id': new_story.id, 'title': new_story.title})


@main.route('/chapter', methods=['POST'])
def create_chapter():
    data = request.get_json()
    logging.debug(f'Received data: {data}')
    if 'story_id' not in data or 'content' not in data:
        return jsonify({'error': 'Story ID and content are required'}), 400
    new_chapter = Chapter(story_id=data['story_id'], content=data['content'])
    db.session.add(new_chapter)
    db.session.commit()
    return jsonify({'id': new_chapter.id, 'content': new_chapter.content})



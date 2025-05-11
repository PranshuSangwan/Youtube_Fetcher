# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['YOUTUBE_API_KEYS'] = os.environ.get('YOUTUBE_API_KEYS', '').split(',')
app.config['YOUTUBE_SEARCH_QUERY'] = os.environ.get('YOUTUBE_SEARCH_QUERY', 'cricket')
app.config['YOUTUBE_FETCH_INTERVAL'] = int(os.environ.get('YOUTUBE_FETCH_INTERVAL', 10))

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models
from app.models import Video

# Register routes
from app.api.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# Initialize background task
from app.tasks.fetcher import VideoFetcher

@app.before_request
def start_background_task():
    fetcher = VideoFetcher(
        api_keys=app.config['YOUTUBE_API_KEYS'],
        search_query=app.config['YOUTUBE_SEARCH_QUERY'],
        interval=app.config['YOUTUBE_FETCH_INTERVAL']
    )
    fetcher.start()
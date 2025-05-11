# app/services/youtube.py
import os
import requests
from datetime import datetime, timedelta
from app.models import Video
from app import db

class YouTubeService:
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"
    
    def __init__(self, api_keys=None, search_query="cricket"):
        self.api_keys = api_keys or []
        self.current_key_index = 0
        self.search_query = search_query
    
    def get_current_api_key(self):
        if not self.api_keys:
            raise ValueError("No API keys available")
        return self.api_keys[self.current_key_index]
    
    def rotate_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return self.get_current_api_key()
    
    # Make sure this method exists and is spelled exactly like this
    def fetch_latest_videos(self, published_after=None):
        """Fetch latest videos from YouTube API"""
        from app import app  # Import here to avoid circular imports
        
        if published_after is None:
            # Default to 5 minutes ago if no specific time provided
            published_after = datetime.utcnow() - timedelta(minutes=5)
            
        params = {
            'part': 'snippet',
            'q': self.search_query,
            'type': 'video',
            'order': 'date',
            'maxResults': 50,  # Maximum allowed by YouTube
            'publishedAfter': published_after.isoformat("T") + "Z",
            'key': self.get_current_api_key()
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            with app.app_context():  # Add application context here
                return self._process_response(response.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403 and "quotaExceeded" in e.response.text:
                # Quota exceeded, try with another key
                if len(self.api_keys) > 1:
                    self.rotate_api_key()
                    return self.fetch_latest_videos(published_after)
                else:
                    raise Exception("All API keys have exhausted their quota")
            raise
    
    def _process_response(self, data):
        """Process YouTube API response and store videos in the database"""
        saved_videos = []
        
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']
            
            # Check if video already exists
            existing_video = Video.query.get(video_id)
            if existing_video:
                continue
                
            # Create new video
            video = Video(
                id=video_id,
                title=snippet['title'],
                description=snippet.get('description', ''),
                published_at=datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')),
                thumbnail_default=snippet['thumbnails'].get('default', {}).get('url'),
                thumbnail_medium=snippet['thumbnails'].get('medium', {}).get('url'),
                thumbnail_high=snippet['thumbnails'].get('high', {}).get('url'),
                channel_id=snippet.get('channelId'),
                channel_title=snippet.get('channelTitle')
            )
            
            db.session.add(video)
            saved_videos.append(video)
        
        db.session.commit()
        return saved_videos
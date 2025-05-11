# app/tasks/fetcher.py
import threading
import time
from datetime import datetime, timedelta
from app.services.youtube import YouTubeService
from app import app, db
from app.models import Video

class VideoFetcher:
    def __init__(self, api_keys, search_query, interval=10):
        self.youtube_service = YouTubeService(api_keys, search_query)
        self.interval = interval
        self.is_running = False
        self.thread = None
        
    def start(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._fetch_loop)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=self.interval+1)
            
    def _fetch_loop(self):
        while self.is_running:
            try:
                # Create an application context for this thread
                with app.app_context():
                    # Find the latest video timestamp or default to 1 day ago
                    latest_video = Video.query.order_by(Video.published_at.desc()).first()
                    if latest_video:
                        published_after = latest_video.published_at
                    else:
                        published_after = datetime.utcnow() - timedelta(days=1)
                    
                    app.logger.info(f"Fetching videos published after {published_after}")
                    videos = self.youtube_service.fetch_latest_videos(published_after)
                    app.logger.info(f"Fetched {len(videos)} new videos")
            except Exception as e:
                app.logger.error(f"Error fetching videos: {str(e)}")
                
            time.sleep(self.interval)
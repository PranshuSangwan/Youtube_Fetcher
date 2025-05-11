from datetime import datetime
from app import db

class Video(db.Model):
    id = db.Column(db.String(50), primary_key=True)  
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    published_at = db.Column(db.DateTime, nullable=False, index=True)  # Indexed for sorting
    thumbnail_default = db.Column(db.String(255), nullable=True)
    thumbnail_medium = db.Column(db.String(255), nullable=True)
    thumbnail_high = db.Column(db.String(255), nullable=True)
    channel_id = db.Column(db.String(100), nullable=True)
    channel_title = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'published_at': self.published_at.isoformat(),
            'thumbnails': {
                'default': self.thumbnail_default,
                'medium': self.thumbnail_medium,
                'high': self.thumbnail_high
            },
            'channel_id': self.channel_id,
            'channel_title': self.channel_title
        }
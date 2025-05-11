# app/api/routes.py
from flask import Blueprint, jsonify, request
from app.models import Video
from app import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/videos', methods=['GET'])
def get_videos():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limit per_page to a reasonable value
    per_page = min(per_page, 100)
    
    # Query with pagination, sorted by published_at in descending order
    videos = Video.query.order_by(Video.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Format response
    response = {
        'videos': [video.to_dict() for video in videos.items],
        'pagination': {
            'total': videos.total,
            'pages': videos.pages,
            'current_page': videos.page,
            'per_page': videos.per_page,
            'has_next': videos.has_next,
            'has_prev': videos.has_prev
        }
    }
    
    return jsonify(response)
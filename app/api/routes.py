# app/api/routes.py
from flask import Blueprint, jsonify, request
from app.models import Video
from app import db
from sqlalchemy import desc, asc

api_bp = Blueprint('api', __name__)

@api_bp.route('/videos', methods=['GET'])
def get_videos():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limit per_page to a reasonable value
    per_page = min(per_page, 100)
    
    # Sorting parameters
    sort_field = request.args.get('sort', 'published_at')
    sort_order = request.args.get('order', 'desc')
    
    # Search parameter
    search_query = request.args.get('search', '')
    
    # Build query
    query = Video.query
    
    # Apply search filter if provided
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            (Video.title.ilike(search_term)) | 
            (Video.description.ilike(search_term)) |
            (Video.channel_title.ilike(search_term))
        )
    
    # Apply sorting
    if sort_field in ['title', 'published_at', 'channel_title']:
        sort_column = getattr(Video, sort_field)
        if sort_order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
    else:
        # Default to published_at desc
        query = query.order_by(desc(Video.published_at))
    
    # Execute query with pagination
    videos = query.paginate(
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
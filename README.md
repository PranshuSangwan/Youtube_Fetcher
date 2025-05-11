# YouTube Video Fetcher API

A Flask-based API that continuously fetches the latest videos from YouTube for a given search query and provides them through a paginated API.

## Features

- Continuously fetches latest videos from YouTube API
- Stores video data in a database
- Provides paginated API to retrieve videos sorted by publishing date
- Supports multiple YouTube API keys with automatic rotation
- Optimized database queries with proper indexing

## Requirements

- Python 3.7+
- Flask
- SQLAlchemy
- Requests

## Installation

1. Clone the repository:

git clone <repository-url>
cd youtube-api-fetcher
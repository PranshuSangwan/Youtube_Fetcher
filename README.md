# 📺 YouTube Video Fetcher API

A Flask-based backend service that continuously fetches the latest videos from YouTube based on a given search query and provides them through a clean, paginated REST API.

---

## 🚀 Features

- 🧠 Automatically fetches latest videos using the YouTube Data API v3  
- 🧵 Background fetching using a threaded service  
- 🔁 Supports multiple API keys (rotates when quota is exhausted)  
- 🧾 Stores video metadata in a SQL database (SQLite by default)  
- 📄 Paginated `/videos` API endpoint sorted by publishing date  
- ✅ Easy configuration using `.env` file  
- 🖥️ Simple Dashboard with search, sort, and pagination  

---

## 🛠️ Tech Stack

- Python 3.7+  
- Flask 3  
- Flask-SQLAlchemy  
- Requests  
- SQLite (default DB, can be swapped)  

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/PranshuSangwan/Youtube_Fetcher.git
cd youtube-video-fetcher
```

---

### 2. Setup Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  
Windows: venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file in the root directory:

```env
export YOUTUBE_API_KEYS=your_api_key1,your_api_key2
export YOUTUBE_SEARCH_QUERY=cricket
export YOUTUBE_FETCH_INTERVAL=10
FLASK_APP=run.py
FLASK_ENV=development
```

💡 Use comma-separated values for multiple API keys.  
💡 If `YOUTUBE_SEARCH_QUERY` is not provided, it defaults to: `cricket`.

---

### 📦 Pre-Run: Create the Database

Before running the application for the first time, follow these steps to initialize the database:

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

Then set the Flask app entry point and run the server:

```bash
# For Windows
set FLASK_APP=run.py

# For Mac/Linux
export FLASK_APP=run.py

# Run the app
flask run
```

---

## 📡 API Endpoint

### `GET /videos`

#### Query Params:
- `page` (default: 1)
- `per_page` (default: 10, max: 100)

#### Sample Request:

```bash
curl http://localhost:5000/videos?page=1&per_page=10
```

#### Sample Response:

```json
{
  "videos": [
    {
      "id": "abc123",
      "title": "Latest Cricket Highlights",
      "description": "...",
      "published_at": "2025-05-10T12:34:56Z",
      "thumbnails": {
        "default": "...",
        "medium": "...",
        "high": "..."
      },
      "channel_id": "...",
      "channel_title": "Star Sports"
    }
  ],
  "pagination": {
    "total": 500,
    "pages": 50,
    "current_page": 1,
    "per_page": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 🖥️ Dashboard

A simple dashboard UI is also included to display the stored videos with:

- 🔍 Search functionality
- 🔃 Sorting options
- 📄 Results per page

### ▶️ To Use the Dashboard

Run the Flask app and open:

```bash
http://localhost:5000/
```

- It will show results for the default query: **cricket**
- If a custom query is set in `.env`, the dashboard will use that

---

## 📂 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   │   └── youtube.py
│   └── tasks/
│       └── fetcher.py
├── run.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🧠 Notes

- `publishedAfter` is dynamically set to avoid stale results.  
- If API quota exceeds, the system will rotate to the next key automatically.  
- Optimized DB queries with indexes on `published_at`.  

---
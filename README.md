# Chatbot PoC Project

This project provides a FastAPI application with utilities to connect to a Redis database, import data from Excel, and expose user data via API routes.

## Project Structure

```
chatbot-poc
├── app
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   ├── routes
│   │   ├── __init__.py
│   │   └── user.py            # User API routes
│   ├── utils
│   │   ├── __init__.py
│   │   └── data_import.py     # Excel-to-Redis import logic
│   └── data                   # Excel data files
├── tests
│   ├── __init__.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── test_user.py
│   └── utils
│       ├── __init__.py
│       └── test_data_import.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- Redis server running locally (default port 6379)

Install dependencies in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

**Start Redis server (if not already running):**
```bash
redis-server
```

**Run the FastAPI app:**
```bash
uvicorn app.main:app --reload
```
Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs.

**Import data from Excel to Redis:**
```bash
python -m app.utils.data_import
```

## Running Tests

To run all tests:
```bash
python -m unittest discover tests
```

## Note

Be cautious when running data import or flush scripts, as they will modify or delete data in
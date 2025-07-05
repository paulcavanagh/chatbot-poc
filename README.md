# Redis Flush Project

This project provides a simple utility to connect to a Redis database and flush (clear) its contents. It is designed to be straightforward and easy to use.

## Project Structure

```
redis-flush-project
├── src
│   ├── flushdb.py        # Contains the functionality to connect to Redis and flush the database
│   └── __init__.py       # Marks the src directory as a Python package
├── requirements.txt       # Lists the dependencies required for the project
└── README.md              # Documentation for the project
```

## Requirements

To run this project, you need to have Python installed along with the `redis` library. You can install the required library using the following command:

```
pip install -r requirements.txt
```

## Usage

1. Ensure that you have a running Redis server. You can start a Redis server locally on the default port (6379).
2. Run the `flushdb.py` script to flush the Redis database:

```
python src/flushdb.py
```

This will connect to the Redis server and clear all the data in the specified database.

## Note

Be cautious when using this script, as it will permanently delete all data in the Redis database you are connected to.
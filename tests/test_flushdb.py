import redis

def test_redis_is_running():
    client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0, decode_responses=True)
    try:
        response = client.ping()
    except redis.ConnectionError:
        response = False
    assert response == True, "Redis server is not running or not reachable"
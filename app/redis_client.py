import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def print_all_licence_types():
    keys = r.keys("user:*")
    licence_types = set()
    for key in keys:
        data = r.get(key)
        if data:
            user = json.loads(data)
            licence_types.add(user.get("licenceType"))
    print("All unique licence types:", licence_types)

# Uncomment to run directly
#if __name__ == "__main__":
#     print_all_licence_types()
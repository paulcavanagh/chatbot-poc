
import pandas as pd
import redis
import json



def import_data_to_redis(excel_file='app/data/data.xlsx', redis_host='localhost', redis_port=6379, redis_db=0):
    df = pd.read_excel(excel_file)
  
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    for index, row in df.iterrows():
        key = f"user:{row['Person ID']}"
        user_data = {
            'personName': str(row['Person name']),
            'nationality': str(row['Nationality']),
            'licenceType': str(row['Licence type']),
            'referenceNo': str(row['Reference No.']),
            'dateFrom': str(row['Date from']),
            'dateTo': str(row['Date to']),
            'status':str(row['Status']),
            'inStatusSince': str(row['In status since']),
            'notes': str(row['Notes']),
            'season': str(row['Season']),
        }
        r.set(key, json.dumps(user_data))  # Store as JSON string
    print("Data imported into Redis successfully.")
    return r

def print_all_licence_types():
    keys = r.keys("user:*")
    licence_types = set()
    for key in keys:
        data = r.get(key)
        if data:
            user = json.loads(data)
            licence_types.add(user.get("licenceType"))
    print("All unique licence types:", licence_types)

def get_user_from_redis(r, user_id):
    key = f"user:{user_id}"
    user_data = r.get(key)
    if user_data is None:
        return None
    # Decode bytes to string, then parse JSON
    return json.loads(user_data.decode())



if __name__ == "__main__":
    r = import_data_to_redis()
    user_id = '13016'  # Replace with the actual Person ID you want to look up
    user_data = get_user_from_redis(r, user_id)
    print(user_data)
    print("PAUL CAVANAGH")
    print_all_licence_types()

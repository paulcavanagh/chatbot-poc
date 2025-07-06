from fastapi import APIRouter, HTTPException, Query
from app.redis_client import r
import json

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    key = f"user:{user_id}"
    data = r.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return json.loads(data)

@router.get("/users")
def get_all_user():
    keys = r.keys("user:*")
    users = [json.loads(r.get(key)) for key in keys if r.get(key)]
    return users

@router.get("/users/by-licence-type/")
def get_users_by_licence_type(licence_type: str = Query(..., description="Licence type to filter by")):
    keys = r.keys("user:*")
    users = []
    for key in keys:
        data = r.get(key)
        if data:
            user = json.loads(data)
            if user.get("licenceType") == licence_type:
                users.append(user)
    return users
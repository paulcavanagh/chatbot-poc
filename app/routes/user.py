from fastapi import APIRouter, HTTPException
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

from fastapi import APIRouter, Depends, HTTPException, Header
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/login")
# Verify JWT sent in Authorization header
def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SUPABASE_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
def read_current_user(user=Depends(get_current_user)):
    return user

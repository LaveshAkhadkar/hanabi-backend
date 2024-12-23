from fastapi import APIRouter, HTTPException, Form, Depends
from app.db import users_collection
from app.db.crud.users import create_user, authenticate_user
from app.db.models.users import User, SignupRequest, LoginRequest
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=User)
async def signup(username: str = Form(...), password: str = Form(...)):
    # Check if username already exists
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    user = create_user(users_collection, username, password)
    return user


@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Authenticate the user
    user = authenticate_user(users_collection, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create the JWT token
    token_data = {"sub": user["username"]}
    token = create_access_token(data=token_data)

    # Return the token and user details
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
    }

from bson.objectid import ObjectId
from pymongo.collection import Collection
from app.core.security import hash_password, verify_password
from app.db.models.users import User

def get_user_by_username(users_collection: Collection, username: str):
    """
    Retrieve a user by their username.
    """
    return users_collection.find_one({"username": username})

def create_user(users_collection: Collection, username: str, password: str):
    """
    Create a new user with the given username and password.
    """
    hashed_password = hash_password(password)
    user = {
        "username": username,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_superuser": False,
    }
    result = users_collection.insert_one(user)
    user["_id"] = str(result.inserted_id)  # Convert ObjectId to string for easy JSON handling
    return user

def authenticate_user(users_collection: Collection, username: str, password: str):
    """
    Authenticate a user by checking their username and password.
    """
    user = get_user_by_username(users_collection, username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return user

def get_all_users(users_collection: Collection):
    """
    Get all users in the database.
    """
    users = list(users_collection.find())
    for user in users:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string for each user
    return users

def delete_user(users_collection: Collection, user_id: str):
    """
    Delete a user by their user_id.
    """
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0

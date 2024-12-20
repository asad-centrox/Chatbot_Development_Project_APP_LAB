"""Hi
"""

from typing import Dict
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str


class UserSchema(User):
    hashed_password: str


users_db: Dict[str, UserSchema] = {
    "ai": UserSchema(
        **{
            "username": "ai",
            "email": "template@gmail.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        },
    ),
}


async def get_user(username: str) -> UserSchema | None:
    """
    This should call some sort of db or service to get
    user information
    """
    return users_db.get(username, None)

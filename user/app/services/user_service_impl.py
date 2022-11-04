from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB
from app.services.user_service import UserService

from uuid import uuid4


class UserServiceImpl(UserService):
    def create_user(self, user_create: UserCreate):
        # If username already exists, return None
        user_found = self.get_user_by_username(user_create.username)
        if user_found:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        # If id is not provided, generate one
        if not user_create.id:
            user_create.id = str(uuid4())

        hashed_password = get_password_hash(user_create.password)
        user_for_db = UserInDB(**user_create.dict(), hashed_password=hashed_password)

        user = User(**user_for_db.dict())
        user.save()
        return user.id

    def get_user_by_username(self, username: str):
        users_found = User.user_index.query(username)
        for user in users_found:
            return user
        return None

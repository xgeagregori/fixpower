from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB
from app.services.user_service import UserService

from uuid import uuid4


class UserServiceImpl(UserService):
    def create_user(self, user_create: UserCreate):
        user_already_exists = False

        if user_create.id:
            try:
                user_found = self.get_user_by_id(user_create.id)
                user_already_exists = True
            except:
                pass

            # If id already exists, raise exception
            if user_already_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already exists",
                )
        else:
            # If id is not provided, generate one
            user_create.id = str(uuid4())

        # If username already exists, raise exception
        user_found = self.get_user_by_username(user_create.username)
        if user_found:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        hashed_password = get_password_hash(user_create.password)
        user_for_db = UserInDB(**user_create.dict(), hashed_password=hashed_password)
        print(user_for_db)
        user = User(**user_for_db.dict())
        user.save()
        return user.id

    def get_users(self):
        try:
            return User.scan()
        except User.ScanError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found",
            )

    def get_user_by_username(self, username: str):
        users_found = User.user_index.query(username)
        for user in users_found:
            return user
        return None

    def get_user_by_id(self, id: str):
        try:
            return User.get(id)
        except User.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    def update_user_by_id(self, id: str, user_update: UserCreate):
        user = self.get_user_by_id(id)

        for key, value in user_update.dict().items():
            if value:
                # If password is provided, hash it before updating
                if key == "password":
                    value = get_password_hash(value)
                    setattr(user, "hashed_password", value)
                else:
                    setattr(user, key, value)

        user.save()
        return user

    def delete_user_by_id(self, id: str):
        user = self.get_user_by_id(id)
        user.delete()
        return id

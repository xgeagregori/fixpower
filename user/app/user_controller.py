from fastapi import FastAPI, Depends, HTTPException, status
from mangum import Mangum

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.dependencies.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.dependencies.user import UserDep
from app.schemas.user import UserBase, UserCreate, UserUpdate
from app.schemas.notification import NotificationCreate, NotificationUpdate

app = FastAPI(
    # root_path="/prod/user-api/v1",
    title="User API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/user-api/v1")
router = InferringRouter()


@cbv(router)
class UserController:
    # User routes
    @app.post("/login", tags=["users"])
    async def login(
        form_data: OAuth2PasswordRequestForm = Depends(), self=Depends(UserDep)
    ):
        """Authenticate user and return access token"""
        user = authenticate_user(
            self.user_service, form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @app.post("/register", status_code=status.HTTP_201_CREATED, tags=["users"])
    def register(user_create: UserCreate, self=Depends(UserDep)):
        """Register user"""
        user_id = self.user_service.create_user(user_create)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User not created",
            )
        return {"id": user_id}

    @app.get("/users", tags=["users"])
    def get_users(self=Depends(UserDep)):
        """Get all users"""
        users = self.user_service.get_users()
        return [user.attribute_values for user in users]

    @app.get("/users/me", tags=["users"])
    def get_users(current_user: UserBase = Depends(get_current_user)):
        """Get authenticated user"""
        return current_user.attribute_values

    @app.get("/users/{user_id}", tags=["users"])
    def get_user_by_id(user_id: str, self=Depends(UserDep)):
        """Get user by id"""
        user = self.user_service.get_user_by_id(user_id)
        return user.attribute_values

    @app.patch("/users/{user_id}", tags=["users"])
    def update_user_by_id(user_id, user_update: UserUpdate, self=Depends(UserDep)):
        """Update user by id"""
        user = self.user_service.update_user_by_id(user_id, user_update)
        return user.attribute_values

    @app.delete("/users/{user_id}", tags=["users"])
    def delete_user_by_id(user_id: str, self=Depends(UserDep)):
        """Delete user by id"""
        user_id = self.user_service.delete_user_by_id(user_id)
        return {"id": user_id}

    # Notification routes
    @app.post(
        "/users/{user_id}/notifications",
        status_code=status.HTTP_201_CREATED,
        tags=["notifications"],
    )
    def create_notification(
        user_id: str, notification_create: NotificationCreate, self=Depends(UserDep)
    ):
        """Create notification for user"""
        notification_id = self.notification_service.create_notification(
            user_id, notification_create
        )
        return {"id": notification_id}

    @app.get("/users/{user_id}/notifications", tags=["notifications"])
    def get_notifications_by_user_id(user_id: str, self=Depends(UserDep)):
        """Get notifications for user"""
        notifications = self.notification_service.get_notifications_by_user_id(user_id)
        return [notification.attribute_values for notification in notifications]

    @app.get("/users/{user_id}/notifications/{notification_id}", tags=["notifications"])
    def get_notification_by_id(
        user_id: str, notification_id: str, self=Depends(UserDep)
    ):
        """Get notification by id for user"""
        notification = self.notification_service.get_notification_by_id(
            user_id, notification_id
        )
        return notification.attribute_values

    @app.patch(
        "/users/{user_id}/notifications/{notification_id}", tags=["notifications"]
    )
    def update_notification_by_id(
        user_id: str,
        notification_id: str,
        notification_update: NotificationUpdate,
        self=Depends(UserDep),
    ):
        """Update notification by id for user"""
        notification = self.notification_service.update_notification_by_id(
            user_id, notification_id, notification_update
        )
        return notification.attribute_values

    @app.delete(
        "/users/{user_id}/notifications/{notification_id}", tags=["notifications"]
    )
    def delete_notification_by_id(
        user_id: str, notification_id: str, self=Depends(UserDep)
    ):
        """Delete notification by id for user"""
        notification_id = self.notification_service.delete_notification_by_id(
            user_id, notification_id
        )
        return {"id": notification_id}


app.include_router(router)

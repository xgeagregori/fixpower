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
from app.dependencies.auth import check_user_permissions
from app.dependencies.user import UserDep
from app.schemas.chat_message import (
    ChatMessageCreate,
    ChatMessageUpdate,
    ChatMessageOut,
)
from app.schemas.profile import ProfileUpdate, ProfileOut
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from app.schemas.settings import SettingsOut
from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserOut, UserOutCurrent
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationOut,
)

app = FastAPI(
    root_path="/prod/user-api/v1",
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
    def get_users(
        current_user: UserInDB = Depends(get_current_user), self=Depends(UserDep)
    ):
        """Get all users"""
        users = self.user_service.get_users()

        # Remove hashed_password from response
        formatted_users = []
        for user in users:
            user.profile.settings = SettingsOut(
                **user.profile.settings.attribute_values
            )
            user.profile = ProfileOut(**user.profile.attribute_values)
            formatted_user = UserOut(**user.attribute_values)
            formatted_users.append(formatted_user)

        return formatted_users

    @app.get("/users/me", tags=["users"])
    def get_users(current_user: UserInDB = Depends(get_current_user)):
        """Get authenticated user"""
        for notification in current_user.notifications:
            notification = NotificationOut(**notification.attribute_values)
        current_user.profile.settings = SettingsOut(
            **current_user.profile.settings.attribute_values
        )
        current_user.profile = ProfileOut(**current_user.profile.attribute_values)
        formatted_user = UserOutCurrent(**current_user.attribute_values)
        return formatted_user

    @app.get("/users/{user_id}", tags=["users"])
    def get_user_by_id(
        user_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Get user by id"""
        user = self.user_service.get_user_by_id(user_id)
        user.profile.settings = SettingsOut(**user.profile.settings.attribute_values)
        user.profile = ProfileOut(**user.profile.attribute_values)
        formatted_user = UserOut(**user.attribute_values)
        return formatted_user

    @app.patch("/users/{user_id}", tags=["users"])
    def update_user_by_id(
        user_id,
        user_update: UserUpdate,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Update user by id"""
        check_user_permissions(current_user, user_id)
        user = self.user_service.update_user_by_id(user_id, user_update)

        for notification in user.notifications:
            notification = NotificationOut(**notification.attribute_values)
        user.profile.settings = SettingsOut(**user.profile.settings.attribute_values)
        user.profile = ProfileOut(**user.profile.attribute_values)

        formatted_user = UserOutCurrent(**user.attribute_values)
        return formatted_user

    @app.delete("/users/{user_id}", tags=["users"])
    def delete_user_by_id(
        user_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Delete user by id"""
        check_user_permissions(current_user, user_id)
        user_id = self.user_service.delete_user_by_id(user_id)
        return {"id": user_id}

    # Notification routes
    @app.post(
        "/users/{user_id}/notifications",
        status_code=status.HTTP_201_CREATED,
        tags=["notifications"],
    )
    def create_notification(
        user_id: str,
        notification_create: NotificationCreate,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Create notification for user"""
        check_user_permissions(current_user, user_id)
        notification_id = self.notification_service.create_notification(
            user_id, notification_create
        )
        return {"id": notification_id}

    @app.get("/users/{user_id}/notifications", tags=["notifications"])
    def get_notifications_by_user_id(
        user_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Get notifications for user"""
        check_user_permissions(current_user, user_id)
        notifications = self.notification_service.get_notifications_by_user_id(user_id)
        return [
            NotificationOut(**notification.attribute_values)
            for notification in notifications
        ]

    @app.get("/users/{user_id}/notifications/{notification_id}", tags=["notifications"])
    def get_notification_by_id(
        user_id: str,
        notification_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Get notification by id for user"""
        check_user_permissions(current_user, user_id)
        notification = self.notification_service.get_notification_by_id(
            user_id, notification_id
        )
        return NotificationOut(**notification.attribute_values)

    @app.patch(
        "/users/{user_id}/notifications/{notification_id}", tags=["notifications"]
    )
    def update_notification_by_id(
        user_id: str,
        notification_id: str,
        notification_update: NotificationUpdate,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Update notification by id for user"""
        check_user_permissions(current_user, user_id)
        notification = self.notification_service.update_notification_by_id(
            user_id, notification_id, notification_update
        )
        return NotificationOut(**notification.attribute_values)

    @app.delete(
        "/users/{user_id}/notifications/{notification_id}", tags=["notifications"]
    )
    def delete_notification_by_id(
        user_id: str,
        notification_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Delete notification by id for user"""
        check_user_permissions(current_user, user_id)
        notification_id = self.notification_service.delete_notification_by_id(
            user_id, notification_id
        )
        return {"id": notification_id}

    # Profile routes
    @app.get("/users/{user_id}/profile", tags=["profile"])
    def get_profile_by_user_id(
        user_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Get profile for user"""
        profile = self.profile_service.get_profile_by_user_id(user_id)
        profile.settings = SettingsOut(**profile.settings.attribute_values)

        return ProfileOut(**profile.attribute_values)

    @app.patch("/users/{user_id}/profile", tags=["profile"])
    def update_profile_by_user_id(
        user_id: str,
        profile_update: ProfileUpdate,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Update profile for user"""
        check_user_permissions(current_user, user_id)
        profile = self.profile_service.update_profile_by_user_id(
            user_id, profile_update
        )
        profile.settings = SettingsOut(**profile.settings.attribute_values)
        return ProfileOut(**profile.attribute_values)

    # Review routes
    @app.post(
        "/users/{user_id}/reviews",
        status_code=status.HTTP_201_CREATED,
        tags=["reviews"],
    )
    def create_review(
        user_id: str,
        review_create: ReviewCreate,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Create review for user"""
        # The sender of the review must be the current user
        check_user_permissions(current_user, review_create.sender_id)
        review_id = self.review_service.create_review(user_id, review_create)
        return {"id": review_id}

    @app.get("/users/{user_id}/reviews", tags=["reviews"])
    def get_reviews_by_user_id(
        user_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Get reviews for user"""
        reviews = self.review_service.get_reviews_by_user_id(user_id)
        return [ReviewOut(**review.attribute_values) for review in reviews]

    @app.get("/users/{user_id}/reviews/{review_id}", tags=["reviews"])
    def get_review_by_id(
        user_id: str,
        review_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Get review by id for user"""
        review = self.review_service.get_review_by_id(user_id, review_id)
        return ReviewOut(**review.attribute_values)

    @app.patch("/users/{user_id}/reviews/{review_id}", tags=["reviews"])
    def update_review_by_id(
        user_id: str,
        review_id: str,
        review_update: ReviewUpdate,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Update review by id for user"""
        review = self.review_service.get_review_by_id(user_id, review_id)
        check_user_permissions(current_user, review.sender_id)
        review = self.review_service.update_review_by_id(
            user_id, review_id, review_update
        )
        return ReviewOut(**review.attribute_values)

    @app.delete("/users/{user_id}/reviews/{review_id}", tags=["reviews"])
    def delete_review_by_id(
        user_id: str,
        review_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Delete review by id for user"""
        review = self.review_service.get_review_by_id(user_id, review_id)
        check_user_permissions(current_user, review.sender_id)
        review_id = self.review_service.delete_review_by_id(user_id, review_id)
        return {"id": review_id}

    # ChatMessage routes
    @app.post(
        "/users/{user_id}/chat-messages",
        status_code=status.HTTP_201_CREATED,
        tags=["chat-messages"],
    )
    def create_chat_message(
        user_id: str,
        chat_message_create: ChatMessageCreate,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Create chat message"""
        # The sender of the chat message must be the current user
        check_user_permissions(current_user, chat_message_create.sender_id)
        chat_message_id = self.chat_message_service.create_chat_message(
            user_id, chat_message_create
        )
        return {"id": chat_message_id}

    @app.get("/users/{user_id}/chat-messages", tags=["chat-messages"])
    def get_chat_messages_by_user_id(
        user_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Get chat messages for user"""
        check_user_permissions(current_user, user_id)
        chat_messages = self.chat_message_service.get_chat_messages_by_user_id(user_id)
        return [
            ChatMessageOut(**chat_message.attribute_values)
            for chat_message in chat_messages
        ]

    @app.get("/users/{user_id}/chat-messages/{chat_message_id}", tags=["chat-messages"])
    def get_chat_message_by_id(
        user_id: str,
        chat_message_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Get chat message by id for user"""
        check_user_permissions(current_user, user_id)
        chat_message = self.chat_message_service.get_chat_message_by_id(
            user_id, chat_message_id
        )
        return ChatMessageOut(**chat_message.attribute_values)

    @app.patch(
        "/users/{user_id}/chat-messages/{chat_message_id}", tags=["chat-messages"]
    )
    def update_chat_message_by_id(
        user_id: str,
        chat_message_id: str,
        chat_message_update: ChatMessageUpdate,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Update chat message by id for user"""
        chat_message = self.chat_message_service.get_chat_message_by_id(
            user_id, chat_message_id
        )
        check_user_permissions(current_user, chat_message.sender_id)
        chat_message = self.chat_message_service.update_chat_message_by_id(
            user_id, chat_message_id, chat_message_update
        )
        return ChatMessageOut(**chat_message.attribute_values)

    @app.delete(
        "/users/{user_id}/chat-messages/{chat_message_id}", tags=["chat-messages"]
    )
    def delete_chat_message_by_id(
        user_id: str,
        chat_message_id: str,
        current_user: UserInDB = Depends(get_current_user),
        self=Depends(UserDep),
    ):
        """Delete chat message by id for user"""
        chat_message = self.chat_message_service.get_chat_message_by_id(
            user_id, chat_message_id
        )
        check_user_permissions(current_user, chat_message.sender_id)
        chat_message_id = self.chat_message_service.delete_chat_message_by_id(
            user_id, chat_message_id
        )
        return {"id": chat_message_id}


app.include_router(router)

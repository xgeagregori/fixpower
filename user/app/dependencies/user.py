from app.services.chat_message_service import ChatMessageService
from app.services.chat_message_service_impl import ChatMessageServiceImpl
from app.services.notification_service import NotificationService
from app.services.notification_service_impl import NotificationServiceImpl
from app.services.profile_service import ProfileService
from app.services.profile_service_impl import ProfileServiceImpl
from app.services.review_service import ReviewService
from app.services.review_service_impl import ReviewServiceImpl
from app.services.user_service import UserService
from app.services.user_service_impl import UserServiceImpl


class UserDep:
    def __init__(self):
        self.user_service: UserService = UserServiceImpl()

        self.chat_message_service: ChatMessageService = ChatMessageServiceImpl()
        self.notification_service: NotificationService = NotificationServiceImpl()
        self.profile_service: ProfileService = ProfileServiceImpl()
        self.review_service: ReviewService = ReviewServiceImpl()

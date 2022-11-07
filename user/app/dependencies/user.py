from app.services.notification_service import NotificationService
from app.services.notification_service_impl import NotificationServiceImpl
from app.services.profile_service import ProfileService
from app.services.profile_service_impl import ProfileServiceImpl
from app.services.user_service import UserService
from app.services.user_service_impl import UserServiceImpl


class UserDep:
    def __init__(self):
        self.user_service: UserService = UserServiceImpl()
        self.notification_service: NotificationService = NotificationServiceImpl()
        self.profile_service: ProfileService = ProfileServiceImpl()

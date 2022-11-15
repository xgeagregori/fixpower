from app.schemas.profile import ProfileUpdate
from app.services.profile_service import ProfileService
from app.services.user_service_impl import UserServiceImpl


class ProfileServiceImpl(ProfileService):
    def __init__(self):
        self.user_service = UserServiceImpl()

    def get_profile_by_user_id(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        return user.profile

    def update_profile_by_user_id(self, user_id, profile_update: ProfileUpdate):
        user = self.user_service.get_user_by_id(user_id)

        for key, value in profile_update.dict().items():
            if value:
                if key == "settings":
                    for setting_key, setting_value in value.items():
                        if setting_value is not None:
                            setattr(user.profile.settings, setting_key, setting_value)
                else:
                    setattr(user.profile, key, value)
                user.save()
        return user.profile

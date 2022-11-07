from abc import ABC, abstractmethod


class ProfileService(ABC):
    @abstractmethod
    def get_profile_by_user_id(self, id):
        pass

    @abstractmethod
    def update_profile_by_user_id(self, id, profile):
        pass

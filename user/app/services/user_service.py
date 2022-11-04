from abc import ABC, abstractmethod


class UserService(ABC):
    @abstractmethod
    def create_user(self, user):
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        pass

from abc import ABC, abstractmethod


class UserService(ABC):
    @abstractmethod
    def create_user(self, user):
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        pass

    @abstractmethod
    def get_user_by_id(self, id):
        pass

    @abstractmethod
    def update_user_by_id(self, id, user):
        pass

    @abstractmethod
    def delete_user_by_id(self, id):
        pass

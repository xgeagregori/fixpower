from abc import ABC, abstractmethod


class FavouriteService(ABC):
    @abstractmethod
    def create_favourite(self, user_id, favourite_create):
        pass

    @abstractmethod
    def get_favourites_by_user_id(self, user_id):
        pass

    @abstractmethod
    def delete_favourite_by_id(self, favourite_id):
        pass

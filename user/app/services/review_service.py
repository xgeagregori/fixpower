from abc import ABC, abstractmethod


class ReviewService(ABC):
    @abstractmethod
    def create_review(self, review):
        pass

    @abstractmethod
    def get_reviews_by_user_id(self, user_id):
        pass

    @abstractmethod
    def get_review_by_id(self, review_id):
        pass

    @abstractmethod
    def update_review_by_id(self, review_id, review_update):
        pass

    @abstractmethod
    def delete_review_by_id(self, review_id):
        pass

from fastapi import HTTPException, status

from app.models.review import Review
from app.services.review_service import ReviewService
from app.services.user_service_impl import UserServiceImpl

from uuid import uuid4


class ReviewServiceImpl(ReviewService):
    def __init__(self):
        self.user_service = UserServiceImpl()

    def create_review(self, user_id, review_create):
        generated_id = str(uuid4())
        review = Review(id=generated_id, **review_create.dict())

        user = self.user_service.get_user_by_id(user_id)
        user.profile.reviews.append(review)
        user.save()

        return review.id

    def get_reviews_by_user_id(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        return user.profile.reviews

    def get_review_by_id(self, user_id, review_id):
        user = self.user_service.get_user_by_id(user_id)
        for review in user.profile.reviews:
            if review.id == review_id:
                return review
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    def update_review_by_id(self, user_id, review_id, review_update):
        user = self.user_service.get_user_by_id(user_id)
        for review in user.profile.reviews:
            if review.id == review_id:
                for key, value in review_update.dict().items():
                    if value:
                        setattr(review, key, value)
                        user.save()
                return review

    def delete_review_by_id(self, user_id, review_id):
        user = self.user_service.get_user_by_id(user_id)
        for review in user.profile.reviews:
            if review.id == review_id:
                user.profile.reviews.remove(review)
                user.save()
                return review_id

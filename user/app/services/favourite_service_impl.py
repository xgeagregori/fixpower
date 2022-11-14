from fastapi import HTTPException, status

from app.models.product_listing import ProductListing
from app.services.favourite_service import FavouriteService
from app.services.user_service_impl import UserServiceImpl


class FavouriteServiceImpl(FavouriteService):
    def __init__(self):
        self.user_service = UserServiceImpl()

    def create_favourite(self, user_id, favourite_create):
        product_listing = ProductListing(**favourite_create.dict())

        user = self.user_service.get_user_by_id(user_id)
        user.favourites.append(product_listing)
        user.save()
        return product_listing.id

    def get_favourites_by_user_id(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        return user.favourites

    def delete_favourite_by_id(self, user_id, favourite_id):
        user = self.user_service.get_user_by_id(user_id)
        for favourite in user.favourites:
            if favourite.id == favourite_id:
                user.favourites.remove(favourite)
                user.save()
                return favourite_id
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favourite not found",
        )

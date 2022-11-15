from fastapi import HTTPException, status

from app.dependencies.auth import authenticate_service
from app.models.commands.command import Command

import os
import requests


class ShippedCommand(Command):
    def __init__(self):
        self.access_token = authenticate_service()

    def execute(self, transaction):
        product_listing = self.get_product_listing(transaction)

        if (
            product_listing["seller"] is not None
            and product_listing["buyer"] is not None
        ):
            self.send_notification_seller(product_listing)
            self.send_notification_buyer(product_listing)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product listing does not have a seller or buyer",
            )

    def get_product_listing(self, transaction):
        product_listing = requests.get(
            os.getenv("AWS_API_GATEWAY_URL")
            + f"/product-listing-api/v1/product-listings/{transaction.product_listing.id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        return product_listing.json()

    def send_notification_seller(self, product_listing):
        requests.post(
            os.getenv("AWS_API_GATEWAY_URL")
            + f"/user-api/v1/users/"
            + product_listing["seller"]["id"]
            + "/notifications",
            json={
                "type": "SHIPPED",
                "title": "You have shipped an item!",
                "message": "Your item has been shipped. Please wait for the buyer to receive it.",
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

    def send_notification_buyer(self, product_listing):
        requests.post(
            os.getenv("AWS_API_GATEWAY_URL")
            + f"/user-api/v1/users/"
            + product_listing["buyer"]["id"]
            + "/notifications",
            json={
                "type": "SHIPPED",
                "title": "Your item has been shipped!",
                "message": "Your item has been shipped. Please wait for it to arrive.",
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

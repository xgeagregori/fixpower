from app.dependencies.auth import authenticate_service
from app.models.commands.command import Command
from app.schemas.transaction import TransactionState

import os
import requests


class ReturnedCommand(Command):
    def __init__(self):
        self.access_token = authenticate_service()

    def execute(self, transaction):
        product_listing = self.get_product_listing(transaction)

        self.send_notification_seller(product_listing)
        self.send_notification_buyer(product_listing)

    def get_product_listing(self, transaction):
        product_listing = requests.get(
            os.getenv("AWS_API_GATEWAY_URL")
            + f"product-listing-api/v1/product-listings/{transaction.product_listing.id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        return product_listing.json()

    def send_notification_seller(self, product_listing):
        requests.post(
            os.getenv("AWS_API_GATEWAY_URL")
            + f"/user-api/v1/users/" + product_listing["seller"]["id"] + "/notifications",
            json={
                "type": "RETURNED",
                "title": "Your item has been returned!",
                "message": "Your item has been returned. Please wait for it to arrive.",
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

    def send_notification_buyer(self, product_listing):
        requests.post(
            os.getenv("AWS_API_GATEWAY_URL")
            + f"/user-api/v1/users/" + product_listing["buyer"]["id"] + "/notifications",
            json={
                "type": "RETURNED",
                "title": "You have returned an item!",
                "message": "You have returned an item. We will refund you the money.",
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

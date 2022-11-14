from app.dependencies.auth import authenticate_service
from app.models.commands.command import Command
from app.schemas.transaction import TransactionState

import os
import requests


class PaidCommand(Command):
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
            + "/user-api/v1/users/" + product_listing["seller"]["id"] + "/notifications",
            json={
                "type": "PAID",
                "title": "You have sold an item!",
                "message": "Your item has been paid for. Please ship it as soon as possible.",
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

    def send_notification_buyer(self, product_listing):
        requests.post(
            os.getenv("AWS_API_GATEWAY_URL")
            + f"/user-api/v1/users/" + product_listing["buyer"]["id"] + "/notifications",
            json={
                "type": "PAID",
                "title": "You have bought an item!",
                "message": "Your item has been paid for. Please wait for the seller to ship it.",
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

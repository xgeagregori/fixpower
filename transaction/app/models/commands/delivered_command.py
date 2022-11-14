from app.dependencies.auth import authenticate_service
from app.models.commands.command import Command
from app.schemas.transaction import TransactionState

import os
import requests

class DeliveredCommand(Command):
    def __init__(self):
        self.access_token = authenticate_service()

    def execute(self, transaction):
        transaction.state = TransactionState.DELIVERED
        transaction.save()

        product_listing = self.get_product_listing()

        self.send_notification_seller(product_listing)
        self.send_notification_buyer(product_listing)

        return transaction

    def get_product_listing(self):
        product_listing = requests.get(
            os.getenv(
                "AWS_API_GATEWAY_URL") + f"product-listing-api/v1/product-listings/{self.transaction.product_listing_id}",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )

        return product_listing.json()

    def send_notification_seller(self, product_listing):
        requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + f"/user-api/v1/users/{product_listing.seller.id}/notifications",
            json={
                "type": "DELIVERED",
                "title": "Your transaction has been completed!",
                "message": "The item you shipped has been delivered. Your money has been transferred to your account."
            },
        )

    def send_notification_buyer(self, product_listing):
        requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + f"/user-api/v1/users/{product_listing.buyer.id}/notifications",
            json={
                "type": "DELIVERED",
                "title": "Your transaction has been completed!",
                "message": "Thank you for confirming the delivery of your item. Your money has been transferred to the seller's account."
            },
        )
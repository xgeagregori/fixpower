from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    UTCDateTimeAttribute,
    NumberAttribute,
)

from app.models.user import UserAttribute

import datetime
import os


class Order(Model):
    class Meta:
        table_name = os.getenv("AWS_SHOPPING_CART_TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID_LAMBDA")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY_LAMBDA")

    id = UnicodeAttribute(hash_key=True)
    # items= ListAttribute(of=ProductListing, default=[])
    user = UserAttribute()
    price = NumberAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now())

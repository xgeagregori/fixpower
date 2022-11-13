from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, NumberAttribute, BooleanAttribute, MapAttribute, ListAttribute

from app.models.product_listing import ProductListingAttribute

import datetime
import os


class Transaction(Model):
    class Meta:
        table_name = os.getenv("AWS_TRANSACTION_TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID_LAMBDA")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY_LAMBDA")

    id = UnicodeAttribute(hash_key=True)
    state = UnicodeAttribute()
    product_listing = ProductListingAttribute()
    final_price = NumberAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now)

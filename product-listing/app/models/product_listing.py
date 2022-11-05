from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
import os




class ProductListingIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "username"
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    username = UnicodeAttribute(hash_key=True)



class ProductListing(Model):
    class Meta:
        table_name = os.getenv("AWS_PRODUCT_LISTING_TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID_LAMBDA")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY_LAMBDA")

    id = UnicodeAttribute(hash_key=True)
    listed_price = NumberAttribute()
    # productListing_index = ProductListingIndex()

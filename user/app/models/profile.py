from pynamodb.attributes import MapAttribute, UnicodeAttribute, BinaryAttribute, ListAttribute
from app.models.review import Review
from app.models.settings import SettingsAttribute

class ProfileAttribute(MapAttribute):
    picture = BinaryAttribute(null=True)
    address = UnicodeAttribute()
    reviews = ListAttribute(of=Review, default=[])
    settings = SettingsAttribute()
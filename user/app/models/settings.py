from pynamodb.attributes import MapAttribute, BooleanAttribute, UnicodeAttribute


class SettingsAttribute(MapAttribute):
    sms_notifications = BooleanAttribute()
    email_notifications = BooleanAttribute()
    payment_method = UnicodeAttribute(null=True)

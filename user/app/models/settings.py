from pynamodb.attributes import MapAttribute, BooleanAttribute

class SettingsAttribute(MapAttribute):
    sms_notifications = BooleanAttribute()
    email_notifications = BooleanAttribute()
from fastapi import HTTPException, status

from app.models.notification import Notification
from app.models.notifier import Notifier
from app.models.notification_decorators import AppNotifier, SMSNotifier, EmailNotifier
from app.services.notification_service import NotificationService
from app.services.user_service_impl import UserServiceImpl

from uuid import uuid4


class NotificationServiceImpl(NotificationService):
    def __init__(self):
        self.user_service = UserServiceImpl()

    def create_notification(self, user_id, notification_create):
        generated_id = str(uuid4())
        notification = Notification(id=generated_id, **notification_create.dict())

        user = self.user_service.get_user_by_id(user_id)
        user.notifications.append(notification)
        user.save()

        # Send notification to user based on their settings
        settings = user.profile.settings
        notifier: Notifier = AppNotifier()
        if settings.sms_notifications:
            notifier = SMSNotifier(notifier)
        if settings.email_notifications:
            notifier = EmailNotifier(notifier)

        notifier.send(notification.attribute_values)

        return notification.id

    def get_notifications_by_user_id(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        return user.notifications

    def get_notification_by_id(self, user_id, notification_id):
        user = self.user_service.get_user_by_id(user_id)
        for notification in user.notifications:
            if notification.id == notification_id:
                return notification
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    def update_notification_by_id(self, user_id, notification_id, notification_update):
        user = self.user_service.get_user_by_id(user_id)
        for notification in user.notifications:
            if notification.id == notification_id:
                for key, value in notification_update.dict().items():
                    if value:
                        setattr(notification, key, value)
                        user.save()
                return notification

    def delete_notification_by_id(self, user_id, notification_id):
        user = self.user_service.get_user_by_id(user_id)
        for notification in user.notifications:
            if notification.id == notification_id:
                user.notifications.remove(notification)
                user.save()
                return notification_id

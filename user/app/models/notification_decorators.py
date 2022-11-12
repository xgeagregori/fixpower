from abc import ABC, abstractmethod

from app.models.notifier import Notifier
from app.services.user_service_impl import UserServiceImpl


class NotifierDecorator(Notifier, ABC):
    def __init__(self, notifier):
        self.notifier = notifier

    @abstractmethod
    def send(self, notification):
        if self.notifier is not None:
            self.notifier.send(notification)


class AppNotifier(Notifier):
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_service = UserServiceImpl()

    def send(self, notification):
        self.sendAppNotification(notification)

    def sendAppNotification(self, notification):
        user = self.user_service.get_user_by_id(self.user_id)
        user.notifications.append(notification)
        user.save()


class SMSNotifier(NotifierDecorator):
    def __init__(self, notifier):
        super().__init__(notifier)

    def send(self, notification):
        super().send(notification)
        self.sendSMSNotification(notification)

    def sendSMSNotification(self, notification):
        print("Sending SMS notification")


class EmailNotifier(NotifierDecorator):
    def __init__(self, notifier):
        super().__init__(notifier)

    def send(self, notification):
        super().send(notification)
        self.sendEmailNotification(notification)

    def sendEmailNotification(self, notification):
        print("Sending Email notification")

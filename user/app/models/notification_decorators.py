from abc import ABC, abstractmethod

from app.models.notifier import Notifier


class NotifierDecorator(Notifier, ABC):
    def __init__(self, notifier):
        self.notifier = notifier

    @abstractmethod
    def send(self, notification):
        if self.notifier is not None:
            self.notifier.send(notification)


class AppNotifier(Notifier):
    def send(self, notification):
        self.sendAppNotification(notification)

    def sendAppNotification(self, notification):
        print("Sending app notification")


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
        print("Sending email notification")

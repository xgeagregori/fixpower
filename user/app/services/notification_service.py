from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def create_notification(self, notification):
        pass

    @abstractmethod
    def get_notifications_by_user_id(self):
        pass

    @abstractmethod
    def get_notification_by_id(self, id):
        pass

    @abstractmethod
    def update_notification_by_id(self, id, notification):
        pass

    @abstractmethod
    def delete_notification_by_id(self, id):
        pass

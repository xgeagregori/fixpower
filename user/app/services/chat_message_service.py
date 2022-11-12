from abc import ABC, abstractmethod


class ChatMessageService(ABC):
    @abstractmethod
    def create_chat_message(self, chat_message):
        pass

    @abstractmethod
    def get_chat_messages_by_user_id(self, user_id):
        pass

    @abstractmethod
    def get_chat_message_by_id(self, chat_message_id):
        pass

    @abstractmethod
    def update_chat_message_by_id(self, chat_message):
        pass

    @abstractmethod
    def delete_chat_message_by_id(self, chat_message_id):
        pass

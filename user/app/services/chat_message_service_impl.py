from fastapi import HTTPException, status

from app.models.chat_message import ChatMessage
from app.services.chat_message_service import ChatMessageService
from app.services.user_service_impl import UserServiceImpl

from uuid import uuid4


class ChatMessageServiceImpl(ChatMessageService):
    def __init__(self):
        self.user_service = UserServiceImpl()

    def create_chat_message(self, user_id, chat_message_create):
        generated_id = str(uuid4())
        chat_message = ChatMessage(id=generated_id, **chat_message_create.dict())

        user_sender = self.user_service.get_user_by_id(chat_message_create.sender_id)
        user_sender.chat_messages.append(chat_message)
        user_sender.save()

        user_recipient = self.user_service.get_user_by_id(
            chat_message_create.recipient_id
        )
        user_recipient.chat_messages.append(chat_message)
        user_recipient.save()

        return chat_message.id

    def get_chat_messages_by_user_id(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        return user.chat_messages

    def get_chat_message_by_id(self, user_id, chat_message_id):
        user = self.user_service.get_user_by_id(user_id)
        for chat_message in user.chat_messages:
            if chat_message.id == chat_message_id:
                return chat_message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ChatMessage not found",
        )

    def update_chat_message_by_id(self, user_id, chat_message_id, chat_message_update):
        chat_message = self.get_chat_message_by_id(user_id, chat_message_id)
        for user_id in [chat_message.sender_id, chat_message.recipient_id]:
            user = self.user_service.get_user_by_id(user_id)
            for chat_message in user.chat_messages:
                if chat_message.id == chat_message_id:
                    for key, value in chat_message_update.dict().items():
                        if value:
                            setattr(chat_message, key, value)
                            user.save()
        return chat_message

    def delete_chat_message_by_id(self, user_id, chat_message_id):
        chat_message = self.get_chat_message_by_id(user_id, chat_message_id)
        for user_id in [chat_message.sender_id, chat_message.recipient_id]:
            user = self.user_service.get_user_by_id(user_id)
            for chat_message in user.chat_messages:
                if chat_message.id == chat_message_id:
                    user.chat_messages.remove(chat_message)
                    user.save()
        return chat_message_id

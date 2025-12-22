from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.models import User, Conversation, Message, UserPreference
from database.session import db_manager


class DuplicateUser(Exception):
    pass


class UserNotFound(Exception):
    pass


class ConversationNotFound(Exception):
    pass


def register_user(
    username: str, password: str, full_name: Optional[str] = None
) -> User:
    with db_manager.session_scope() as session:
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            raise DuplicateUser(f"User with username='{username}' already exists.")

        new_user = User(username=username, full_name=full_name)
        session.add(new_user)
        session.flush()

        preferences = UserPreference(
            user_id=new_user.id, ai_model="gemini-2.5-flash", max_tokens=1000
        )
        session.add(preferences)

        preferences.custom_settings = {"password": password}

        return new_user


def login_user(username: str, password: str) -> int:
    with db_manager.session_scope() as session:
        user = session.query(User).filter_by(username=username).first()

        if not user:
            raise UserNotFound("Login or password is incorrect.")
        stored_password = (
            user.preferences.custom_settings.get("password")
            if user.preferences
            else None
        )

        if stored_password != password:
            raise UserNotFound("Login or password is incorrect.")

        return user.id


def get_user_by_id(user_id: int) -> Optional[User]:
    with db_manager.session_scope() as session:
        return session.query(User).filter_by(id=user_id).first()


def get_user_by_username(username: str) -> Optional[User]:
    with db_manager.session_scope() as session:
        return session.query(User).filter_by(username=username).first()


def create_conversation(user_id: int, title: Optional[str] = None) -> int:
    with db_manager.session_scope() as session:
        conversation = Conversation(user_id=user_id, title=title or "New Chat")
        session.add(conversation)
        session.flush()
        return conversation.id


def get_user_conversations(user_id: int) -> List[dict]:
    with db_manager.session_scope() as session:
        conversations = session.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.is_active == True
        ).order_by(Conversation.updated_at.desc()).all()
        
        result = []
        for conv in conversations:
            result.append({
                'id': conv.id,
                'title': conv.title,
                'updated_at': conv.updated_at,
                'user_id': conv.user_id
            })
        return result


def get_conversation_by_id(conversation_id: int) -> Optional[Conversation]:
    with db_manager.session_scope() as session:
        return session.query(Conversation).filter_by(id=conversation_id).first()


def get_or_create_active_conversation(user_id: int) -> int:
    with db_manager.session_scope() as session:
        conversation = (
            session.query(Conversation)
            .filter_by(user_id=user_id, is_active=True)
            .order_by(Conversation.updated_at.desc())
            .first()
        )

        if not conversation:
            conversation = Conversation(user_id=user_id, title="Chat Session")
            session.add(conversation)
            session.flush()

        return conversation.id


def save_message(
    conversation_id: int, role: str, content: str, metadata: Optional[dict] = None
) -> Message:
    with db_manager.session_scope() as session:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            message_metadata=metadata,
        )
        session.add(message)

        conversation = session.query(Conversation).filter_by(id=conversation_id).first()
        if conversation:
            from datetime import datetime, timezone

            conversation.updated_at = datetime.now(timezone.utc)

        session.flush()
        return message


def get_conversation_messages(
    conversation_id: int, limit: Optional[int] = None
) -> List[dict]:
    with db_manager.session_scope() as session:
        query = (
            session.query(Message)
            .filter_by(conversation_id=conversation_id)
            .order_by(Message.created_at)
        )

        if limit:
            total = query.count()
            if total > limit:
                query = query.offset(total - limit)

        messages = query.all()
        
        return [
            {
                'id': msg.id,
                'conversation_id': msg.conversation_id,
                'role': msg.role,
                'content': msg.content,
                'message_metadata': msg.message_metadata,
                'created_at': msg.created_at
            }
            for msg in messages
        ]


def load_history(
    user_id: int, conversation_id: Optional[int] = None, limit: Optional[int] = None
) -> List[Tuple[str, str]]:
    with db_manager.session_scope() as session:
        if conversation_id:
            messages = get_conversation_messages(conversation_id, limit)
        else:
            conversation = (
                session.query(Conversation)
                .filter_by(user_id=user_id, is_active=True)
                .order_by(Conversation.updated_at.desc())
                .first()
            )

            if not conversation:
                return []

            messages = get_conversation_messages(conversation.id, limit)
        
        return [(msg['content'], msg['role']) for msg in messages]


def get_user_preferences(user_id: int) -> Optional[UserPreference]:
    with db_manager.session_scope() as session:
        return session.query(UserPreference).filter_by(user_id=user_id).first()


def update_user_preferences(user_id: int, **kwargs) -> UserPreference:

    with db_manager.session_scope() as session:
        preferences = session.query(UserPreference).filter_by(user_id=user_id).first()

        if not preferences:
            preferences = UserPreference(user_id=user_id)
            session.add(preferences)

        for key, value in kwargs.items():
            if hasattr(preferences, key):
                setattr(preferences, key, value)

        session.flush()
        return preferences


def delete_conversation(conversation_id: int):
    with db_manager.session_scope() as session:
        conversation = session.query(Conversation).filter_by(id=conversation_id).first()
        if conversation:
            session.delete(conversation)


def mark_conversation_inactive(conversation_id: int):
    with db_manager.session_scope() as session:
        conversation = session.query(Conversation).filter_by(id=conversation_id).first()
        if conversation:
            conversation.is_active = False

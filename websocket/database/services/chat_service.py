from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.chat_models import *


# Get chat history cache from Redis by room id
async def get_history_cache(session: AsyncSession, room_id):
    pass


# Get all messages from PostgresSQL by room id
async def get_messages_by_room_name(session: AsyncSession, room_name: str) -> list[Message]:
    result = await session.execute(select(Message).filter_by(room_name=room_name))
    return result.scalars().all()


# Add message to PostgresSQL
def add_message(session: AsyncSession, text: str, sender_id: int, room_id: int):
    message = Message(text=text, sender_id=sender_id, room_id=room_id)
    session.add(message)
    return message

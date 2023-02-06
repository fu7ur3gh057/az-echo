from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.chat_models import *


async def get_messages_by_room_name(session: AsyncSession, room_name: str) -> list[Message]:
    result = await session.execute(select(Message).filter_by(room_name=room_name))
    return result.scalars().all()


async def add_message(session: AsyncSession, text: str, user_id: str, room_name: str):
    pass

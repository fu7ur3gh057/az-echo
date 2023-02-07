import datetime
from sqlalchemy import Column, DateTime, String, Integer, BigInteger, Text

from database.base import Base


# Chat Models

# class Room(Base):
#     id = Column(Integer, autoincrement=True, primary_key=True, index=True)
#     user_id = Column(BigInteger)


class Message(Base):
    __tablename__ = "chat_message"
    # id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    sender_id = Column(BigInteger)
    room_id = Column(BigInteger)
    text = Column(Text)
    date = Column(DateTime, default=datetime.datetime.utcnow)

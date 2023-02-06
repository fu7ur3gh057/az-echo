from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from database.base import Base


class Message(Base):
    __tablename__ = "chat_message"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user = Column(String)
    room_name = Column(String)
    text = Column(String)

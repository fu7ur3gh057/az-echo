from fastapi import FastAPI
import logging
from database.base import init_models, get_session
from sqlalchemy.ext.asyncio import AsyncSession
import json
from collections import defaultdict
from starlette.websockets import WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, Request, Depends, BackgroundTasks

from managers.chat_manager import ChatManager

app = FastAPI()

chat_broadcast = ChatManager()


@app.websocket('/ws/chat/{room_name}')
async def websocket_chat_endpoint(websocket: WebSocket, room_name,
                                  session: AsyncSession = Depends(get_session)):
    # Connecting
    await chat_broadcast.connect(websocket, room_name)
    try:
        while True:
            data = await websocket.receive_text()
            message_body = ''
    except WebSocketDisconnect as ex:  # Disconnecting
        print(ex)
        await chat_broadcast.remove(websocket, room_name)


@app.websocket('/ws/notifications')
async def websocket_notification_endpoint():
    pass

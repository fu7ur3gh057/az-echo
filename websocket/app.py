from fastapi import FastAPI
import logging

from fastapi.responses import HTMLResponse
from sqlalchemy.exc import IntegrityError

from config.config import settings
from database.base import init_models, get_session
from sqlalchemy.ext.asyncio import AsyncSession
import json
from collections import defaultdict
from starlette.websockets import WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, Request, Depends, BackgroundTasks
import aiohttp

from database.exceptions import DuplicatedEntryError
from database.services import chat_service
from managers.chat_manager import ChatManager
from database.base import get_session
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

chat_broadcast = ChatManager()


@app.get("/")
async def get():
    return HTMLResponse("""
        <html>
            <head>
                <title>FastAPI WebSockets with Django JWT example</title>
            </head>
            <body>
                <h1>FastAPI WebSockets with Django JWT example</h1>
                <p>Open the Web Console to see the WebSocket messages</p>
                <script>
                    var ws = new WebSocket("ws://0.0.0.0:8088/ws/chat/1?token=");
                    ws.onmessage = function(event) {
                        console.log("Received message", event.data);
                    };
                </script>
            </body>
        </html>
    """)


async def check_jwt(jwt_token: str):
    async with aiohttp.ClientSession() as aio_session:
        async with aio_session.get(f"{settings.DATABASE_URL}/api/v1/auth/jwt-verify/", headers={
            "Authorization": f"Bearer {jwt_token}"
        }) as response:
            if response.status == 200:
                return True
            else:
                return False


# NOTIFICATIONS ENDPOINT
@app.websocket('/ws/notifications')
async def websocket_notifications(websocket: WebSocket):
    jwt_token = websocket.query_params.get('token')
    if check_jwt(jwt_token):
        pass


# CHAT ENDPOINT
@app.websocket('/ws/chat/{room_id}')
async def websocket_chat(websocket: WebSocket, room_id, session: AsyncSession = Depends(get_session)):
    print('START CONNECTING')
    jwt_token = websocket.query_params.get('token')
    if await check_jwt(jwt_token):
        # Connecting
        await chat_broadcast.connect(websocket, room_id)
        try:
            while True:
                data = await websocket.receive_json()
                sender = int(data['sender'])
                text = data['text']
                try:
                    chat_service.add_message(session=session, text=text, sender_id=sender, room_id=room_id)
                    await session.commit()
                    room_members = (
                        chat_broadcast.get_members(room_id)
                        if chat_broadcast.get_members(room_id) is not None
                        else []
                    )
                    if websocket not in room_members:
                        print("SENDER NOT IN ROOM MEMBERS: RECONNECTING")
                        await chat_broadcast.connect(websocket, room_id)
                    await chat_broadcast.notify(data)
                except IntegrityError as ex:
                    await session.rollback()
                    raise DuplicatedEntryError("The message is already stored")
        except WebSocketDisconnect as ex:  # Disconnecting
            print(ex)
            await chat_broadcast.remove(websocket, room_id)
    else:
        raise WebSocketDisconnect("Unauthorized")


@app.websocket('/ws/notifications')
async def websocket_notification_endpoint():
    pass

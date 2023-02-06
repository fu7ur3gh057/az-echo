from collections import defaultdict
from fastapi import FastAPI, WebSocket, Request, Depends, BackgroundTasks


class ChatManager:
    def __init__(self):
        # Collection with lists of room name and websockets inside list
        self.connections: dict = defaultdict(dict)
        self.generator = self.get_notification_generator()

    # Get notification generator
    async def get_notification_generator(self):
        while True:
            message = yield
            msg = message['message']
            room_name = message['room_name']
            await self.notify(msg, room_name)

    # Get all members by room name
    def get_members(self, room_name):
        try:
            return self.connections[room_name]
        except Exception:
            return None

    # Pushing message to generator
    async def push(self, msg: str, room_name: str = None):
        message_body = {"message": msg, "room_name": room_name}
        await self.generator.asend(message_body)

    # Connecting | Add websocket to connections room name
    async def connect(self, websocket: WebSocket, room_name: str):
        # accepting websocket
        await websocket.accept()
        # if there are no any connections with room name
        if self.connections[room_name] == {} or len(self.connections[room_name]) == 0:
            self.connections[room_name] = []
        # add websocket to connections room name
        self.connections[room_name].append(websocket)
        print(f"CONNECTIONS : {self.connections[room_name]}")

    # Disconnecting | Remove websocket from connections room name
    async def remove(self, websocket: WebSocket, room_name: str):
        self.connections[room_name].remove(websocket)
        print(f'CONNECTION REMOVED: {self.connections[room_name]}')

    # Notify all members by room name
    async def notify(self, message: str, room_name: str):
        living_connections = []
        # while any connections with current room name
        while len(self.connections[room_name]) > 0:
            # pop websocket from connections
            websocket = self.connections[room_name].pop()
            # send text to websocket
            await websocket.send_text(message)
            # add to list for not to lose websockets
            living_connections.append(websocket)
        # returning back all websockets to connections
        self.connections[room_name] = living_connections

from enum import Enum

from fastapi import WebSocket

from backend.user import User


class ConnectionManager:
    class TYPES(Enum):
        CONNECTION = "CONNECTION"
        DISCONNECT = "DISCONNECT"
        USER = "USER"
        MESSAGE = "MESSAGE"
        PRESENTATION = "PRESENTATION"
        MAIN = "MAIN"

    main_sockets: dict[str, WebSocket]
    active_connections: dict[str, list[User]]

    def __init__(self):
        self.main_sockets = {}
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, session_id: str, user: User = None):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []

        if user:
            self.active_connections[session_id].append(user)
            return
        self.main_sockets[session_id] = websocket


    def disconnect(self, websocket: WebSocket, session_id: str):
        user = next((u for u in self.active_connections[session_id] if u.is_user(websocket)), None)

        if user:
            self.active_connections[session_id].remove(user)

    async def broadcast(self, session_id: str, message: str):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.websocket.send_text(message)

    async def send_to_main(self, message_obj: dict, session_id: str, type: TYPES = TYPES.MESSAGE):
        try:
            main_socket = self.main_sockets[session_id]
            await main_socket.send_json({
                "type": type.value,
                "data": message_obj
            })
        except:
            raise
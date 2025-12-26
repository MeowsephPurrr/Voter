from dataclasses import dataclass

from fastapi import WebSocket


@dataclass
class User:
    id: str
    websocket: WebSocket
    session_id: str
    name: str

    def is_user(self, websocket: WebSocket) -> bool:
        return websocket == self.websocket

    def as_dict(self):
        return {
            "userId": self.id,
            "name": self.name,
        }
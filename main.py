from logging import raiseExceptions

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.connection_manager import ConnectionManager
from backend.user import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where main.py is located
BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Mount the static directory (for JS/CSS)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

manager = ConnectionManager()


@app.get("/")
async def read_index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/questions/{session_id}")
async def read_index():
    return FileResponse(FRONTEND_DIR / "questions.html")


@app.get("/mobile/{session_id}/presentation")
async def get_mobile(session_id: str):
    return FileResponse(FRONTEND_DIR / "presentation.html")


@app.get("/mobile/{session_id}")
async def get_mobile(session_id: str):
    return FileResponse(FRONTEND_DIR / "mobile.html")


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket_handler(websocket, session_id, type=ConnectionManager.TYPES.MAIN)


@app.websocket("/ws/{session_id}/presentation")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket_handler(websocket, session_id, type=ConnectionManager.TYPES.PRESENTATION)


@app.websocket("/ws/{session_id}/{id}/{name}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, id: str, name: str):
    user = User(id=id, websocket=websocket, session_id=session_id, name=name)
    await websocket_handler(websocket, session_id, user=user)

@app.get("/api/data")
async def get_data():
    return {
        "url": "http://127.0.0.1:8000",
    }

async def websocket_handler(
        websocket: WebSocket,
        session_id: str,
        user: User = None,
        type: ConnectionManager.TYPES = None
):
    await manager.connect(websocket, session_id, user)
    try:
        match type:
            case ConnectionManager.TYPES.MAIN:
                await _main_connection(websocket, session_id)
            case ConnectionManager.TYPES.PRESENTATION:
                await _presentation_connection(websocket, session_id)
            case _:
                await _user_connection(websocket, user, session_id)

        await manager.connect(websocket, session_id, user=user)
    except WebSocketDisconnect:
        if type not in [ConnectionManager.TYPES.MAIN, ConnectionManager.TYPES.PRESENTATION]:
            message_obj = user.as_dict()
            await manager.send_to_main(message_obj, session_id=session_id, type=manager.TYPES.DISCONNECT)
        manager.disconnect(websocket, session_id)


async def _main_connection(websocket: WebSocket, session_id: str):
    await websocket.send_json({
        "type": manager.TYPES.USER.value,
        "data": [user.as_dict() for user in manager.active_connections[session_id]],
    })

    while True:
        data = await websocket.receive_text()
        await manager.broadcast(session_id, data)


async def _presentation_connection(websocket: WebSocket, session_id: str):
    while True:
        data = await websocket.receive_text()
        await manager.send_to_main({"message": data}, session_id=session_id, type=manager.TYPES.PRESENTATION)
        await manager.broadcast(session_id, data)


async def _user_connection(websocket: WebSocket, user: User, session_id: str):
    await manager.send_to_main(user.as_dict(), session_id=session_id, type=manager.TYPES.CONNECTION)
    while True:
        message = await websocket.receive_text()
        message_obj = user.as_dict()
        message_obj["message"] = message
        await manager.send_to_main(message_obj, session_id=session_id)


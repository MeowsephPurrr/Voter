from logging import raiseExceptions

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.connection_manager import ConnectionManager

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


@app.get("/mobile/{session_id}")
async def get_mobile(session_id: str):
    return FileResponse(FRONTEND_DIR / "mobile.html")


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket_handler(websocket, session_id)


@app.websocket("/ws/{session_id}/{id}/{name}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, id: str, name: str):
    await websocket_handler(websocket, session_id, id, name)


async def websocket_handler(websocket: WebSocket, session_id: str, id: str = None, name: str = None):
    user = await manager.connect(websocket, session_id, id, name)
    try:
        if user:
            await manager.send_to_main(user, "", manager.TYPES.CONNECTION)
            while True:
                message = await websocket.receive_text()
                await manager.send_to_main(user, message)
        else:
            await websocket.send_json({
                "type": manager.TYPES.USER.value,
                "data": [user.as_dict() for user in manager.active_connections[session_id]],
            })

            while True:
                data = await websocket.receive_text()
                await manager.broadcast(session_id, data)
    except WebSocketDisconnect:
        if user:
            await manager.send_to_main(user, "", manager.TYPES.DISCONNECT)
        manager.disconnect(websocket, session_id)


@app.get("/api/data")
async def get_data():
    return {
        "url": "http://127.0.0.1:8000",
    }

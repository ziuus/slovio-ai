from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
from core.loop import run

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    with open("static/index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Use "chat" event for standard responses
                response = await run(data, use_vision=False)
                await websocket.send_json({"type": "chat", "payload": {"text": response}})
            except Exception as e:
                await websocket.send_json({"type": "log", "payload": {"message": f"System Error: {str(e)}", "level": "error"}})
    except WebSocketDisconnect:
        pass

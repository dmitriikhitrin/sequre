from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
import json
app = FastAPI()

class WebSocketConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        if len(self.active_connections) > 2:
            return 500
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

mananger: WebSocketConnectionManager = WebSocketConnectionManager()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if await mananger.connect(websocket) == 500:
        raise HTTPException(status_code=500, details="Connection limit exceeded")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await mananger.broadcast(data)
    except WebSocketDisconnect:
        mananger.disconnect(websocket)
        await mananger.broadcast(json.dumps({"text": "aborted"}))

from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
from qiskit import QuantumCircuit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from math import pi
from qiskit import Aer, execute
import random


def binaryToDecimal(binary):
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

def createCircuit(numUsers, QECQubits, registers):
    users = QuantumRegister(numUsers, "user")
    ancillas = QuantumRegister(QECQubits, "ancilla")
    cr = ClassicalRegister(registers, 'c')
    qc = QuantumCircuit(users, ancillas, cr)
    return qc

numUsers = 3
QECQubits = 1
registers = 3
def initializeDialog(userIn):
    qc = createCircuit(numUsers, QECQubits, registers)
    qc.h(userIn)
    return qc

def enterDialog(userIn, userEn):
    qc = initializeDialog(userIn)
    qc.cnot(userIn, userEn)
    return qc

def closeDialog(qc, userIn, userEn):
    qc.reset(userIn)
    qc.reset(userEn)
    return qc

def errorX(qc, userIn, userEn):
    qc.rx(random.random()*pi/2, userIn) 
    qc.rx(random.random()*pi/2, userEn)
    return qc

def errorCorrection(qc, userIn, userEn, QECQubit):
    qc.cnot(userIn, QECQubit)
    qc.cnot(userEn, QECQubit)
    return qc

def getPrivateKeys(userIn, userEn, QECQubit, keyLength):
    qc = enterDialog(userIn, userEn)
    
    qc.barrier()
    qc = errorX(qc, userIn, userEn)
    qc.barrier()
    
    qc = errorCorrection(qc, userIn, userEn, QECQubit)
    qc.barrier()
    qc.measure([userIn, userEn, QECQubit], [0,1,2])
    
    lstIn = []
    lstEn = []
    counts = []
    
    
    while len(lstEn) <= keyLength:
        backend = Aer.get_backend('qasm_simulator')
        job_sim = execute(qc, backend, shots = 1)
        result = job_sim.result()
        count = result.get_counts(qc)
        counts.append(count)
        if (int(list(count.keys())[0][0]) == 0):
            lstIn.append(list(count.keys())[0][registers-userIn-1])
            lstEn.append(list(count.keys())[0][registers-userEn-1])

    
    if (len(lstIn) != 0 and len(lstEn) != 0):
        if lstIn[0] == 0:
            lstIn = lstIn[1:]
        if lstEn[0] == 0:
            lstEn = lstEn[1:]
        keyIn = binaryToDecimal(int("".join(lstIn)))
        keyEn = binaryToDecimal(int("".join(lstEn)))

    if keyIn != keyEn:
        return 0
    else:
        return keyIn

class WebSocketConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []
        self.token = 0
        self.sentTokenTimes: int = 0
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        if len(self.active_connections) > 2:
            return 500
        self.active_connections.append(ws)
        if len(self.active_connections) == 2:
            if self.token == 0:
                self.token = getPrivateKeys(0, 1, 3, 16)
            print(self.token)

    async def disconnect(self):
        for connection in self.active_connections:
            self.active_connections.remove(connection)

        for connection in self.active_connections:
            await connection.close()
        
        self.token = 0

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            if len(self.active_connections) == 2 and self.sentTokenTimes<2:
                # await connection.send_text(json.dumps({"token":str(self.token)}))
                await connection.send_text(json.dumps({"text":str(self.token)}))
                self.sentTokenTimes += 1
            else:
                await connection.send_text(message)

mananger: WebSocketConnectionManager = WebSocketConnectionManager()

    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    result = getPrivateKeys(0, 1, 3, 128)
    print(result)
    raise HTTPException(status_code=500, detail="Oops")

roomCreated:bool = False
roomJoined: bool = False

class RoomCreator(BaseModel):
    id: str

class RoomVisitor(BaseModel):
    id: str

@app.post("/create/room")
async def main(req: RoomCreator):
    print(req)
    if not roomCreated:
        roomCreated = True
        return {"message": "Room created. Waiting for your buddy to join."}
    else:
        raise HTTPException(status_code=500, detail="")

@app.get("/join/room")
async def join():
    if not roomCreated:
        return {"message": "Sorry, no room is created yet"}
    roomJoined = True
    return {"message": "You want to enter the room!"}



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await mananger.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await mananger.broadcast(data)
    except WebSocketDisconnect:
        await mananger.disconnect()


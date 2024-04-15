import websockets
import datetime
import json
import asyncio


CONNECTIONS = set()

PLAYERS = []
ROOMS = []

async def register(websocket):

    if websocket not in CONNECTIONS:
        greetings = await websocket.recv()
        print(f">>> {greetings}")
        CONNECTIONS.add(websocket)
        print(f'Number of connection: {len(CONNECTIONS)}')
    else:
        return

    
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)


async def register_player(websocket):
    global PLAYERS, CONNECTIONS, ROOMS

    if websocket not in CONNECTIONS:
        player = await websocket.recv()
        player = json.loads(player)
        player["websocket"] = websocket
        PLAYERS.append(player)
    else:
        return
    
    for pl in PLAYERS:
        print(pl)
    
    try:
        await websocket.wait_closed()
    finally:
        PLAYERS = filter(lambda pl: pl["websocket"] == websocket, PLAYERS)
        CONNECTIONS.remove(websocket)
        
    
async def handle_quizz():
    global ROOMS, PLAYERS
    

async def show_time():
    while True:
        message = datetime.datetime.now().isoformat() + "Z"
        websockets.broadcast(CONNECTIONS, message)
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(register_player, "localhost", 8001):
        await show_time()


if __name__ == "__main__":
    asyncio.run(main())

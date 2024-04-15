import websockets
import datetime
import random
import asyncio


CONNECTIONS = set()


async def register(websocket):

    if websocket not in CONNECTIONS:
        CONNECTIONS.add(websocket)
        print(f'Number of connection: {len(CONNECTIONS)}')
    else:
        return

    
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

    


async def show_time():
    while True:
        message = datetime.datetime.now().isoformat() + "Z"
        websockets.broadcast(CONNECTIONS, message)
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(register, "77.37.86.225", 8001):
        await show_time()


if __name__ == "__main__":
    asyncio.run(main())

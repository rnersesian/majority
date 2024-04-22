import websockets
import datetime
import json
import asyncio


CONNECTIONS = set()

QUESTIONS = [
    {
        "question": "Quelle est la couleur du cheval blanc d'Henri IV",
        "answers" : ["Blanc", "Jaune", "AYAAA"],
        "solution": 0
    },
    {
        "question": "En Chine, si t'as pas de bol, t'as pas de ...",
        "answers" : ["Crédit social", "Cheveux", "Riz"],
        "solution": 2
    },
    {
        "question": "Quelle est la hauteur de la tour Effeil",
        "answers" : ["900 courgettes", "3 Lebron James", "lela"],
        "solution": 0
    },
]

async def register(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event['type'] == 'init'

    CONNECTIONS.add(websocket)

    await start_quizz(websocket)

    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)


async def start_quizz(websocket):
    for question in QUESTIONS:
        event = {
            "type": "question",
            "question": {"label": question["question"], "answers": question['answers']}
        }
        await websocket.send(json.dumps(event))

        try:
            message = await websocket.recv()
            answer = json.loads(message)
            print(answer)
        except:
            return
        

async def main():
    async with websockets.serve(register, "localhost", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

import websockets
import datetime
import json
import asyncio


CONNECTIONS = set()

QUESTIONS = [
    {
        "label": "Quelle est la couleur du cheval blanc d'Henri IV",
        "answers" : ["Blanc", "Jaune", "AYAAA"],
        "solution": 0
    },
    {
        "label": "En Chine, si t'as pas de bol, t'as pas de ...",
        "answers" : ["Crédit social", "Cheveux", "Riz"],
        "solution": 2
    },
    {
        "label": "Quelle est la hauteur de la tour Effeil",
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
    score = 0
    for question in QUESTIONS:
        event = {
            "type": "question",
            "question": {"label": question["label"], "answers": question['answers']}
        }
        await websocket.send(json.dumps(event))

        try:
            message = await websocket.recv()
            message = json.loads(message)
            if message["type"] == "answer" and message["answer"] == question["answers"][question["solution"]]:
                score += 1
        except:
            return
        
    print(score)
        

async def main():
    async with websockets.serve(register, "localhost", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

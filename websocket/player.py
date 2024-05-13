from ws_event import WsEvent, Events
import secrets
from utils import log
from typing import Any

class Player():

    def __init__(self, websocket, player_name) -> None:
        self.websocket = websocket
        self.name = player_name
        self.id = "player_" + secrets.token_urlsafe(12)
        self.joined_room: Any = None


    async def send(self, event_type: str, data: dict):
        try:
            event = WsEvent(event_type=event_type, data=data).to_str
            await self.websocket.send(event)
            log(f"Package sent to player '{self.name}' :\n{event}")
        except Exception as e:
            print(e)
            print(f"ERROR : Could not send event to player :\n\t{self}")


    async def send_error(self, message: str):
        try:
            event = WsEvent(event_type=Events.ERROR, data={"message": message}).to_str
            await self.websocket.send(event)
            log(f"Error sent to player '{self.name}' :\n{message}")
        except:
            print(f"ERROR : Could not send error event to player :\n\t{self}")


    async def recv(self) -> WsEvent | None:
        try:
            message = await self.websocket.recv()
            event = WsEvent.from_json(message)

            assert event is not None
            log(f"Package recieved from player '{self.name}' :\n{event.to_str}")
            return event
        except:
            print(f"Coulnd't recieve event from player '{self.name}'")


    def __repr__(self) -> str:
        return f'<Player "{self.name}" - ID : {self.id}>'

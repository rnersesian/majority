from ws_event import WsEvent, Events
import secrets

class Player():

    def __init__(self, websocket, player_name) -> None:
        self.websocket = websocket
        self.name = player_name
        self.id = secrets.token_urlsafe(12)


    async def send(self, event_type: str, data: dict):
        try:
            event = WsEvent(event_type=event_type, data=data).to_str
            await self.websocket.send(event)
        except:
            print(f"ERROR : Could not send event to player :\n\t{self}")


    async def send_error(self, message: str):
        try:
            event = WsEvent(event_type=Events.ERROR, data={"message": message}).to_str
            await self.websocket.send(event)
        except:
            print(f"ERROR : Could not send error event to player :\n\t{self}")


    async def recv(self) -> WsEvent:
        try:
            message = await self.websocket.recv()
            return WsEvent.from_json(message)
        except:
            print(f"Coulnd't recieve event from player '{self.name}'")


    def __repr__(self) -> str:
        return f'<Player "{self.name}" - ID : {self.id}>'
import asyncio, websockets, secrets
from ws_event import WsEvent, send_error, send_event, Events


class WebSocketServer():

    def __init__(self, host="localhost", port=8001) -> None:
        self.rooms = []
        self.connected = []
        self.host = host
        self.port = port


    def remove_connected(self, player_name):
        """Remove user from connected players
        
        Keyword arguments:
        player_name -- Name of the player (unique)
        Return: None
        """
        self.connected = list(filter(lambda x: x["player_name"] != player_name, self.connected))


    def add_connected(self, player_name, websocket):
        """Add user to the list of connected players
        
        Keyword arguments:
        player_name -- Name of the player
        websocket   -- Websocket to communicate with the said player
        Return: None
        """
        
        self.connected.append({
            "player_name": player_name,
            "websocket": websocket
        })


    def get_player_websocket(self, player_name):
        """ Get a websocket from a unique player_name
        
        Keyword arguments:
        player_name -- name of a player (unique)
        Return: Websocket
        """ 
        return list(filter(lambda x: x['player_name'] == player_name, self.connected))[0]['websocket']


    async def show_rooms(self, websocket, player_name):
        """Send a list of available rooms to the user
        
        Keyword arguments:
        websocket -- Websocket to send rooms to
        Return: None
        """
        await websocket.send(WsEvent("show_rooms", {"rooms": self.rooms}).to_str)

        # Listening to client
        async for message in websocket:
            try:
                event = WsEvent.from_json(message)

                if event.type == Events.CREATE_ROOM:
                    await send_event(websocket, Events.MESSAGE,{'message': 'You are creating a room'})

                elif event.type == Events.JOIN_ROOM:
                    await send_event(websocket, Events.MESSAGE, {'message': 'You are joining a room'})

                print(self.get_player_websocket(player_name))

            except Exception as e:
                print(e)
                await send_error(websocket, "Invalid Action")


    async def register(self, websocket):
        """Handle initial connection from user
        
        Keyword arguments:
        websocket -- A Websocket
        Return: None
        """
        async for message in websocket:
            try:
                event = WsEvent.from_json(message)
                player_name = event["data"]["player_name"]
                self.connected.append({
                    "player_name": player_name,
                    "websocket": websocket
                })
            except Exception as e:
                print("CONNECTION ERROR :", e)
                await send_error(websocket, 'Something went wrong')
                continue
            
            if event.type == Events.CONNECT:
                await self.show_rooms(websocket, player_name)
                self.remove_connected(player_name)

            else:
                await send_error(websocket, 'Recieved unhandled event type')

    
    async def __run(self):
        async with websockets.serve(self.register, self.host, self.port):
            await asyncio.Future()
    
    
    def start(self):
        asyncio.run(self.__run())
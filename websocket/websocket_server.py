import asyncio, websockets, secrets, json
from typing import List, Type
from ws_event import WsEvent, send_error, Events
from player import Player



class WebSocketServer():

    def __init__(self, host="localhost", port=8001) -> None:
        self.rooms = []
        self.connected: List[Player] = []
        self.host = host
        self.port = port


    def remove_connected(self, player: Player):
        """Remove user from connected players
        
        Keyword arguments:
        player: Player -- player object
        Return: None
        """
        print(f">>> Player disconnected : {player.name}")
        self.connected = list(filter(lambda x: x.id != player.id, self.connected))


    def add_connected(self, player: Player):
        """Add user to the list of connected players
        
        Keyword arguments:
        player: Player -- player object
        Return: None
        """
        print(f">>> New player connected : {player.name}")
        self.connected.append(player)

    
    def broadcast(self, player_list: List[Player], event: WsEvent):
        """ Broadcast an event to a list of players
        
        Keyword arguments:
        player_list : Player    -- List of Player to broadast to
        event       : WsEvent   -- Event to broadcast
        Return: None
        """
        
        for player in player_list:
            asyncio.create_task(player.send(event))


    async def show_rooms(self, player: Player):
        """Send a list of available rooms to the user
        
        Keyword arguments:
        websocket -- Websocket to send rooms to
        Return: None
        """
        await player.send(Events.SHOW_ROOMS, {"rooms": self.rooms})

        # Listening to client
        async for message in player.websocket:
            try:
                event = WsEvent.from_json(message)

                if event.type == Events.CREATE_ROOM:
                    await player.send(Events.MESSAGE, {'message': 'You are creating a room'})

                elif event.type == Events.JOIN_ROOM:
                    await player.send(Events.MESSAGE, {'message': 'You are joining a room'})

            except Exception as e:
                print(e)
                await player.send_error("Invalid Action")


    async def register(self, websocket):
        """Handle initial connection from user
        
        Keyword arguments:
        websocket -- A Websocket
        Return: None
        """
        async for message in websocket:
            try:
                event = WsEvent.from_json(message)

            except Exception as e:
                print("CONNECTION ERROR :", e)
                await send_error(websocket, 'Something went wrong')
                continue
            
            if event.type == Events.CONNECT:
                player_name = event["data"]["player_name"]
                player = Player(websocket, player_name)
                self.add_connected(player)

                await self.show_rooms(player)

                await player.websocket.wait_closed()
                self.remove_connected(player)

            else:
                await send_error(websocket, 'Recieved unhandled event type')

    
    async def __run(self):
        async with websockets.serve(self.register, self.host, self.port):
            await asyncio.Future()
    
    
    def start(self):
        asyncio.run(self.__run())

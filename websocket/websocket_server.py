import asyncio, websockets
from typing import List
from ws_event import WsEvent, send_error, Events
from player import Player
from room import Room



class WebSocketServer():

    def __init__(self, host="localhost", port=8001) -> None:
        self.rooms: List[Room] = []
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


    async def manage_room(self, room: Room, player: Player):
        async for message in player.websocket:
            try:
                event = WsEvent.from_json(message)
            except:
                print(">>> Error with the json body")
                continue
            
            if event.type == Events.CHAT_MESSAGE:
                room.broadcast(event)
        

    async def create_room(self, player: Player):
        room = Room(player)
        self.rooms.append(room)
        await player.send(Events.CREATE_ROOM, {
            "message": "Room created",
            "room_name": room.name,
            "room_id": room.id
        })
        await self.manage_room(room, player)

    
    async def join_room(self, player: Player, event: WsEvent):
        """ Make a player join a room from with its ID
        
        Keyword arguments:
        player : Player -- player object
        room_id : str   -- id of the room
        Return: None
        """
        try: # Check if room_id exist in data
            room_id = event.data["room_id"]
        except:
            print(f">>> Event sent from player '{player.name}' is invalid :\n event")
            await player.send_error('Sent event websocket package is invalid')
            return
        
        try: # Check if room exists
            room: Room = list(filter(lambda r: r.id == room_id, self.rooms))[0]
        except IndexError:
            await player.send_error(f"Room with ID {room_id} does not exist")
            return

        await room.add_player(player)
        await self.manage_room(room, player)


    async def show_rooms(self, player: Player):
        """Send a list of available rooms to the user
        
        Keyword arguments:
        websocket -- Websocket to send rooms to
        Return: None
        """
        await player.send(Events.SHOW_ROOMS, {"rooms": self.room_list_json})

        # Listening to client
        async for message in player.websocket:
            try:
                event = WsEvent.from_json(message)

                if event.type == Events.CREATE_ROOM:
                    await self.create_room(player)
                    continue

                elif event.type == Events.JOIN_ROOM:
                    # await player.send(Events.MESSAGE, {'message': 'You are joining a room'})
                    await self.join_room(player, event)
                    continue

            except Exception as e:
                print(e)
                await player.send_error("Invalid Action")


    async def handle_disconnect(self, player):
        # Check if player has joined any room
        self.remove_connected(player)
        joined_rooms = list(filter(lambda r: player in r.player_list, self.rooms))

        # Remove player from all joined rooms
        for room in joined_rooms:
            print(f">>> Removing player '{player.name}' from room '{room.name}'")
            await room.remove_player(player)
            if room.player_list.__len__() == 0:
                self.rooms.remove(room)
        
        print(f">>> Number of opened rooms : {self.rooms.__len__()}")

        del player
        


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
                await self.handle_disconnect(player)

            if event.type == Events.SHOW_ROOMS:
                player.send(Events.SHOW_ROOMS, {"rooms": self.room_list_json})

            else:
                await send_error(websocket, 'Recieved unhandled event type')

    
    async def __run(self):
        async with websockets.serve(self.register, self.host, self.port):
            await asyncio.Future()
    
    
    def start(self):
        asyncio.run(self.__run())


    @property
    def room_list_json(self):
        return [{
            "room_name": room.name,
            "room_id": room.id,
            "room_owner": room.owner.name
        } for room in self.rooms]
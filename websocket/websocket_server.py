import asyncio, websockets
from typing import List
from ws_event import WsEvent, send_error, Events
from player import Player
from room import Room
from utils import log



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
        log(f"Player disconnected : '{player.name}'")
        self.connected = list(filter(lambda x: x.id != player.id, self.connected))


    def add_connected(self, player: Player):
        """Add user to the list of connected players
        
        Keyword arguments:
        player: Player -- player object
        Return: None
        """
        log(f"Player connected : '{player.name}'")
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


    async def handle_disconnect(self, player):
        # Check if player has joined any room
        self.remove_connected(player)
        joined_rooms = list(filter(lambda r: player in r.player_list, self.rooms))

        # Remove player from all joined rooms
        for room in joined_rooms:
            log(f"Removing player '{player.name}' from room '{room.name}'")
            await room.remove_player(player)
            if room.player_list.__len__() == 0:
                self.rooms.remove(room)

        del player

    
    async def handle_events(self, player: Player):
        """ Handle events recieved by web clients
        
        Keyword arguments:
        websocket       -- websocket to communicate with web clients
        player: Player  -- player's identity
        Return: None
        """
        async for message in player.websocket:
            try:
                event = WsEvent.from_json(message)
            except:
                await player.send_error("Could not read event")

            try:
                if event.type == Events.SHOW_ROOMS:
                    await self.handle_get_room_list(player)
                    continue

                elif event.type == Events.CREATE_ROOM:
                    await self.handle_create_room(player, event.data)
                    continue

                elif event.type == Events.JOIN_ROOM:
                    await self.handle_join_room(player, event.data)
                    continue

                elif event.type == Events.REFRESH_PLAYER_LIST:
                    await self.handle_refresh_player_list(player)
                    continue

                elif event.type == Events.CHAT_MESSAGE:
                    await self.handle_chat_message(player, event.data)
                    continue



            except InvalidActionException:
                log(f"Recieved invalid action from player <{player.name}> :\n", event)
                await player.send_error("Invalid error")
            except Exception as e:
                log(f"Something went wrong : ", e)
                await self.handle_disconnect(player)
                return
            
        await self.handle_disconnect(player)
            

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
                await self.handle_connect(player)

    
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
            "room_owner": room.owner.name if room.owner is not None else ""
        } for room in self.rooms]
    

    ###################
    # Events Handlers #
    ###################

    async def handle_connect(self, player: Player):
        """Handle initial connection from player"""
        self.add_connected(player)
        await player.send(Events.CONNECT_SUCCESS, {})
        await self.handle_events(player)


    async def handle_get_room_list(self, player: Player):
        """Send list of room to a web client"""
        print(self.room_list_json)
        await player.send(Events.SHOW_ROOMS, {"rooms": self.room_list_json})


    async def handle_create_room(self, player: Player, data: dict):
        """Create a new room"""
        try:
            room_name = data["room_name"] if "room_name" in data.keys() else None
            new_room = Room(player, room_name)
            await player.send(Events.CREATE_ROOM, {
                "room_name": new_room.name,
                "room_id": new_room.id,
                "message": f"Room [{new_room.name}] is created"
            })
            self.rooms.append(new_room)

        except:
            log("ERROR : Could not create room")
            await player.send_error("Could not create room")
    

    async def handle_join_room(self, player: Player, data: dict):
        """Join existing room"""
        try:
            room_id = data["room_id"]
            room: Room = list(filter(lambda r: r.id == room_id, self.rooms))[0]
            await room.add_player(player)
            player.joined_room = room

        except KeyError:
            log("ERROR : Missing room_id field event data")
        except IndexError:
            await player.send_error(f"Room with ID {room_id} does not exist")
        except:
            log("ERROR : Could not join room")


    async def handle_refresh_player_list(self, player: Player):
        """Refresh list of player in a room"""
        try:
            if player.joined_room == None: raise Exception

            await player.send(Events.REFRESH_PLAYER_LIST,
                              {"player_list": player.joined_room.player_list_json})
            
        except:
            log(f"ERROR: Could not refresh player list for player <{player.name}>")


    async def handle_chat_message(self, player: Player, data: dict):
        """Send a message from a player to its room"""
        try:
            if player.joined_room == None: raise Exception

            if "message" in data.keys():
                player.joined_room.broadcast(WsEvent(Events.CHAT_MESSAGE, data))
            else:
                raise KeyError
            
        except KeyError:
            log("ERROR : Missing message field event data")
        except:
            log(f"Error when sending a message by player <{player.name}>")
    



#
# Exceptions
#

class InvalidActionException(Exception):
    pass
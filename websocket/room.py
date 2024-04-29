from player import Player
from ws_event import WsEvent, Events
from typing import List
import secrets, asyncio
from utils import log


class Room():

    def __init__(self, player: Player, room_name=None) -> None:
        self.player_list: List[Player] = []
        # self.player_list.append(player)
        self.owner = None
        self.name = room_name if room_name is not None else player.name + "'s room"
        self.id = "room_" + secrets.token_urlsafe(12)


    async def add_player(self, player: Player) -> None:
        log(f"Adding player '{player.name}' to room '{self.name}, Current players :'")
        if self.player_list.__len__() == 0: # Making the added player Owner if room is empty
            self.owner = player
        try:
            self.player_list.append(player)
            for player_name in [pl.name for pl in self.player_list]:
                print(f"\t- {player_name}")
            await self.broadcast(
                WsEvent(Events.REFRESH_PLAYER_LIST, {"player_list": self.player_list_json})
            )
        except Exception as e:
            log("ADD PLAYER ERROR :\n", e)
            print(player)

    
    async def remove_player(self, player: Player) -> None:
        replaceOwner = True if player == self.owner and self.player_list.__len__() > 1 else False
        self.player_list = list(filter(lambda x: x.id != player.id, self.player_list))

        if replaceOwner:
            self.owner = self.player_list[0]

        if self.player_list.__len__() > 0: # If owner is replaced then there are still players in the room
            await self.broadcast(
                WsEvent(Events.REFRESH_PLAYER_LIST,{"player_list": self.player_list_json})
            )


    async def broadcast(self, event: WsEvent):
        try:
            for player in self.player_list:
                asyncio.create_task(player.send(event.type, event.data))
        except Exception as e:
            log("BROADCAST ERROR :\n", e)


    @property
    def player_list_json(self):
        return [{
            "player_name": player.name,
            "player_id": player.id
        } for player in self.player_list]
    

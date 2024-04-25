from player import Player
from ws_event import WsEvent, Events
from typing import List
import secrets, asyncio


class Room():

    def __init__(self, player: Player, room_name=None) -> None:
        self.player_list: List[Player] = []
        self.player_list.append(player)
        self.owner = player
        self.name = room_name if room_name is not None else player.name + "'s room"
        self.id = "room_" + secrets.token_urlsafe(12)


    async def add_player(self, player: Player) -> None:
        print(f">>> Adding player '{player.name}' to room '{self.name}'")
        try:
            self.player_list.append(player)
            await self.broadcast(
                WsEvent(Events.REFRESH_PLAYER_LIST, {"player_list", self.player_list_json})
            )
        except Exception as e:
            print(">>> ADD PLAYER ERROR :\n", e)
            print(player)

    
    async def remove_player(self, player: Player) -> None:
        self.player_list = list(filter(lambda x: x.id != player.id, self.player_list))
        if self.player_list > 0:
            print(self.player_list_json)
            await self.broadcast(
                # TODO : fix player list broadcast
                WsEvent(Events.REFRESH_PLAYER_LIST,{"player_list", self.player_list_json})
            )



    async def broadcast(self, event: WsEvent):
        try:
            for player in self.player_list:
                asyncio.create_task(player.send(event))
        except Exception as e:
            print(">>> BROADCAST ERROR :\n", e)

    @property
    def player_list_json(self):
        return [{
            "player_name": player.name,
            "player_id": player.id
        } for player in self.player_list]
    


    
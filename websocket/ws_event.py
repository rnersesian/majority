import json

class WsEvent(dict):
    def __init__(self, event_type, data=None):
        try:
            self.update({
                "type": event_type,
                "data": data
            })
        except KeyError as e:
            print(f'ERROR: Missing type or data from WsEvent Object\n>>> {e}')

    @property
    def type(self):
        return self.__getitem__('type')

    @property
    def data(self):
        return self.__getitem__('data')


    @classmethod
    def from_json(self, json_data):
        
        # Ensure json_data is not a string decoded JSON
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
            
        try:
            data = json_data["data"] if "data" in json_data.keys() else None
            return WsEvent(json_data["type"], data)
        except KeyError as e:
            print(f'ERROR: Missing type or data from WsEvent Object\n>>> {e}')


    @property
    def to_str(self):
        return json.dumps(self)
    
    
class JSONParsingException(Exception):
    pass
    

async def send_error(websocket, message):
    event = WsEvent("error", {'message': message}).to_str
    await websocket.send(event)


async def send_event(websocket, event_type, data):
    await websocket.send(WsEvent(
        event_type=event_type,
        data=data
    ).to_str)


# List of events
class Events():
    CONNECT         = "connect"
    MESSAGE         = "message"
    SHOW_ROOMS      = "show_rooms"
    CREATE_ROOM     = "create_room"
    JOIN_ROOM       = "join_room"
    SEND_QUESTIONS  = "send_questions"
    SEND_ANSWER     = "send_answer"
    SEND_SCORE      = "send_score"
    ERROR           = "error"
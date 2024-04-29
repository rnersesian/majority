export async function sendRequests(websocket, event_type, data)
{
    websocket.send(JSON.stringify({
        "type": event_type,
        "data" : data
    }))
}


export let WsEvents = {
    CONNECT             : "connect",
    CONNECT_SUCCESS     : "connect_success",
    MESSAGE             : "message",
    SHOW_ROOMS          : "show_rooms",
    CREATE_ROOM         : "create_room",
    DELETE_ROOM         : "delete_room",
    JOIN_ROOM           : "join_room",
    SEND_QUESTIONS      : "send_questions",
    SEND_ANSWER         : "send_answer",
    SEND_SCORE          : "send_score",
    ERROR               : "error",
    CHAT_MESSAGE        : "chat_message",
    REFRESH_PLAYER_LIST : "refresh_player_list"
}



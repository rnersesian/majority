import React, { useEffect, useRef, useState } from "react"
import {useLocation} from 'react-router-dom';
import InputForm from "../components/input_form";
import InputText from "../components/input_text";
import { sendRequests } from "../ws_requests";
import { WsEvents } from "../ws_requests";


const PlayRoomPage = () => {

    const location = useLocation();
    const [username, setUsername] = useState(location.state !== null && location.state.username ? location.state.username : "")
    const [connected, setConnected] = useState(username !== "")
    const socketRef = useRef(null)
    const urlParams = new URLSearchParams(window.location.search)
    const room_id = urlParams.get("join")
    console.log(room_id)

    const join = () => {
        if (username !== "")
        {
            setConnected(true)
        } else {
            alert("Please enter a username")
        }
    }

    useEffect(() => {
        if (connected)
        {
            socketRef.current = new WebSocket(process.env.REACT_APP_WEBSOCKET_ADDRESS)

            socketRef.current.onopen = async () => {
                console.log('Website is connected to websocket', process.env.REACT_APP_WEBSOCKET_ADDRESS)
                await sendRequests(socketRef.current, WsEvents.CONNECT, {"player_name": username})
            }

            socketRef.current.addEventListener("message", (ws_event) => {
                let event = JSON.parse(ws_event.data)
                switch (event.type)
                {
                    case WsEvents.CONNECT_SUCCESS:
                        console.log("Connected to room !")
                        sendRequests(socketRef.current, WsEvents.JOIN_ROOM, {room_id: room_id})
                        break

                    case WsEvents.REFRESH_PLAYER_LIST:
                        console.log(event.data)
                        break
                    
                    default:
                        console.error("Recieved unhandled event",event.type)
                }
            })
        }
    }, [connected])


    if (!connected)
    {
        return (
            <div className="main-content">
                <InputForm title="Login">
                    <InputText type="text" label="username" id="username" value={username}
                    onChange={(event) => {setUsername(event.target.value)}}/>
                    
                    <button className="submit-button" onClick={join}>Submit</button>
                </InputForm>
            </div>
            
        )
    }

    return(
        <div>
            {/* {location.state.username || ""} */}
            <h1>{username}</h1>
            hey
        </div>
    )
}

export default PlayRoomPage
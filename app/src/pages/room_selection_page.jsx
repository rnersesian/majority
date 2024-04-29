import React, { useEffect, useRef, useState } from "react"
import InputForm from "../components/input_form"
import InputText from "../components/input_text"
import { WsEvents, sendRequests} from "../ws_requests"
import { useNavigate } from "react-router-dom"


const RoomSelectPage = () =>
{
    const [username, setUsername] = useState('')
    const [connected, setConnected] = useState(false)
    const [rooms, setRooms] = useState([])
    const [roomName, setRoomName] = useState("")
    
    const socketRef = useRef(null)
    const navigate = useNavigate()


    // Managing all Websocket event types
    const setup_websocket = () => {
        let websocket = new WebSocket(process.env.REACT_APP_WEBSOCKET_ADDRESS)

        websocket.onopen = async () => {
            console.log('Website is connected to websocket', process.env.REACT_APP_WEBSOCKET_ADDRESS)
            await sendRequests(websocket, WsEvents.CONNECT, {"player_name": username})
        }

        websocket.addEventListener("message", (ws_event) => {
            let event = JSON.parse(ws_event.data)
            switch (event.type)
            {
                case WsEvents.SHOW_ROOMS:
                    setRooms(event.data.rooms)
                    break

                case WsEvents.CREATE_ROOM:
                    console.log(event.data)
                    socketRef.current.close()
                    navigate("/room?join=" + event.data.room_id, {state: {"username": username}})
                    break

                case WsEvents.CONNECT_SUCCESS:
                    sendRequests(socketRef.current, WsEvents.SHOW_ROOMS, {})
                    break
                
                
                default:
                    console.error("Recieved unhandled event",event.type)
            }
        })

        return websocket
    }


    // Make sure username is not empty before connecting to the server
    const join = () => {
        if (username !== "")
        {
            setConnected(true)
            if (socketRef.current == null) socketRef.current = setup_websocket()
        } else {
            alert("Please enter a username")
        }
    }

    // Return username form if not connected already
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

    return (
        <div className="content_center">
            <h3>User : {username}</h3>
            <div>
                <InputText type="text" label="Room Name" id="room_name" value={roomName}
                onChange={(event) => {setRoomName(event.target.value)}} />
                <button className="submit-button" onClick={() =>{
                    sendRequests(socketRef.current, WsEvents.CREATE_ROOM, {"room_name": roomName})
                }}>Create Room</button>
            </div>
            <h2>Rooms</h2>
            {rooms.length === 0 ?
                <div>No Available room</div> :
                <table className="room-list">
                    <tr>
                        <th>Owner</th>
                        <th>Room Name</th>
                        <th>Join</th>
                    </tr>
                    {rooms.map(r => {return <tr>
                        <td>{r.room_owner}</td>
                        <td>{r.room_name}</td>
                        <td><button onClick={() => {
                            socketRef.current.close()
                            navigate("/room?join=" + r.room_id, {state: {"username": username}})
                        }}>Join</button></td>
                    </tr>})}
                </table>
            }

                <button className="submit-button" onClick={() =>{
                    sendRequests(socketRef.current, WsEvents.SHOW_ROOMS, {})
                }}>Refresh</button>
        </div>
    )

    
}
export default RoomSelectPage
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
    const [players, setPlayers] = useState([])
    const [message, setMessage] = useState("")

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
                        console.log("Refreshing player list")
                        setPlayers(event.data.player_list)
                        break

                    case WsEvents.ERROR:
                        alert(event.data.message || "")
                        window.location.href = "/lobbies"
                    
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
    console.log(players)
    return(
        <div className="lobby-page">
            <div className="left-panel">
                <div id="player-list">
                    {
                        players.length > 0 &&
                        players.map(pl => {
                            return(
                                <div>{pl.player_name}</div>
                            )
                        })
                    }
                </div>
            </div>
            <div className="game-panel">
                <div className="top-side">
                <div className="chat-box">
                    {messages.map(message => {
                        return (
                        <div className="message">
                            <div className="user">{message.username}</div>
                            <div className="content">{message.content}</div>
                        </div>
                        )
                    })}
                </div>
                </div>
                <div className="bottom-side" style={{alignItems: "center", flexDirection: "row", justifyContent: "space-between"}}>
                    <textarea value={message} name="" id="" cols="1" style={{width: "90%", height: "20px", float: "left", marginLeft: "20px", resize: "none", border: "none", backgroundColor: "lightgrey"}}
                    onChange={(event) => alert(event.target.value)}></textarea>
                    <button  style={{float: "right", marginRight: "20px"}}>Send</button>
                </div>
            </div>
        </div>
    )
}

export default PlayRoomPage


const messages = [
    {
      username: "Alice",
      content: "Hey there! How's it going?"
    },
    {
      username: "Bob",
      content: "Not bad, just working on some code."
    },
    {
      username: "Charlie",
      content: "Anyone up for a game of chess?"
    },
    {
      username: "David",
      content: "I'm down for chess!"
    },
    {
      username: "Eve",
      content: "What's everyone's plans for the weekend?"
    },
    {
      username: "Frank",
      content: "I'm thinking of going hiking."
    },
    {
      username: "Grace",
      content: "I'll join you, Frank. Hiking sounds fun!"
    },
    {
      username: "Hannah",
      content: "Count me in too! I need some fresh air."
    },
    {
      username: "Isaac",
      content: "I'm stuck with this bug. Can anyone help?"
    },
    {
      username: "Jack",
      content: "Sure, Isaac. What seems to be the problem?"
    },
    {
      username: "Kelly",
      content: "Just finished a great book, any recommendations?"
    },
    {
      username: "Liam",
      content: "I'm working on a new project, it's pretty exciting!"
    },
    {
      username: "Mia",
      content: "Does anyone want to grab coffee later?"
    },
    {
      username: "Nora",
      content: "I need advice on choosing a new laptop, any suggestions?"
    },
    {
      username: "Oliver",
      content: "Hey everyone, what's the latest gossip?"
    },
    {
      username: "Bob",
      content: "Not bad, just working on some code."
    },
    {
      username: "Charlie",
      content: "Anyone up for a game of chess?"
    },
    {
      username: "David",
      content: "I'm down for chess!"
    },
    {
      username: "Eve",
      content: "What's everyone's plans for the weekend?"
    },
    {
      username: "Frank",
      content: "I'm thinking of going hiking."
    },
    {
      username: "Grace",
      content: "I'll join you, Frank. Hiking sounds fun!"
    },
    {
      username: "Hannah",
      content: "Count me in too! I need some fresh air."
    },
    {
      username: "Isaac",
      content: "I'm stuck with this bug. Can anyone help?"
    },
    {
      username: "Jack",
      content: "Sure, Isaac. What seems to be the problem?"
    },
    {
      username: "Kelly",
      content: "Just finished a great book, any recommendations?"
    },
    {
      username: "Liam",
      content: "I'm working on a new project, it's pretty exciting!"
    },
    {
      username: "Mia",
      content: "Does anyone want to grab coffee later?"
    },
    {
      username: "Nora",
      content: "I need advice on choosing a new laptop, any suggestions?"
    },
    {
      username: "Oliver",
      content: "Hey everyone, what's the latest gossip?"
    },
    {
      username: "Bob",
      content: "Not bad, just working on some code."
    },
    {
      username: "Charlie",
      content: "Anyone up for a game of chess?"
    },
    {
      username: "David",
      content: "I'm down for chess!"
    },
    {
      username: "Eve",
      content: "What's everyone's plans for the weekend?"
    },
    {
      username: "Frank",
      content: "I'm thinking of going hiking."
    },
    {
      username: "Grace",
      content: "I'll join you, Frank. Hiking sounds fun!"
    },
    {
      username: "Hannah",
      content: "Count me in too! I need some fresh air."
    },
    {
      username: "Isaac",
      content: "I'm stuck with this bug. Can anyone help?"
    },
    {
      username: "Jack",
      content: "Sure, Isaac. What seems to be the problem?"
    },
    {
      username: "Kelly",
      content: "Just finished a great book, any recommendations?"
    },
    {
      username: "Liam",
      content: "I'm working on a new project, it's pretty exciting!"
    },
    {
      username: "Mia",
      content: "Does anyone want to grab coffee later?"
    },
    {
      username: "Nora",
      content: "I need advice on choosing a new laptop, any suggestions?"
    },
    {
      username: "Oliver",
      content: "Hey everyone, what's the latest gossip?"
    }
  ];
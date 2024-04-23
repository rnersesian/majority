import React, { useEffect, useRef, useState } from "react"
import InputForm from "../components/input_form"
import InputText from "../components/input_text"

const MultiQuizzPage = () =>
{
    const [username, setUsername] = useState('')
    const [joined, setJoined] = useState(false)
    
    const socketRef = useRef(null)

    
    const join = () => {
        if (username != "")
        {
            setJoined(true)
            if (socketRef.current == null)
            {
                socketRef.current = new WebSocket(process.env.REACT_APP_WEBSOCKET_ADDRESS)
                socketRef.current.onopen = async () => {
                    console.log('Website is connected to websocket', process.env.REACT_APP_WEBSOCKET_ADDRESS)
                    await socketRef.current.send(JSON.stringify({
                        "type": "connect",
                        "player_name": username
                    }))
                }
            }


        } else {
            alert("Please enter a username")
        }
    }

    if (!joined)
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
    } else
    {
        return (
            <div>Hello {username}</div>
        )
    }

    
}

export default MultiQuizzPage
import React, { useEffect, useState, useRef } from "react"
import {io} from "socket.io-client"

const truc = true

const MainPage = () => {

  const [time, setTime] = useState("")
  const socketRef = useRef(null);

  useEffect(() => {

    // Establish WebSocket connection if not already connected
      socketRef.current = new WebSocket(process.env.REACT_APP_WEBSOCKET_ADDRESS);

      // WebSocket event listeners
      socketRef.current.onopen = () => {
        console.log('WebSocket connected');
        // Send "hello" message once connected
        socketRef.current.send(JSON.stringify({
          "player_id": "test",
          "player_name": "Robert"
        }));
      };

      socketRef.current.onmessage = (event) => {
        setTime(event.data);
      };

      socketRef.current.onclose = () => {
        socketRef.current.send("Goodbye !");
        console.log('WebSocket disconnected');
      };
    
  }, []); // Only runs once when the component mounts

  return (
  <>
    <h1>Main Page</h1>
    <h3>{time}</h3>
  </>
  )
}

export default MainPage

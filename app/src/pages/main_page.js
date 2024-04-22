import React, { useEffect, useState, useRef, useTransition } from "react"
import {io} from "socket.io-client"

const truc = true

const send_answer = (websocket, answer) =>
{
  websocket.send(JSON.stringify({
    "type": "answer",
    "answer": answer
  }))
}

const MainPage = () => {

  // const [time, setTime] = useState("")
  const [question, setQuestion] = useState(null)
  const socketRef = useRef(null);

  useEffect(() => {

    // Establish WebSocket connection if not already connected
      socketRef.current = new WebSocket(process.env.REACT_APP_WEBSOCKET_ADDRESS);

      // WebSocket event listeners
      socketRef.current.onopen = () => {
        console.log('WebSocket connected');
        // Send "hello" message once connected
        socketRef.current.send(JSON.stringify({
          "type": "init",
          "player_name": "Robert"
        }));
      };

      socketRef.current.onmessage = (event) => {
        let data = JSON.parse(event.data)
        switch(data.type)
        {
          case "question":
            setQuestion(data.question)
            break;
        }
      };

      socketRef.current.onclose = () => {
        socketRef.current.send("Goodbye !");
        console.log('WebSocket disconnected');
      };
    
  }, []); // Only runs once when the component mounts

  return (
  <>
    <h1>QUIZZ</h1>
    <h3>{question ? question.label: ""}</h3>

    {question ?  question.answers.map(q => {
      return <input type="button" key={q} value={q} onClick={() => send_answer(socketRef.current, q)}/>
    }): ""}
  </>
  )
}

export default MainPage

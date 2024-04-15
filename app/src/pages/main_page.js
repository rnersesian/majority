import React, { useState } from "react"
import {io} from "socket.io-client"


const MainPage = () => {


  const [time, setTime] = useState("")
  const socket = io("ws://77.37.86.225:8001")
  
  socket.on("connect", () => {
    socket.send("Hello there !")
  })

  socket.on("message", (data) => {
    console.log(data) 
  })


  
  return (
  <>
    <h1>Main Page</h1>
    <h3>{time}</h3>
  </>
  )
}

export default MainPage

import { Title } from "@solidjs/meta";
import { Show, createEffect, createSignal, onMount } from "solid-js";
import Cookie from "js-cookie"
import { Navigate, useNavigate } from "@solidjs/router";
import { WsEvents, sendRequests } from "~/utils/WSEvent";

export default function Home() {

  const [username, setUsername] = createSignal("")
  const [joined, setJoined] = createSignal(false)
  const [socket, setSocket] = createSignal({} as WebSocket)

  
  
  onMount(async () => {
    setSocket(new WebSocket("ws://77.37.86.225:8001"))
    console.log("hey")

    socket().addEventListener("message", (ws_event) => {
      let event = JSON.parse(ws_event.data)
      
      // Filtering events recieved by websocket 
      switch (event.type) { 
        case WsEvents.CONNECT_SUCCESS:
          let _username = (document.getElementById("username") as HTMLInputElement).value
          Cookie.set("username", _username)
          setJoined(true)
          break;

        default:
          console.log("Whut ?");
          break;
      }
    })
  })

  // When User enter its Username
  const on_connect = async () => {
    if (username() !== "") {
      await sendRequests(socket(), WsEvents.CONNECT, {player_name: username()})
    }
  }

  const navigate = useNavigate()

  createEffect(() => {
    setUsername(Cookie.get('username') || "")
  })


  
  // Login form that appears first
  const login_form =
    <div style={{margin: "auto", "margin-top": "100px"}}>
      <div>
        <div class="form-input">
          <label for="username">Username</label> <br/>
          <input type="text" id="username" placeholder="John Doe" value={username()} onChange={(event) => setUsername(event.currentTarget.value)}/>
        </div>
        <div class="form-input">
          <button value="Connect" class="submit" onClick={on_connect}>Connect</button>
        </div>
      </div> 
    </div>


  return (
    <main>
      <Title>Home</Title>
      <div class="content_center">
        <div></div>
          <Show when={joined()} fallback={login_form}>
            <div class="tspacing-x">
              <form>
                <div class="inline-input">
                  <label for="room_name">Create Room</label>
                  <input id="room_name" placeholder="Room Name"/>
                  <button class="submit">Create</button>
                </div>
              </form> 
            </div>
          </Show>
        <div></div>
      </div>
    </main>
  )
}

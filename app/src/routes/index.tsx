import { Title } from "@solidjs/meta";
import { Show, createSignal } from "solid-js";

export default function Home() {
  const [username, setUsername] = createSignal("")

  const on_connect = () => {
    let _username = (document.getElementById("username") as HTMLInputElement).value
    setUsername(_username)
    console.log(username())
  }

  console.log(username())


    const login_form = <main style={{margin: "auto", "margin-top": "100px"}}>
      <Title>Home</Title>
      <form>
        <div class="form-input">
          <label for="username">Username</label> <br/>
          <input type="text" id="username" placeholder="John Doe"/>
        </div>
        <div class="form-input">
          <button value="Connect" class="submit" onClick={on_connect}>Connect</button>
        </div>
      </form> 
    </main>

  return (
    <Show when={(username() !== "")} fallback={login_form}>
      <div>Hey {username()}</div>
    </Show>
  )
}

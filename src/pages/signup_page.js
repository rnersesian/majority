import React, { useState } from "react"
import InputText from "../components/input_text";


const SignupPage = () => {

  const [username, setUsername] = useState("")

  const onUsernameChange = (event) => {
    setUsername(event.target.value)
  };

  return (
  <div className="content_center">
    <h1>Sign Up page</h1>
      
      <InputText id="username" type="text" label="Username" value={username} onChange={onUsernameChange}/>

  </div>
  );
};


export default SignupPage;

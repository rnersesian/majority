import React, { useState } from "react"
import InputForm from "../components/input_form"
import InputText from "../components/input_text"

const MultiQuizzPage = () =>
{
    const [username, setUsername] = useState('')
    const [joined, setJoined] = useState(false)
    
    const join = () => {
        if (username != "")
        {
            setJoined(true)
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
    } else {
        console.log("hey")
        return (
            <div>Hello {username}</div>
        )
    }

    
}

export default MultiQuizzPage
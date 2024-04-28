import React, { useState } from "react"
import {useLocation} from 'react-router-dom';

const PlayRoomPage = () => {

    const location = useLocation();
    const [username, setUsername] = useState(location.state !== null && location.state.username ? location.state.username : "")

    return(
        <div>
            {/* {location.state.username || ""} */}
            hey
        </div>
    )
}

export default PlayRoomPage
import { a } from "react-router-dom"


const Navbar = () => {
  return (
    <div className="topnav">
      <div className="topnav_left">
        <a href="/">Home</a>
        <a href="lobbies">Multi Player</a>
      </div>
      <div className="topnav_right">
        <a href="signup">Sign Up</a>
      </div>
    </div>
  )
}


export default Navbar

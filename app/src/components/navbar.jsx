import { Link } from "react-router-dom"


const Navbar = () => {
  return (
    <div className="topnav">
      <div className="topnav_left">
      <Link to="/">Home</Link>
        <Link to="solo">Solo</Link>
        <Link to="lobbies">Multi Player</Link>
        <Link to="#about">About</Link>
      </div>
      <div className="topnav_right">
        <Link to="signup">Sign Up</Link>
      </div>
    </div>
  )
}


export default Navbar

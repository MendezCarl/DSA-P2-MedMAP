import { useState } from "react"
import {useNavigate} from "react-router-dom"
import "./LandingMain.css"

function LandingMain() {
    const [street, setAddress] = useState("")
    const navigate = useNavigate()

    const onSubmit = () => {
    localStorage.setItem('theaddy', street);
    navigate(`/results?`)
  }
    return(
        <div className="landing-wrapper">
            <div id="box0">
                <h1>Find the right specialist for you.</h1>
                <h2>Use our special search features to find a medical facility that is specific to you.</h2>
            </div>

            <div id="box1">
                <h3>To get started, enter your street address below:</h3>

                <input
                type="text"
                onChange={(e) => setAddress(e.target.value)}
                placeholder="123 Main St..."
                />

                <button className="effect" onClick={onSubmit}>
                Start
                </button>
            </div>
        </div>
  )
}

export default LandingMain;
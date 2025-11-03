import { Routes, Route, useNavigate } from "react-router-dom"
import { useState } from "react"
import Results from "./Results"

function LandingPage() {
  const [address, setAddress] = useState("")
  const [insurance, setInsurance] = useState("")
  const navigate = useNavigate()

  const onSubmit = () => {
    localStorage.setItem('theaddy', address);
    localStorage.setItem('provider', insurance);
    navigate(`/results?`)
  }

  return (
    <section className="hero">
      <h1>Find a in-network doctor near you</h1>
      <p>Enter your address</p>
      <input
        type="text"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        placeholder="123 Main St..."
      />
      <p>Enter your insurance provider</p>
      <input
        type="text"
        value={insurance}
        onChange={(e) => setInsurance(e.target.value)}
        placeholder="United.."
      />
      <button onClick={onSubmit}>Start</button>
    </section>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/results" element={<Results />} />
    </Routes>
  )
}

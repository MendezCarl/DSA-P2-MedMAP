import { Routes, Route } from "react-router-dom"
import Results from "./Results"
import Header from "./Header"
import LandingMain from "./LandingMain"
import LandingGen from "./LandingGen"

function LandingPage() {
  return (
    <section className="hero">
      <Header />
      <main>
          <LandingMain />
          <LandingGen />
      </main>
        <footer>
          <hr></hr>
          MedMap 2025 <br></br>
          authors: Ahsan Rahul, Carlos Mendez, Kris Meideros
        </footer>
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

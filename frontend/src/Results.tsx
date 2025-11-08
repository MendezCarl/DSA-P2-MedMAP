import { useEffect, useState } from "react"
import Header from "./Header"
import HospitalCard from "./hospitalcard"
import "./Results.css"
export default function Results() {
    const street = localStorage.getItem('theaddy') || "No address provided"
    const specialty = localStorage.getItem('specialty') || "no specialty provided"

    useEffect(() => {
    fetch("http://localhost:8000/api/hello")
        .then(r => r.json())
    }, [])

    return (
    <div>
        <Header />
        <hr></hr>
        <p>Street Address: {street}</p>
        <p>Requested Specialty: {specialty}</p>
        <hr></hr>
        <div className="page">
        <div className="left-column">
            <HospitalCard />
            <HospitalCard />
            <HospitalCard />
        </div>

        <div className="right-map">
            {/* map goes here later */}
        </div>
    </div>
    </div>
    )
}

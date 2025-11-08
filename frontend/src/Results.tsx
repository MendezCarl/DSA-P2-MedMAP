import { useEffect, useState } from "react"
import Header from "./Header"
import HospitalCard from "./hospitalcard"
import "./Results.css"
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
export default function Results() {
    const street = localStorage.getItem('theaddy') || "No address provided"
    const specialty = localStorage.getItem('specialty') || "no specialty provided"

    useEffect(() => {
        const map = L.map('map').setView([51.505, -0.09], 13) // Update to not be hardcoded

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution:
            '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(map)

        var circle = L.circle([51.505, -0.09], { // Update to not be hardcoded
            color: 'red',
            fillColor: 'rgba(238, 255, 0, 1)',
            fillOpacity: 0.3,
            radius: 500
        }).addTo(map);

        var marker = L.marker([51.505, -0.09]).addTo(map);

        // Proper cleanup
        return () => {
            map.remove()
        }
    }, [])

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
            <div id="map"></div>
        </div>
    </div>
    </div>
    )
}

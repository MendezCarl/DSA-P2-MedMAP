import { useEffect, useState } from "react"
import Header from "./Header"
import HospitalCard from "./hospitalcard"
import "./Results.css"
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

type HospitalInfo = {
  name: string
  address: string
  functionality: string[]
  longitude: number
  latitude: number
  distance: number
}

export default function Results() {
    const street = localStorage.getItem('theaddy') || "No address provided"
    const specialty = localStorage.getItem('specialty') || "no specialty provided"
    const [hospitals, setHospitals] = useState<HospitalInfo[]>([])

    useEffect(() => {
        if (hospitals.length === 0) return

        const fac = hospitals[0]

        const map = L.map("map").setView([fac.latitude, fac.longitude], 12)

        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution:
            '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(map)

        hospitals.forEach(h => {
            L.marker([h.latitude, h.longitude])
            .addTo(map)
            .bindPopup(
                `${h.name}<br>${h.address}<br>${h.distance.toFixed(0)} m away`
            )
        })

        return () => {
            map.remove()
        }
        }, [hospitals])

    useEffect(() => {
        fetch("http://localhost:8000/api/hospitals", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ address: street }),
        })
            .then(res => res.json())
            .then((data: HospitalInfo[]) => {
            setHospitals(data)
            })
            .catch(console.error)
    }, [street])

    return (
    <div>
        <Header />
        <hr></hr>
        <p>Street Address: {street}</p>
        <p>Requested Specialty: {specialty}</p>
        <hr></hr>
        <div className="page">
        <div className="left-column">
            {hospitals.map(h => (
                <HospitalCard
                key={h.name + h.address}
                name={h.name}
                address={h.address}
                distance={h.distance}
                functionality={h.functionality}
                />
            ))}
        </div>

        <div className="right-map">
            {/* map goes here later */}
            <div id="map"></div>
        </div>
    </div>
    </div>
    )
}

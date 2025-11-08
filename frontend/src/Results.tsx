import { useEffect, useState } from "react"
import HosiptalCard from "./hospitalcard"

export default function Results() {
    const street = localStorage.getItem('theaddy') || "no address found"
    const [backendMsg, setBackendMsg] = useState("loading...")

    useEffect(() => {
    fetch("http://localhost:8000/api/hello")
        .then(r => r.json())
        .then(data => setBackendMsg(data.message))
    }, [])

    return (
    <div>   
        <p>Street Address: {street}</p>
        {/* <p>Backend says: {backendMsg}</p> */}
        <HosiptalCard />
        <HosiptalCard />
        <HosiptalCard />
    </div>
    )
}

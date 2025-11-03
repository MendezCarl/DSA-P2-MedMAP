import { useEffect, useState } from "react"

export default function Results() {
    const address = localStorage.getItem('theaddy') || "no address found"
    const insurance = localStorage.getItem('provider') || "no insurance found"
    const [backendMsg, setBackendMsg] = useState("loading...")

    useEffect(() => {
    fetch("http://localhost:8000/api/hello")
        .then(r => r.json())
        .then(data => setBackendMsg(data.message))
    }, [])

    return (
    <div>
        <h1>Results Page</h1>
        <p>Address: {address}</p>
        <p>Insurance: {insurance}</p>
        <p>Backend says: {backendMsg}</p>
    </div>
    )
}

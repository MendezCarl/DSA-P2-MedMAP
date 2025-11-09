import { useEffect, useState } from "react";
import Header from "./Header";
import HospitalCard from "./HospitalCard";
import "./Results.css";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

type HospitalInfo = {
  name: string;
  address: string;
  functionality: string[];
  longitude: number;
  latitude: number;
  distance: number;
};

type RouteResult = {
  algorithm: string;
  path: [number, number][];       
  wayPointsCount: number;
  distanceKm: number;
  startCoord: [number, number];
  endCoord: [number, number];
};

export default function Results() {
const [algorithm, setAlgorithm] = useState<"dijkstra" | "astar">("dijkstra");
  const street = localStorage.getItem("theaddy") || "No address provided";
  const specialty = localStorage.getItem("specialty") || "no specialty provided";
  const [hospitals, setHospitals] = useState<HospitalInfo[]>([]);
  const [route, setRoute] = useState<RouteResult | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/hospitals", {
        method: "POST",
    })
        .then(res => res.json())
        .then((data: HospitalInfo[]) => {
        console.log("Hospitals from API:", data);
        setHospitals(data);
        })
        .catch(console.error);
    }, []);

  const handleRouteClick = (hospital: HospitalInfo) => {
    const fromLat = 29.6516;
    const fromLon = -82.3248;

    const toLat = hospital.latitude;
    const toLon = hospital.longitude;

    fetch("http://localhost:8000/api/route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fromLat,
        fromLon,
        toLat,
        toLon,
        algorithm,
      }),
    })
      .then(res => {
        if (!res.ok) {
          throw new Error("Failed to fetch route");
        }
        return res.json();
      })
      .then((data: RouteResult) => {
        console.log("Route data:", data);
        setRoute(data);
      })
      .catch(console.error);
  };

  useEffect(() => {
    if (hospitals.length === 0) return;

    const defaultCenterLat = 29.62821;
    const defaultCenterLon = -82.36349;
    const centerLat = route ? route.startCoord[0] : defaultCenterLat;
    const centerLon = route ? route.startCoord[1] : defaultCenterLon;

    const existing = L.DomUtil.get("map") as any;
    if (existing && existing._leaflet_id) {
      existing._leaflet_id = null;
    }

    const map = L.map("map").setView([centerLat, centerLon], 12);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    L.circle([defaultCenterLat, defaultCenterLon], {
      radius: 40200,
      color: "yellow",
      fillColor: "yellow",
      fillOpacity: 0.15,
    }).addTo(map);

    // Hospital markers
    hospitals.forEach(h => {
      L.marker([h.latitude, h.longitude])
        .addTo(map)
        .bindPopup(
          `${h.name}<br>${h.address}<br>${h.distance.toFixed(0)} m away`
        );
    });

    // Draw route polyline if we have one
    if (route && route.path && route.path.length > 1) {
      const latlngs = route.path.map(([lat, lon]) => [lat, lon]) as [number, number][];

      const polyline = L.polyline(latlngs, {
        color: "blue",
        weight: 4,
      }).addTo(map);

      // Fit map to route bounds
      map.fitBounds(polyline.getBounds());
    }

    return () => {
      map.remove();
    };
  }, [hospitals, route]);

  return (
    <div>
      <Header />
      <hr />
      <p>Street Address: {street}</p>
      <p>Requested Specialty: {specialty}</p>
      <hr />
      <div className="page">
        <div className="algorithm-toggle">
  <label>
    <input
      type="radio"
      value="dijkstra"
      checked={algorithm === "dijkstra"}
      onChange={() => setAlgorithm("dijkstra")}
    />
    Dijkstra
  </label>
  <label style={{ marginLeft: "1rem" }}>
    <input
      type="radio"
      value="astar"
      checked={algorithm === "astar"}
      onChange={() => setAlgorithm("astar")}
    />
    A*
  </label>
</div>

        <div className="left-column">
          {hospitals.map(h => (
            <HospitalCard
              key={h.name + h.address}
              name={h.name}
              address={h.address}
              distance={h.distance}
              functionality={h.functionality}
              onRoute={() => handleRouteClick(h)}
            />
          ))}
        </div>

        <div className="right-map">
          <div id="map"></div>
        </div>
      </div>
    </div>
  );
}

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel 

from backend.schemas.output import hospitalInfo
from backend.schemas.output import route as RouteSchema
from backend.utils.osmImplmentation import getLocationFromAddress, createSearchArea, findRoute
from backend.utils.databaseImplmentation import getMedicalFacilities

router = APIRouter()

@router.post("/api/hospitals", response_model=list[hospitalInfo])
def get_nearby_hospitals():

    hospitals = [
        hospitalInfo(
            name="UF Health Shands Hospital",
            address="1600 SW Archer Rd, Gainesville, FL 32610",
            functionality=[
                "General Medical Facility",
                "Emergency Department",
                "Trauma Center",
                "Cardiac Care Unit",
                "Neurology Services"
            ],
            longitude=-82.3410,
            latitude=29.6390,
            distance=2.1
        ),
        hospitalInfo(
            name="HCA Florida North Florida Hospital",
            address="6500 W Newberry Rd, Gainesville, FL 32605",
            functionality=[
                "General Medical Facility",
                "Emergency Department",
                "Surgical Unit",
                "ICU",
                "Orthopedic Services"
            ],
            longitude=-82.3924,
            latitude=29.6591,
            distance=5.4
        ),
        hospitalInfo(
            name="Malcom Randall VA Medical Center",
            address="1601 SW Archer Rd, Gainesville, FL 32608",
            functionality=[
                "Veterans Affairs Hospital",
                "Primary Care",
                "Rehabilitation Services",
                "Mental Health",
                "Pharmacy"
            ],
            longitude=-82.3407,
            latitude=29.6398,
            distance=2.0
        ),
        hospitalInfo(
            name="UF Health Shands Psychiatric Hospital",
            address="4101 NW 89th Blvd, Gainesville, FL 32606",
            functionality=[
                "Psychiatric Facility",
                "Mental and Behavioral Health",
                "Outpatient Services"
            ],
            longitude=-82.4121,
            latitude=29.6840,
            distance=7.1
        ),
        hospitalInfo(
            name="HCA Florida Lake City Hospital",
            address="340 NW Commerce Dr, Lake City, FL 32055",
            functionality=[
                "General Medical Facility",
                "Emergency Department",
                "Inpatient Care"
            ],
            longitude=-82.6896,
            latitude=30.1847,
            distance=47.0  # ~47 km (≈29 mi)
        ),
    ]

    return hospitals

    # loc = getLocationFromAddress(address)
    # if not loc:
    #     raise HTTPException(status_code=404, detail="Could not resolve address")

    # area = createSearchArea(loc.latitude, loc.longitude, radiusKm=25)
    # if not area:
    #     raise HTTPException(status_code=500, detail="Failed to create search area")

    # facilities = getMedicalFacilities(area)

    # return facilities


class RouteRequest(BaseModel):
    fromLat: float
    fromLon: float
    toLat: float
    toLon: float
    algorithm: str = "dijkstra" 

@router.post("/api/route", response_model=RouteSchema)
def get_route(req: RouteRequest):
    r = findRoute(
        fromLat=req.fromLat,
        fromLon=req.fromLon,
        toLat=req.toLat,
        toLon=req.toLon,
        algo=req.algorithm,
    )
    if not r:
        raise HTTPException(status_code=404, detail="No route found")

    return r
from fastapi import APIRouter, HTTPException, Body

from backend.schemas.output import hospitalInfo
from backend.utils.osmImplmentation import getLocationFromAddress, createSearchArea
from backend.utils.databaseImplmentation import getMedicalFacilities

router = APIRouter()

@router.post("/api/hospitals", response_model=list[hospitalInfo])
def get_nearby_hospitals(address: str = Body(..., embed=True)):
    loc = getLocationFromAddress(address)
    if not loc:
        raise HTTPException(status_code=404, detail="Could not resolve address")

    area = createSearchArea(loc.latitude, loc.longitude, radiusKm=25)
    if not area:
        raise HTTPException(status_code=500, detail="Failed to create search area")

    facilities = getMedicalFacilities(area)

    return facilities
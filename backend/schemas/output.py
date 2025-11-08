from pydantic import BaseModel

class currentLocation(BaseModel):
    latitude: float
    longitude: float
    street: str | None = None

class destinationLocation(BaseModel):
    latitude: float
    longitude: float
    street: str | None = None

class hospitalInfo(BaseModel):
    name: str
    address: str
    functionality: list[str]
    longitude: float
    latitude: float
    distance: float

class hospitalInfoRequest(BaseModel):
    longitude: float
    latitude: float
    address: str | None = None
    name: str | None = None
    functionality: list[str] | None = None

#search area will be a circle with radius r
class searchArea(BaseModel):
    minLongitude: float
    minLatitude: float
    maxLongitude: float
    maxLatitude: float
    city:  str | None

class route(BaseModel):
    algorithm: str
    path: list[tuple[float, float]]
    wayPointsCount: int
    distanceKm: float
    startCoord: tuple[float, float]
    endCoord: tuple[float, float]
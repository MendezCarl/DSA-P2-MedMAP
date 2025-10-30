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
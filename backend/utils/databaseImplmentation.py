import requests
from geopy.distance import geodesic
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.schemas.output import searchArea, hospitalInfo

DATABASE_API_URL = "https://data.cms.gov/data-api/v1/dataset/8ba0f9b4-9493-4aa0-9f82-44ea9468d1b5/data"

def getMedicalFacilities(area: searchArea) -> list[hospitalInfo]:
    try:
        params ={
            'limit': 100000,
            'offset': 0
        }

        if area.city:
            params['filter[city]'] = area.city

        response = requests.get(DATABASE_API_URL, params=params)
        response.raise_for_status()

        data = response.json()
        facilities = []

        for facility in data:
            try:
                lat = float(facility.get('latitude', 0))
                lon = float(facility.get('longitude', 0))
            except(ValueError, TypeError):
                continue

            if not (area.minLatitude <= lat <= area.maxLatitude and 
                    area.minLongitude <= lon <= area.maxLongitude):
                continue

            name = facility.get('facility_name', 'Unknown Facility')

            addressParts = []
            if facility.get('address'):
                addressParts.append(facility['address'])
            if facility.get('city'):
                addressParts.append(facility['city'])
            if facility.get('state'):
                addressParts.append(facility['state'])
            if facility.get('zip_code'):
                addressParts.append(facility['zip_code'])

            address = ', '.join(addressParts) if addressParts else "Address not found in database"

            functionality = []
            
            if facility.get('emergency_services') == 'Yes':
                functionality.append('Emergency')
            
            facility_type = facility.get('facility_type') or facility.get('hospital_type')
            if facility_type:
                functionality.append(facility_type)
            
            rating = facility.get('hospital_overall_rating')
            if rating:
                functionality.append(f'{rating}-Star Rating')
            
            #default value
            if not functionality:
                functionality = ['General Hospital']
            
            facilityCoord = (lat,lon)

            #recalulate center vertex(origin)
            fromLat = (area.minLatitude + area.maxLatitude) / 2
            fromLon = (area.minLongitude + area.maxLongitude) / 2
            fromCoord = (fromLat, fromLon)

            distance = geodesic(fromCoord, facilityCoord).meters

            facilities.append(hospitalInfo(
                name = name,
                address= address,
                functionality = functionality,
                longitude= lon,
                latitude= lat,
                distance = round(distance, 2)
            ))

        facilities.sort(key = lambda h: h.distance)
        print(f"There are {len(facilities)} in the search area"
        return facilities
    except Exception as e:
        print(f"Not able to access database of facilities")
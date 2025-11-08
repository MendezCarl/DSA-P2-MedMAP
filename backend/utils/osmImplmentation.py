# adjacency list representation of a graph
# will be using a weighted graph. The weights will be the distance between nodes

from collections import defaultdict
import math
import requests
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.schemas.output import (
    currentLocation,
    destinationLocation,
    hospitalInfo,
    hospitalInfoRequest,
    searchArea
)
from backend.utils.graph import Graph

OVERPASS_API_URL = "http://overpass-api.de/api/interpreter"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

geoLocator = Nominatim(user_agent="medMap")

ALLOWED_NODE_TYPES = {
    "motorway",
    "motorway_link",
    "trunk",
    "trunk_link",
    "primary",
    "primary_link",
    "secondary",
    "secondary_link",
    "tertiary",
    "tertiary_link",
    "unclassified",
    "residential",
    "service",
    "living_street",
    "road",
}

EXCLUDED_NODE_TYPES = {
    "footway",
    "path",
    "pedestrian",
    "cycleway",
    "steps",
}

def getLocationFromAddress(address:str) -> currentLocation | None:
    try:
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }

        response = requests.get(NOMINATIM_URL, params=params)
        response.raise_for_status()

        data = response.json()
        if not data:
            return None
        
        result = data[0]
        return currentLocation(
            latitude=float(result['lat']),
            longitude=float(result['lon']),
            street=result['display_name']
        )
    except Exception as e:
        print(F"Error getting location from Address: {e}")
        return None

def findClosestCity(lat: float, lon: float) -> str | None:
    try:
        location = geoLocator.reverse(f"{lat}, {lon}", exactly_one=True)

        if not location:
            return None
        
        if hasattr(location, 'raw'):
            address = location.raw.get('address', {})
            
            # Extract city from address components
            city = (
                address.get('city') or
                address.get('town') or
                address.get('village') or
                address.get('municipality') or
                address.get('county')
            )
            
            return city
        
        return None
            
    except Exception as e:
        print(f"Error finding closest City to address: {e}")
        return None
    
def createSearchArea(lat: float, lon: float, radiusKm: float = 25) -> searchArea | None:
    try:
        #used https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
        #says the formula for how to work with longitude and latidute

        latDiff = radiusKm / 110.574
        lonDiff = radiusKm / (111.320 * math.cos(math.radians(lat)))

        city = findClosestCity(lat, lon)

        return searchArea(
            minLongitude= lon - lonDiff,
            minLatitude= lat - latDiff,
            maxLongitude= lon + lonDiff,
            maxLatitude= lat + latDiff,
            city = city
        )
    except Exception as e:
        print(f"Error creating search area: {e}")
        return None
    
def getRoadNetwork(area: searchArea) -> list[dict]:
    highwayTypes = '|'.join(ALLOWED_NODE_TYPES)

    overpassQuery = f"""
    [out:json];
    (
        way["highway"~"^({highwayTypes})$"]({area.minLatitude}, {area.minLongitude}, {area.maxLatitude}, {area.maxLongitude});
    );
    out body;
    >;
    out skel qt;
    """

    try:
        response = requests.post(OVERPASS_API_URL, data = overpassQuery)
        response.raise_for_status()

        data = response.json()
        elements = data.get('elements', [])

        cityName = area.city or "search area"
        waysCount = len([e for e in elements if e['type'] == 'way'])
        nodesCount = len([e for e in elements if e['type'] == 'node'])

        print(f"found {waysCount} roads and {nodesCount} nodes in {cityName}")

        return elements
    except Exception as e:
        print(f"Error retrieving road network: {e}")
        return []

def buildGraphFromRoadNetwork(area: searchArea):
    elements = getRoadNetwork(area)

    nodes = {}
    ways = []

    for element in elements:
        if element['type'] == 'way':
            ways.append(element)
        elif element['type'] == 'node':
            nodes[element['id']] = (element['lat'], element['lon'])

    graph = Graph()

    for way in ways:
        wayNode = way.get('nodes', [])

        for i in range(len(wayNode) - 1):
            node1Id = wayNode[i]
            node2Id = wayNode[i+1]

            if node1Id in nodes and node2Id in nodes:
                coord1 = nodes[node1Id]
                coord2 = nodes[node2Id]

                distance = geodesic(coord1, coord2).meters

                #makes the graph a undirectedgraph, assumes all roads are 2 way
                graph.addEdge(coord1, coord2, distance)
                graph.addEdge(coord2, coord1, distance)

    print(f"Graph has been built with {len(graph.graph)} nodes")
    return graph

def findNearestRoadNode(lat: float, lon: float, graph: Graph) -> tuple[float, float] | None:
    givenNode = (lat, lon)
    minDistance = float('inf')
    nearestNod = None

    for node in graph.graph.keys():
        distance = geodesic(givenNode, node).meters
        if distance < minDistance:
            minDistance = distance
            nearestNod = node
    
    return nearestNod

def findRoute(fromLat: float, fromLon: float, toLat: float, toLon: float, algo: str):
    try:
        startCoord = (fromLat, fromLon)
        endCoord = (toLat, toLon)
        distance = geodesic(startCoord, endCoord).kilometers

        centerLat = (fromLat + toLat) / 2 
        centerLon = (fromLon + toLon) / 2

        radius = max(distance * 0.75, 5)

        area = createSearchArea(centerLat, centerLon)

        if not area:
            print("could not create a search area")
            return None
        
        graph = buildGraphFromRoadNetwork(area)

        if len(graph.graph) == 0:
            print("No road network found")
            return None
        
        startNode = findNearestRoadNode(fromLat, fromLon, graph)
        endNode = findNearestRoadNode(toLat, toLon, graph)

        if not startNode or not endNode:
            print("No rode nodes at currently location")
            return None
        
        if algo.lower() == "astar":
            path = graph.aStarRoute(startNode, endNode)
            if path:
                print(f"AStar route with {len(path)} nodes")
        elif algo.lower() == "dijkstra":
            path = graph.dijkstraRoute(startNode, endNode)  
            if path:
                print(f"Dijkstra route with {len(path)} nodes")

        if not path:
            print("No road route found")
            return None
        
        roadRouteTotalDistance = 0
        for i in range(len(path) - 1):
            roadRouteTotalDistance += geodesic(path[i], path[i+1]).kilometers
        print(f"Total road route distance: {roadRouteTotalDistance}km")

        return path
    except Exception as e:
        print(f"Error finding road route: {e}")
        return None
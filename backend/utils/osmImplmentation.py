# adjacency list representation of a graph
# will be using a weighted graph. The weights will be the distance between nodes

from collections import defaultdict

OVERPASS_API_URL = "http://overpass-api.de/api/interpreter"

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
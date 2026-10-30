
# airports.py
# Sample data for an educational air traffic simulation

AIRPORTS = {
    "DEL": {
        "name": "Delhi",
        "x": 2,
        "y": 8,
        "capacity": 100
    },
    "JAI": {
        "name": "Jaipur",
        "x": 1,
        "y": 6,
        "capacity": 45
    },
    "LKO": {
        "name": "Lucknow",
        "x": 5,
        "y": 7,
        "capacity": 55
    },
    "BHO": {
        "name": "Bhopal",
        "x": 4,
        "y": 4,
        "capacity": 40
    },
    "MUM": {
        "name": "Mumbai",
        "x": 2,
        "y": 1,
        "capacity": 90
    },
    "HYD": {
        "name": "Hyderabad",
        "x": 6,
        "y": 2,
        "capacity": 65
    },
    "BLR": {
        "name": "Bengaluru",
        "x": 5,
        "y": 0,
        "capacity": 70
    },
    "CHE": {
        "name": "Chennai",
        "x": 8,
        "y": 1,
        "capacity": 60
    }
}

# Direct connections and illustrative distances in km.
# Each route is undirected.
ROUTES = [
    ("DEL", "JAI", 230),
    ("DEL", "LKO", 420),
    ("DEL", "BHO", 600),
    ("JAI", "BHO", 500),
    ("JAI", "MUM", 900),
    ("LKO", "BHO", 320),
    ("LKO", "HYD", 900),
    ("BHO", "MUM", 650),
    ("BHO", "HYD", 650),
    ("MUM", "HYD", 620),
    ("MUM", "BLR", 840),
    ("HYD", "BLR", 500),
    ("HYD", "CHE", 520),
    ("BLR", "CHE", 290)
]

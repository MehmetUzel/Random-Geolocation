import requests
import json

city = "Larende"
urls = f"https://nominatim.openstreetmap.org/search.php?q={city}&polygon_geojson=1&format=json"

res = requests.get(urls)
jsond = res.json()

polygonps = list(map(tuple, jsond[0]['geojson']['coordinates'][0]))


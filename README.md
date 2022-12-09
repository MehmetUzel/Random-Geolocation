# Random-Geolocation
This Python script can be used for creation random points inside given geolocation polygon data

docker run -d geoloc tail -f /dev/null

https://stackoverflow.com/questions/54626317/find-polygon-of-city-or-region-on-map

https://nominatim.org/release-docs/develop/api/Search/

https://nominatim.openstreetmap.org/search.php?q=Tepebasi&polygon_geojson=1&format=json&accept-language=en

https://nominatim.openstreetmap.org/search.php?city=Eskisehir&polygon_geojson=1&format=geojson


https://www.latlong.net


docker cp <containerId>:/file/path/within/container /host/path/target

docker cp e80fe0f239d1:/app_demo/foo.png ~/ 

curl -o point.csv 'http://127.0.0.1:8000/v1/search' -H 'accept: application/json'

intelligent_sutherland


"docker" Failed to get options via gdal-config: [Errno 2] No such file or directory: gdal-config #13 3.830   A GDAL API version must be specified.


"""
curl -X 'POST' \
'http://127.0.0.1:8000/v1/search' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"area_name": "string","num_of_loc": 100,"is_normal_dist": false,"wb_or_xmean": 41.00,"eb_or_xstd": 0.07,"nb_or_ymean": 28.95,"sb_or_ystd": 0.23}'
"""
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import random
import pandas as pd 
from app.locationproc import is_inside_polygon
from fastapi.responses import StreamingResponse
import io
import requests

load_dotenv()
app = FastAPI()

class Search(BaseModel):
    area_name: str
    num_of_loc: int
    is_uniform_dist: bool
    wb_or_xmean: float
    eb_or_xstd: float
    nb_or_ymean: float
    sb_or_ystd: float

@app.get("/v1/test/smp", status_code=201)
async def testing():
    return {"mehmet":"success"}

@app.get("/v1/test/data" , response_description='csv')
async def recieve_test_signal():
    data = {
        "area_name": "Istanbul",
        "num_of_loc": 100,
        "is_uniform_dist": False,
        "wb_or_xmean": 28.95,
        "eb_or_xstd": 0.23,
        "nb_or_ymean": 41.00,
        "sb_or_ystd": 0.07
    }
    signal = Search(**data)

    df = process_signal(signal)

    stream = io.StringIO()
    
    df.to_csv(stream, index = False, header = False)

    response = StreamingResponse(iter([stream.getvalue()]),
                        media_type="text/csv"
    )

    response.headers["Content-Disposition"] = "attachment; filename=export.csv"

    return response

@app.get("/v1/search" , response_description='csv')
async def recieve_signal(signal: Search):
    
    df, found_name = process_signal(signal)

    stream = io.StringIO()
    
    df.to_csv(stream, index = False, header = False)

    response = StreamingResponse(iter([stream.getvalue()]),
                        media_type="text/csv"
    )

    #!!! Add found name and fig to responsee !!!

    response.headers["Content-Disposition"] = "attachment; filename=export.csv"

    return response


def process_signal(signal: Search):
    points_list, found_name = get_polygon_list("Beylikdüzü")

    polygonps = convert_to_tuple(points_list)

    xlist, ylist = get_points(signal, polygonps, points_list)    

    save_fig(polygonps, xlist, ylist)

    data = list(zip(xlist, ylist))

    df = pd.DataFrame(data)

    return df, found_name  

def save_fig(polygonps,xlist,ylist):
    polygon = Polygon(polygonps)

    p = gpd.GeoSeries(polygon)
    p.plot()

    plt.scatter(xlist, ylist, c='cyan')
    plt.savefig('foo.png', bbox_inches='tight')

def get_points(signal: Search, polygon_list, points_list):
    NUMBER_OF_POINTS = signal.num_of_loc
    count = 0
    pcount = 0
    xlist = []
    ylist = []

    while NUMBER_OF_POINTS > pcount:
        x, y = random_loc(signal, points_list)
        p = (x, y)
        if is_inside_polygon(points = polygon_list, p = p):
            pcount += 1
            xlist.append(x)
            ylist.append(y)
        else:
            count -= 1
        
        if count < -1000:
            break

    return xlist, ylist
    
def random_loc(signal: Search, points_list):
    if signal.is_uniform_dist:
        xmin, xmax, ymin, ymax = find_boundaries(points_list)
        return random.uniform(xmin, xmax) , random.uniform(ymin, ymax)

    return random.gauss(signal.wb_or_xmean, signal.eb_or_xstd) , random.gauss(signal.nb_or_ymean, signal.sb_or_ystd)


def get_polygon_list(city):
	query_city = city.replace(' ','+')
	urls = f"https://nominatim.openstreetmap.org/search.php?q={query_city}&polygon_geojson=1&format=json"

	res = requests.get(urls)
	jsond = res.json()
	for a in jsond:
		if a['geojson']['type'] == 'Polygon':
			return a['geojson']['coordinates'][0], a['display_name']

def convert_to_tuple(points):
	return list(map(tuple, points))

def find_boundaries(points):
	x_coord, y_coord = zip(*points)

	xmin = min(x_coord)
	xmax = max(x_coord)
	ymin = min(y_coord)
	ymax = max(y_coord)

	return xmin,xmax,ymin,ymax


"""
def random_gauss_points(num_req, polygonpoints):
	count = 0
	xlist = []
	ylist = []

	for x in range(num_req):
		y = random.gauss(41.00, 0.07)
		a =  random.gauss(28.95, 0.23)
		p = (a, y)
		if (is_inside_polygon(points = polygonpoints, p = p)):
			count += 1
			xlist.append(a)
			ylist.append(y)
		if count >= 1500:
			break

	return xlist, ylist


def random_normal_points(num_req, polygonpoints, points_list):
	xmin, xmax, ymin, ymax = find_boundaries(points_list)
	count = 0
	xlist = []
	ylist = []

	for x in range(num_req*10):
		y = random.uniform(ymin, ymax)
		a =  random.uniform(xmin, xmax)
		p = (a, y)
		if (is_inside_polygon(points = polygonpoints, p = p)):
			count += 1
			xlist.append(a)
			ylist.append(y)
		if count >= num_req:
			break

	return xlist, ylist
"""

def save_points_csv(xlist, ylist):
	data = list(zip(xlist, ylist))

	df = pd.DataFrame(data)
		
	df.to_csv('points.csv', index=False, header=False)

def generate_points():
    points_list, found_name = get_polygon_list("Beylikdüzü")
    print(found_name)

    polygonps = convert_to_tuple(points_list)

    polygon4 = Polygon(polygonps)

    xlist, ylist = random_normal_points(500,polygonps,points_list)

    save_points_csv(xlist, ylist)

    p = gpd.GeoSeries(polygon4)
    p.plot()

    plt.scatter(xlist, ylist, c='cyan')
    plt.show()



from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import random
import pandas as pd  


INT_MAX = 10000

def onSegment(p:tuple, q:tuple, r:tuple) -> bool:
	
	if ((q[0] <= max(p[0], r[0])) &
		(q[0] >= min(p[0], r[0])) &
		(q[1] <= max(p[1], r[1])) &
		(q[1] >= min(p[1], r[1]))):
		return True
		
	return False

def orientation(p:tuple, q:tuple, r:tuple) -> int:
	
	val = (((q[1] - p[1]) *
			(r[0] - q[0])) -
		((q[0] - p[0]) *
			(r[1] - q[1])))
			
	if val == 0:
		return 0
	if val > 0:
		return 1
	else:
		return 2

def doIntersect(p1, q1, p2, q2):
	
	o1 = orientation(p1, q1, p2)
	o2 = orientation(p1, q1, q2)
	o3 = orientation(p2, q2, p1)
	o4 = orientation(p2, q2, q1)

	if (o1 != o2) and (o3 != o4):
		return True
	
	if (o1 == 0) and (onSegment(p1, p2, q1)):
		return True

	if (o2 == 0) and (onSegment(p1, q2, q1)):
		return True

	if (o3 == 0) and (onSegment(p2, p1, q2)):
		return True

	if (o4 == 0) and (onSegment(p2, q1, q2)):
		return True

	return False

def is_inside_polygon(points:list, p:tuple) -> bool:
	
	n = len(points)
	
	if n < 3:
		return False
		
	extreme = (INT_MAX, p[1])
	
	decrease = 0
	count = i = 0
	
	while True:
		next = (i + 1) % n
		
		if(points[i][1] == p[1]):
			decrease += 1
		
		if (doIntersect(points[i],
						points[next],
						p, extreme)):
							
			if orientation(points[i], p,
						points[next]) == 0:
				return onSegment(points[i], p,
								points[next])
								
			count += 1
			
		i = next
		
		if (i == 0):
			break
			
	count -= decrease
	
	return (count % 2 == 1)

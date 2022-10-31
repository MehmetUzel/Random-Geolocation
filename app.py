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

if __name__ == '__main__':
    polygonlist = [(29.256526947021598,41.23541641235357),(29.588193893432674,41.16986083984381),(29.60958290100092,41.18236160278326),(29.674583435058594,41.16152954101574),(29.862083435058594,41.14374923706049),(29.882982254028377,41.09217834472656),(29.848857879638842,41.06917572021507),(29.748725891113565,41.05318450927746),(29.644767761230582,41.00930404663086),(29.496175765991495,41.035736083984375),(29.481319427490405,41.0007019042971),(29.43189430236822,40.97430038452154),(29.419984817504826,40.92051315307623),(29.348457336425952,40.891124725342024),(29.322084426879996,40.85878372192377),(29.261529922485522,40.85514068603521),(29.24763870239275,40.87208175659191),(29.144582748413143,40.90069580078125),(29.09708595275896,40.95013809204113),(29.03152847290056,40.96625137329107),(29.037639617920092,40.97958374023449),(29.02180480957037,40.978195190429915),(29.00597190856945,41.00986099243164),(29.008750915527344,41.02597045898432),(29.051527023315884,41.048194885254134),(29.06597137451172,41.10291671752941),(29.096250534057617,41.11791610717796),(29.070972442627067,41.14319610595709),(29.087083816528377,41.1787490844726),(29.165416717529467,41.224582672119254),(29.256526947021598,41.23541641235357),(28.199028015136832,41.54597091674816),(28.272918701171875,41.49569320678711),(28.63097190856962,41.35013961791992),(28.684305191040153,41.347915649414176),(28.78430557250988,41.30208206176758),(28.81125259399414,41.30541610717779),(28.96597290039074,41.25319290161144),(29.07819366455078,41.254581451416016),(29.11180686950712,41.23819351196289),(29.10958480834961,41.210140228271484),(29.037359237671126,41.15597152709961),(29.07236099243164,41.124862670898665),(29.05708312988287,41.0818061828615),(29.033193588256893,41.0498619079591),(28.975973129272518,41.02152633666992),(28.94013977050804,41.048194885254134),(28.9487495422365,41.057640075683594),(28.944026947021484,41.06458282470709),(28.93625068664562,41.045417785644474),(28.963472366333065,41.02152633666992),(28.986803054809684,41.017082214355526),(28.984863281250114,41.004859924316406),(28.9368057250976,41.00125122070318),(28.875139236450423,40.96847152709961),(28.85014152526867,40.97430419921875),(28.82430458068859,40.95402908325195),(28.76430511474615,40.98152923583979),(28.620138168334904,40.96041488647472),(28.595138549804744,40.97347259521496),(28.588472366333235,41.01763916015625),(28.564027786254883,41.017082214355526),(28.54124832153326,40.984306335449446),(28.407083511352766,41.045417785644474),(28.259582519531648,41.06236267089855),(28.233472824097134,41.07764053344749),(28.123260498046932,41.05986022949247),(28.057348251342773,41.15075302124052),(28.087570190429744,41.21114730834984),(28.15098190307623,41.24227523803734),(28.199129104614258,41.363262176513956),(28.23168945312517,41.499076843261776),(28.179122924804744,41.52955627441423),(28.199028015136832,41.54597091674816)]

    NUMBER_OF_POINTS = 1500
    count = 0
    xlist = []
    ylist = []
    p = gpd.GeoSeries(Polygon(polygonlist))
    p.plot()

    for i in range(NUMBER_OF_POINTS*10):
        #x = random.uniform(west_border, east_border)
        #y = random.uniform(north_border, south_border)
        x =  random.gauss(28.95, 0.23)
        y = random.gauss(41.00, 0.07)
        p = (x, y)
        if is_inside_polygon(points = polygonlist, p = p):
            count += 1
            xlist.append(x)
            ylist.append(y)
        if count >= NUMBER_OF_POINTS:
            break

    data = list(zip(xlist, ylist))
    plt.scatter(xlist, ylist, c='red')
    #plt.show()
    plt.savefig('foo.png', bbox_inches='tight')

    df = pd.DataFrame(data)

    df.to_csv('points.csv', index=False, header=False)

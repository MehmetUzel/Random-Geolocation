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

load_dotenv()
app = FastAPI()

class Search(BaseModel):
    area_name: str
    num_of_loc: int
    is_normal_dist: bool
    wb_or_xmean: float
    eb_or_xstd: float
    nb_or_ymean: float
    sb_or_ystd: float

@app.get("/v1/test", status_code=201)
async def testing():
    return {"mehmet":"success"}

@app.get("/v1/search" , response_description='csv')
async def recieve_signal():
    data = {
        "area_name": "Istanbul",
        "num_of_loc": 100,
        "is_normal_dist": False,
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


def process_signal(signal: Search):

    polygonlist = [(29.256526947021598,41.23541641235357),(29.588193893432674,41.16986083984381),(29.60958290100092,41.18236160278326),(29.674583435058594,41.16152954101574),(29.862083435058594,41.14374923706049),(29.882982254028377,41.09217834472656),(29.848857879638842,41.06917572021507),(29.748725891113565,41.05318450927746),(29.644767761230582,41.00930404663086),(29.496175765991495,41.035736083984375),(29.481319427490405,41.0007019042971),(29.43189430236822,40.97430038452154),(29.419984817504826,40.92051315307623),(29.348457336425952,40.891124725342024),(29.322084426879996,40.85878372192377),(29.261529922485522,40.85514068603521),(29.24763870239275,40.87208175659191),(29.144582748413143,40.90069580078125),(29.09708595275896,40.95013809204113),(29.03152847290056,40.96625137329107),(29.037639617920092,40.97958374023449),(29.02180480957037,40.978195190429915),(29.00597190856945,41.00986099243164),(29.008750915527344,41.02597045898432),(29.051527023315884,41.048194885254134),(29.06597137451172,41.10291671752941),(29.096250534057617,41.11791610717796),(29.070972442627067,41.14319610595709),(29.087083816528377,41.1787490844726),(29.165416717529467,41.224582672119254),(29.256526947021598,41.23541641235357),(28.199028015136832,41.54597091674816),(28.272918701171875,41.49569320678711),(28.63097190856962,41.35013961791992),(28.684305191040153,41.347915649414176),(28.78430557250988,41.30208206176758),(28.81125259399414,41.30541610717779),(28.96597290039074,41.25319290161144),(29.07819366455078,41.254581451416016),(29.11180686950712,41.23819351196289),(29.10958480834961,41.210140228271484),(29.037359237671126,41.15597152709961),(29.07236099243164,41.124862670898665),(29.05708312988287,41.0818061828615),(29.033193588256893,41.0498619079591),(28.975973129272518,41.02152633666992),(28.94013977050804,41.048194885254134),(28.9487495422365,41.057640075683594),(28.944026947021484,41.06458282470709),(28.93625068664562,41.045417785644474),(28.963472366333065,41.02152633666992),(28.986803054809684,41.017082214355526),(28.984863281250114,41.004859924316406),(28.9368057250976,41.00125122070318),(28.875139236450423,40.96847152709961),(28.85014152526867,40.97430419921875),(28.82430458068859,40.95402908325195),(28.76430511474615,40.98152923583979),(28.620138168334904,40.96041488647472),(28.595138549804744,40.97347259521496),(28.588472366333235,41.01763916015625),(28.564027786254883,41.017082214355526),(28.54124832153326,40.984306335449446),(28.407083511352766,41.045417785644474),(28.259582519531648,41.06236267089855),(28.233472824097134,41.07764053344749),(28.123260498046932,41.05986022949247),(28.057348251342773,41.15075302124052),(28.087570190429744,41.21114730834984),(28.15098190307623,41.24227523803734),(28.199129104614258,41.363262176513956),(28.23168945312517,41.499076843261776),(28.179122924804744,41.52955627441423),(28.199028015136832,41.54597091674816)]

    NUMBER_OF_POINTS = signal.num_of_loc
    count = 0
    pcount = 0
    xlist = []
    ylist = []
    #p = gpd.GeoSeries(Polygon(polygonlist))
    #p.plot()

    while NUMBER_OF_POINTS > pcount:
        print(count)
        print(pcount)
        x, y = random_loc(signal)
        p = (x, y)
        if is_inside_polygon(points = polygonlist, p = p):
            pcount += 1
            xlist.append(x)
            ylist.append(y)
        else:
            count -= 1
        
        if count < -1000:
            break

    data = list(zip(xlist, ylist))
    #plt.scatter(xlist, ylist, c='red')
    #plt.show()
    #plt.savefig('foo.png', bbox_inches='tight')

    df = pd.DataFrame(data)

    return df

    df.to_csv('points.csv', index=False, header=False)    
    
def random_loc(signal: Search):
    if signal.is_normal_dist:
        return random.uniform(signal.wb_or_xmean, signal.eb_or_xstd) , random.uniform(signal.nb_or_ymean, signal.sb_or_ystd)

    return random.gauss(signal.wb_or_xmean, signal.eb_or_xstd) , random.gauss(signal.nb_or_ymean, signal.sb_or_ystd)


"""
curl -X 'POST' \
'http://127.0.0.1:8000/v1/search' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"area_name": "string","num_of_loc": 100,"is_normal_dist": false,"wb_or_xmean": 41.00,"eb_or_xstd": 0.07,"nb_or_ymean": 28.95,"sb_or_ystd": 0.23}'
"""
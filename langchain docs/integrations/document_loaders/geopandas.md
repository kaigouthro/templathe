# Geopandas

[Geopandas](https://geopandas.org/en/stable/index.html) is an open-source project to make working with geospatial data in python easier.

GeoPandas extends the datatypes used by pandas to allow spatial operations on geometric types.

Geometric operations are performed by shapely. Geopandas further depends on fiona for file access and matplotlib for plotting.

LLM applications (chat, QA) that utilize geospatial data are an interesting area for exploration.

```bash
pip install sodapy  
 pip install pandas  
 pip install geopandas  

```

```python
import ast  
import pandas as pd  
import geopandas as gpd  
from langchain.document\_loaders import OpenCityDataLoader  

```

Create a GeoPandas dataframe from [`Open City Data`](https://python.langchain.com/docs/integrations/document_loaders/open_city_data) as an example input.

```python
# Load Open City Data  
dataset = "tmnf-yvry" # San Francisco crime data  
loader = OpenCityDataLoader(city\_id="data.sfgov.org", dataset\_id=dataset, limit=5000)  
docs = loader.load()  

```

```python
# Convert list of dictionaries to DataFrame  
df = pd.DataFrame([ast.literal\_eval(d.page\_content) for d in docs])  
  
# Extract latitude and longitude  
df["Latitude"] = df["location"].apply(lambda loc: loc["coordinates"][1])  
df["Longitude"] = df["location"].apply(lambda loc: loc["coordinates"][0])  
  
# Create geopandas DF  
gdf = gpd.GeoDataFrame(  
 df, geometry=gpd.points\_from\_xy(df.Longitude, df.Latitude), crs="EPSG:4326"  
)  
  
# Only keep valid longitudes and latitudes for San Francisco  
gdf = gdf[  
 (gdf["Longitude"] >= -123.173825)  
 & (gdf["Longitude"] <= -122.281780)  
 & (gdf["Latitude"] >= 37.623983)  
 & (gdf["Latitude"] <= 37.929824)  
]  

```

Visualization of the sample of SF crime data.

```python
import matplotlib.pyplot as plt  
  
# Load San Francisco map data  
sf = gpd.read\_file("https://data.sfgov.org/resource/3psu-pn9h.geojson")  
  
# Plot the San Francisco map and the points  
fig, ax = plt.subplots(figsize=(10, 10))  
sf.plot(ax=ax, color="white", edgecolor="black")  
gdf.plot(ax=ax, color="red", markersize=5)  
plt.show()  

```

Load GeoPandas dataframe as a `Document` for downstream processing (embedding, chat, etc).

The `geometry` will be the default `page_content` columns, and all other columns are placed in `metadata`.

But, we can specify the `page_content_column`.

```python
from langchain.document\_loaders import GeoDataFrameLoader  
  
loader = GeoDataFrameLoader(data\_frame=gdf, page\_content\_column="geometry")  
docs = loader.load()  

```

```python
docs[0]  

```

```text
 Document(page\_content='POINT (-122.420084075249 37.7083109744362)', metadata={'pdid': '4133422003074', 'incidntnum': '041334220', 'incident\_code': '03074', 'category': 'ROBBERY', 'descript': 'ROBBERY, BODILY FORCE', 'dayofweek': 'Monday', 'date': '2004-11-22T00:00:00.000', 'time': '17:50', 'pddistrict': 'INGLESIDE', 'resolution': 'NONE', 'address': 'GENEVA AV / SANTOS ST', 'x': '-122.420084075249', 'y': '37.7083109744362', 'location': {'type': 'Point', 'coordinates': [-122.420084075249, 37.7083109744362]}, ':@computed\_region\_26cr\_cadq': '9', ':@computed\_region\_rxqg\_mtj9': '8', ':@computed\_region\_bh8s\_q3mv': '309', ':@computed\_region\_6qbp\_sg9q': nan, ':@computed\_region\_qgnn\_b9vv': nan, ':@computed\_region\_ajp5\_b2md': nan, ':@computed\_region\_yftq\_j783': nan, ':@computed\_region\_p5aj\_wyqh': nan, ':@computed\_region\_fyvs\_ahh9': nan, ':@computed\_region\_6pnf\_4xz7': nan, ':@computed\_region\_jwn9\_ihcz': nan, ':@computed\_region\_9dfj\_4gjx': nan, ':@computed\_region\_4isq\_27mq': nan, ':@computed\_region\_pigm\_ib2e': nan, ':@computed\_region\_9jxd\_iqea': nan, ':@computed\_region\_6ezc\_tdp2': nan, ':@computed\_region\_h4ep\_8xdi': nan, ':@computed\_region\_n4xg\_c4py': nan, ':@computed\_region\_fcz8\_est8': nan, ':@computed\_region\_nqbw\_i6c3': nan, ':@computed\_region\_2dwj\_jsy4': nan, 'Latitude': 37.7083109744362, 'Longitude': -122.420084075249})  

```

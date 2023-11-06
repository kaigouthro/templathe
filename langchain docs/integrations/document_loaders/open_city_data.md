# Open City Data

[Socrata](https://dev.socrata.com/foundry/data.sfgov.org/vw6y-z8j6) provides an API for city open data.

For a dataset such as [SF crime](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry), to to the `API` tab on top right.

That provides you with the `dataset identifier`.

Use the dataset identifier to grab specific tables for a given city_id (`data.sfgov.org`) -

E.g., `vw6y-z8j6` for [SF 311 data](https://dev.socrata.com/foundry/data.sfgov.org/vw6y-z8j6).

E.g., `tmnf-yvry` for [SF Police data](https://dev.socrata.com/foundry/data.sfgov.org/tmnf-yvry).

```bash
pip install sodapy  

```

```python
from langchain.document\_loaders import OpenCityDataLoader  

```

```python
dataset = "vw6y-z8j6" # 311 data  
dataset = "tmnf-yvry" # crime data  
loader = OpenCityDataLoader(city\_id="data.sfgov.org", dataset\_id=dataset, limit=2000)  

```

```python
docs = loader.load()  

```

```text
 WARNING:root:Requests made without an app\_token will be subject to strict throttling limits.  

```

```python
eval(docs[0].page\_content)  

```

```text
 {'pdid': '4133422003074',  
 'incidntnum': '041334220',  
 'incident\_code': '03074',  
 'category': 'ROBBERY',  
 'descript': 'ROBBERY, BODILY FORCE',  
 'dayofweek': 'Monday',  
 'date': '2004-11-22T00:00:00.000',  
 'time': '17:50',  
 'pddistrict': 'INGLESIDE',  
 'resolution': 'NONE',  
 'address': 'GENEVA AV / SANTOS ST',  
 'x': '-122.420084075249',  
 'y': '37.7083109744362',  
 'location': {'type': 'Point',  
 'coordinates': [-122.420084075249, 37.7083109744362]},  
 ':@computed\_region\_26cr\_cadq': '9',  
 ':@computed\_region\_rxqg\_mtj9': '8',  
 ':@computed\_region\_bh8s\_q3mv': '309'}  

```

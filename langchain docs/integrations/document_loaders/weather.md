# Weather

[OpenWeatherMap](https://openweathermap.org/) is an open-source weather service provider

This loader fetches the weather data from the OpenWeatherMap's OneCall API, using the pyowm Python package. You must initialize the loader with your OpenWeatherMap API token and the names of the cities you want the weather data for.

```python
from langchain.document\_loaders import WeatherDataLoader  

```

```python
#!pip install pyowm  

```

```python
# Set API key either by passing it in to constructor directly  
# or by setting the environment variable "OPENWEATHERMAP\_API\_KEY".  
  
from getpass import getpass  
  
OPENWEATHERMAP\_API\_KEY = getpass()  

```

```python
loader = WeatherDataLoader.from\_params(  
 ["chennai", "vellore"], openweathermap\_api\_key=OPENWEATHERMAP\_API\_KEY  
)  

```

```python
documents = loader.load()  
documents  

```

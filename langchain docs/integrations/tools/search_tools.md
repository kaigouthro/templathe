# Search Tools

This notebook shows off usage of various search tools.

```python
from langchain.agents import load\_tools  
from langchain.agents import initialize\_agent  
from langchain.agents import AgentType  
from langchain.llms import OpenAI  

```

```python
llm = OpenAI(temperature=0)  

```

## Google Serper API Wrapper[​](#google-serper-api-wrapper "Direct link to Google Serper API Wrapper")

First, let's try to use the Google Serper API tool.

```python
tools = load\_tools(["google-serper"], llm=llm)  

```

```python
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run("What is the weather in Pomfret?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I should look up the current weather conditions.  
 Action: Search  
 Action Input: "weather in Pomfret"  
 Observation: 37°F  
 Thought: I now know the current temperature in Pomfret.  
 Final Answer: The current temperature in Pomfret is 37°F.  
   
 > Finished chain.  
  
  
  
  
  
 'The current temperature in Pomfret is 37°F.'  

```

## SearchApi[​](#searchapi "Direct link to SearchApi")

Second, let's try SearchApi tool.

```python
tools = load\_tools(["searchapi"], llm=llm)  

```

```python
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run("What is the weather in Pomfret?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out the current weather in Pomfret.  
 Action: searchapi  
 Action Input: "weather in Pomfret"  
 Observation: Thu 14 | Day ... Some clouds this morning will give way to generally sunny skies for the afternoon. High 73F. Winds NW at 5 to 10 mph.  
 Hourly Weather-Pomfret, CT · 1 pm. 71°. 0%. Sunny. Feels Like71°. WindNW 9 mph · 2 pm. 72°. 0%. Sunny. Feels Like72°. WindNW 9 mph · 3 pm. 72°. 0%. Sunny. Feels ...  
 10 Day Weather-Pomfret, VT. As of 4:28 am EDT. Today. 68°/48°. 4%. Thu 14 | Day. 68°. 4%. WNW 10 mph. Some clouds this morning will give way to generally ...  
 Be prepared with the most accurate 10-day forecast for Pomfret, MD with highs, lows, chance of precipitation from The Weather Channel and Weather.com.  
 Current Weather. 10:00 PM. 65°F. RealFeel® 67°. Mostly cloudy. LOCAL HURRICANE TRACKER. Category2. Lee. Late Friday Night - Saturday Afternoon.  
 10 Day Weather-Pomfret, NY. As of 5:09 pm EDT. Tonight. --/55°. 10%. Wed 13 | Night. 55°. 10%. NW 11 mph. Some clouds. Low near 55F.  
 Pomfret CT. Overnight. Overnight: Patchy fog before 3am, then patchy fog after 4am. Otherwise, mostly. Patchy Fog. Low: 58 °F. Thursday.  
 Isolated showers. Mostly cloudy, with a high near 76. Calm wind. Chance of precipitation is 20%. Tonight. Mostly Cloudy. Mostly cloudy, with a ...  
 Partly sunny, with a high near 67. Breezy, with a north wind 18 to 22 mph, with gusts as high as 34 mph. Chance of precipitation is 30%. ... A chance of showers ...  
 Today's Weather - Pomfret, CT ... Patchy fog. Showers. Lows in the upper 50s. Northwest winds around 5 mph. Chance of rain near 100 percent. ... Sunny. Patchy fog ...  
 Thought: I now know the final answer  
 Final Answer: The current weather in Pomfret is mostly cloudy with a high near 67 and a chance of showers. Winds are from the north at 18 to 22 mph with gusts up to 34 mph.  
   
 > Finished chain.  
  
  
  
  
  
 'The current weather in Pomfret is mostly cloudy with a high near 67 and a chance of showers. Winds are from the north at 18 to 22 mph with gusts up to 34 mph.'  

```

## SerpAPI[​](#serpapi "Direct link to SerpAPI")

Now, let's use the SerpAPI tool.

```python
tools = load\_tools(["serpapi"], llm=llm)  

```

```python
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run("What is the weather in Pomfret?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out what the current weather is in Pomfret.  
 Action: Search  
 Action Input: "weather in Pomfret"  
 Observation: {'type': 'weather\_result', 'temperature': '69', 'unit': 'Fahrenheit', 'precipitation': '2%', 'humidity': '90%', 'wind': '1 mph', 'location': 'Pomfret, CT', 'date': 'Sunday 9:00 PM', 'weather': 'Clear'}  
 Thought: I now know the current weather in Pomfret.  
 Final Answer: The current weather in Pomfret is 69 degrees Fahrenheit, 2% precipitation, 90% humidity, and 1 mph wind. It is currently clear.  
   
 > Finished chain.  
  
  
  
  
  
 'The current weather in Pomfret is 69 degrees Fahrenheit, 2% precipitation, 90% humidity, and 1 mph wind. It is currently clear.'  

```

## GoogleSearchAPIWrapper[​](#googlesearchapiwrapper "Direct link to GoogleSearchAPIWrapper")

Now, let's use the official Google Search API Wrapper.

```python
tools = load\_tools(["google-search"], llm=llm)  

```

```python
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run("What is the weather in Pomfret?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I should look up the current weather conditions.  
 Action: Google Search  
 Action Input: "weather in Pomfret"  
 Observation: Showers early becoming a steady light rain later in the day. Near record high temperatures. High around 60F. Winds SW at 10 to 15 mph. Chance of rain 60%. Pomfret, CT Weather Forecast, with current conditions, wind, air quality, and what to expect for the next 3 days. Hourly Weather-Pomfret, CT. As of 12:52 am EST. Special Weather Statement +2 ... Hazardous Weather Conditions. Special Weather Statement ... Pomfret CT. Tonight ... National Digital Forecast Database Maximum Temperature Forecast. Pomfret Center Weather Forecasts. Weather Underground provides local & long-range weather forecasts, weatherreports, maps & tropical weather conditions for ... Pomfret, CT 12 hour by hour weather forecast includes precipitation, temperatures, sky conditions, rain chance, dew-point, relative humidity, wind direction ... North Pomfret Weather Forecasts. Weather Underground provides local & long-range weather forecasts, weatherreports, maps & tropical weather conditions for ... Today's Weather - Pomfret, CT. Dec 31, 2022 4:00 PM. Putnam MS. --. Weather forecast icon. Feels like --. Hi --. Lo --. Pomfret, CT temperature trend for the next 14 Days. Find daytime highs and nighttime lows from TheWeatherNetwork.com. Pomfret, MD Weather Forecast Date: 332 PM EST Wed Dec 28 2022. The area/counties/county of: Charles, including the cites of: St. Charles and Waldorf.  
 Thought: I now know the current weather conditions in Pomfret.  
 Final Answer: Showers early becoming a steady light rain later in the day. Near record high temperatures. High around 60F. Winds SW at 10 to 15 mph. Chance of rain 60%.  
 > Finished AgentExecutor chain.  
  
  
  
  
  
 'Showers early becoming a steady light rain later in the day. Near record high temperatures. High around 60F. Winds SW at 10 to 15 mph. Chance of rain 60%.'  

```

## SearxNG Meta Search Engine[​](#searxng-meta-search-engine "Direct link to SearxNG Meta Search Engine")

Here we will be using a self hosted SearxNG meta search engine.

```python
tools = load\_tools(["searx-search"], searx\_host="http://localhost:8888", llm=llm)  

```

```python
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run("What is the weather in Pomfret")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I should look up the current weather  
 Action: SearX Search  
 Action Input: "weather in Pomfret"  
 Observation: Mainly cloudy with snow showers around in the morning. High around 40F. Winds NNW at 5 to 10 mph. Chance of snow 40%. Snow accumulations less than one inch.  
   
 10 Day Weather - Pomfret, MD As of 1:37 pm EST Today 49°/ 41° 52% Mon 27 | Day 49° 52% SE 14 mph Cloudy with occasional rain showers. High 49F. Winds SE at 10 to 20 mph. Chance of rain 50%....  
   
 10 Day Weather - Pomfret, VT As of 3:51 am EST Special Weather Statement Today 39°/ 32° 37% Wed 01 | Day 39° 37% NE 4 mph Cloudy with snow showers developing for the afternoon. High 39F....  
   
 Pomfret, CT ; Current Weather. 1:06 AM. 35°F · RealFeel® 32° ; TODAY'S WEATHER FORECAST. 3/3. 44°Hi. RealFeel® 50° ; TONIGHT'S WEATHER FORECAST. 3/3. 32°Lo.  
   
 Pomfret, MD Forecast Today Hourly Daily Morning 41° 1% Afternoon 43° 0% Evening 35° 3% Overnight 34° 2% Don't Miss Finally, Here’s Why We Get More Colds and Flu When It’s Cold Coast-To-Coast...  
   
 Pomfret, MD Weather Forecast | AccuWeather Current Weather 5:35 PM 35° F RealFeel® 36° RealFeel Shade™ 36° Air Quality Excellent Wind E 3 mph Wind Gusts 5 mph Cloudy More Details WinterCast...  
   
 Pomfret, VT Weather Forecast | AccuWeather Current Weather 11:21 AM 23° F RealFeel® 27° RealFeel Shade™ 25° Air Quality Fair Wind ESE 3 mph Wind Gusts 7 mph Cloudy More Details WinterCast...  
   
 Pomfret Center, CT Weather Forecast | AccuWeather Daily Current Weather 6:50 PM 39° F RealFeel® 36° Air Quality Fair Wind NW 6 mph Wind Gusts 16 mph Mostly clear More Details WinterCast...  
   
 12:00 pm · Feels Like36° · WindN 5 mph · Humidity43% · UV Index3 of 10 · Cloud Cover65% · Rain Amount0 in ...  
   
 Pomfret Center, CT Weather Conditions | Weather Underground star Popular Cities San Francisco, CA 49 °F Clear Manhattan, NY 37 °F Fair Schiller Park, IL (60176) warning39 °F Mostly Cloudy...  
 Thought: I now know the final answer  
 Final Answer: The current weather in Pomfret is mainly cloudy with snow showers around in the morning. The temperature is around 40F with winds NNW at 5 to 10 mph. Chance of snow is 40%.  
   
 > Finished chain.  
  
  
  
  
  
 'The current weather in Pomfret is mainly cloudy with snow showers around in the morning. The temperature is around 40F with winds NNW at 5 to 10 mph. Chance of snow is 40%.'  

```

- [Google Serper API Wrapper](#google-serper-api-wrapper)
- [SearchApi](#searchapi)
- [SerpAPI](#serpapi)
- [GoogleSearchAPIWrapper](#googlesearchapiwrapper)
- [SearxNG Meta Search Engine](#searxng-meta-search-engine)

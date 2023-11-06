# OpenAI Multi Functions Agent

This notebook showcases using an agent that uses the OpenAI functions ability to respond to the prompts of the user using a Large Language Model.

Install `openai`, `google-search-results` packages which are required as the LangChain packages call them internally.

```bash
pip install openai google-search-results  

```

```python
from langchain.utilities import SerpAPIWrapper  
from langchain.agents import initialize\_agent, Tool  
from langchain.agents import AgentType  
from langchain.chat\_models import ChatOpenAI  

```

The agent is given the ability to perform search functionalities with the respective tool

`SerpAPIWrapper`:

This initializes the `SerpAPIWrapper` for search functionality (search).

```python
import getpass  
import os  
  
os.environ["SERPAPI\_API\_KEY"] = getpass.getpass()  

```

```text
 ········  

```

```python
# Initialize the OpenAI language model  
# Replace <your\_api\_key> in openai\_api\_key="<your\_api\_key>" with your actual OpenAI key.  
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")  
  
# Initialize the SerpAPIWrapper for search functionality  
# Replace <your\_api\_key> in serpapi\_api\_key="<your\_api\_key>" with your actual SerpAPI key.  
search = SerpAPIWrapper()  
  
# Define a list of tools offered by the agent  
tools = [  
 Tool(  
 name="Search",  
 func=search.run,  
 description="Useful when you need to answer questions about current events. You should ask targeted questions.",  
 ),  
]  

```

```python
mrkl = initialize\_agent(  
 tools, llm, agent=AgentType.OPENAI\_MULTI\_FUNCTIONS, verbose=True  
)  

```

```python
# Do this so we can see exactly what's going on under the hood  
from langchain.globals import set\_debug  
  
set\_debug(True)  

```

```python
mrkl.run("What is the weather in LA and SF?")  

```

```text
 [chain/start] [1:chain:AgentExecutor] Entering Chain run with input:  
 {  
 "input": "What is the weather in LA and SF?"  
 }  
 [llm/start] [1:chain:AgentExecutor > 2:llm:ChatOpenAI] Entering LLM run with input:  
 {  
 "prompts": [  
 "System: You are a helpful AI assistant.\nHuman: What is the weather in LA and SF?"  
 ]  
 }  
 [llm/end] [1:chain:AgentExecutor > 2:llm:ChatOpenAI] [2.91s] Exiting LLM run with output:  
 {  
 "generations": [  
 [  
 {  
 "text": "",  
 "generation\_info": null,  
 "message": {  
 "content": "",  
 "additional\_kwargs": {  
 "function\_call": {  
 "name": "tool\_selection",  
 "arguments": "{\n \"actions\": [\n {\n \"action\_name\": \"Search\",\n \"action\": {\n \"tool\_input\": \"weather in Los Angeles\"\n }\n },\n {\n \"action\_name\": \"Search\",\n \"action\": {\n \"tool\_input\": \"weather in San Francisco\"\n }\n }\n ]\n}"  
 }  
 },  
 "example": false  
 }  
 }  
 ]  
 ],  
 "llm\_output": {  
 "token\_usage": {  
 "prompt\_tokens": 81,  
 "completion\_tokens": 75,  
 "total\_tokens": 156  
 },  
 "model\_name": "gpt-3.5-turbo-0613"  
 },  
 "run": null  
 }  
 [tool/start] [1:chain:AgentExecutor > 3:tool:Search] Entering Tool run with input:  
 "{'tool\_input': 'weather in Los Angeles'}"  
 [tool/end] [1:chain:AgentExecutor > 3:tool:Search] [608.693ms] Exiting Tool run with output:  
 "Mostly cloudy early, then sunshine for the afternoon. High 76F. Winds SW at 5 to 10 mph. Humidity59%."  
 [tool/start] [1:chain:AgentExecutor > 4:tool:Search] Entering Tool run with input:  
 "{'tool\_input': 'weather in San Francisco'}"  
 [tool/end] [1:chain:AgentExecutor > 4:tool:Search] [517.475ms] Exiting Tool run with output:  
 "Partly cloudy this evening, then becoming cloudy after midnight. Low 53F. Winds WSW at 10 to 20 mph. Humidity83%."  
 [llm/start] [1:chain:AgentExecutor > 5:llm:ChatOpenAI] Entering LLM run with input:  
 {  
 "prompts": [  
 "System: You are a helpful AI assistant.\nHuman: What is the weather in LA and SF?\nAI: {'name': 'tool\_selection', 'arguments': '{\\n \"actions\": [\\n {\\n \"action\_name\": \"Search\",\\n \"action\": {\\n \"tool\_input\": \"weather in Los Angeles\"\\n }\\n },\\n {\\n \"action\_name\": \"Search\",\\n \"action\": {\\n \"tool\_input\": \"weather in San Francisco\"\\n }\\n }\\n ]\\n}'}\nFunction: Mostly cloudy early, then sunshine for the afternoon. High 76F. Winds SW at 5 to 10 mph. Humidity59%.\nAI: {'name': 'tool\_selection', 'arguments': '{\\n \"actions\": [\\n {\\n \"action\_name\": \"Search\",\\n \"action\": {\\n \"tool\_input\": \"weather in Los Angeles\"\\n }\\n },\\n {\\n \"action\_name\": \"Search\",\\n \"action\": {\\n \"tool\_input\": \"weather in San Francisco\"\\n }\\n }\\n ]\\n}'}\nFunction: Partly cloudy this evening, then becoming cloudy after midnight. Low 53F. Winds WSW at 10 to 20 mph. Humidity83%."  
 ]  
 }  
 [llm/end] [1:chain:AgentExecutor > 5:llm:ChatOpenAI] [2.33s] Exiting LLM run with output:  
 {  
 "generations": [  
 [  
 {  
 "text": "The weather in Los Angeles is mostly cloudy with a high of 76°F and a humidity of 59%. The weather in San Francisco is partly cloudy in the evening, becoming cloudy after midnight, with a low of 53°F and a humidity of 83%.",  
 "generation\_info": null,  
 "message": {  
 "content": "The weather in Los Angeles is mostly cloudy with a high of 76°F and a humidity of 59%. The weather in San Francisco is partly cloudy in the evening, becoming cloudy after midnight, with a low of 53°F and a humidity of 83%.",  
 "additional\_kwargs": {},  
 "example": false  
 }  
 }  
 ]  
 ],  
 "llm\_output": {  
 "token\_usage": {  
 "prompt\_tokens": 307,  
 "completion\_tokens": 54,  
 "total\_tokens": 361  
 },  
 "model\_name": "gpt-3.5-turbo-0613"  
 },  
 "run": null  
 }  
 [chain/end] [1:chain:AgentExecutor] [6.37s] Exiting Chain run with output:  
 {  
 "output": "The weather in Los Angeles is mostly cloudy with a high of 76°F and a humidity of 59%. The weather in San Francisco is partly cloudy in the evening, becoming cloudy after midnight, with a low of 53°F and a humidity of 83%."  
 }  
  
  
  
  
  
 'The weather in Los Angeles is mostly cloudy with a high of 76°F and a humidity of 59%. The weather in San Francisco is partly cloudy in the evening, becoming cloudy after midnight, with a low of 53°F and a humidity of 83%.'  

```

## Configuring max iteration behavior[​](#configuring-max-iteration-behavior "Direct link to Configuring max iteration behavior")

To make sure that our agent doesn't get stuck in excessively long loops, we can set `max_iterations`. We can also set an early stopping method, which will determine our agent's behavior once the number of max iterations is hit. By default, the early stopping uses method `force` which just returns that constant string. Alternatively, you could specify method `generate` which then does one FINAL pass through the LLM to generate an output.

```python
mrkl = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.OPENAI\_FUNCTIONS,  
 verbose=True,  
 max\_iterations=2,  
 early\_stopping\_method="generate",  
)  

```

```python
mrkl.run("What is the weather in NYC today, yesterday, and the day before?")  

```

```text
 [chain/start] [1:chain:AgentExecutor] Entering Chain run with input:  
 {  
 "input": "What is the weather in NYC today, yesterday, and the day before?"  
 }  
 [llm/start] [1:chain:AgentExecutor > 2:llm:ChatOpenAI] Entering LLM run with input:  
 {  
 "prompts": [  
 "System: You are a helpful AI assistant.\nHuman: What is the weather in NYC today, yesterday, and the day before?"  
 ]  
 }  
 [llm/end] [1:chain:AgentExecutor > 2:llm:ChatOpenAI] [1.27s] Exiting LLM run with output:  
 {  
 "generations": [  
 [  
 {  
 "text": "",  
 "generation\_info": null,  
 "message": {  
 "lc": 1,  
 "type": "constructor",  
 "id": [  
 "langchain",  
 "schema",  
 "messages",  
 "AIMessage"  
 ],  
 "kwargs": {  
 "content": "",  
 "additional\_kwargs": {  
 "function\_call": {  
 "name": "Search",  
 "arguments": "{\n \"query\": \"weather in NYC today\"\n}"  
 }  
 }  
 }  
 }  
 }  
 ]  
 ],  
 "llm\_output": {  
 "token\_usage": {  
 "prompt\_tokens": 79,  
 "completion\_tokens": 17,  
 "total\_tokens": 96  
 },  
 "model\_name": "gpt-3.5-turbo-0613"  
 },  
 "run": null  
 }  
 [tool/start] [1:chain:AgentExecutor > 3:tool:Search] Entering Tool run with input:  
 "{'query': 'weather in NYC today'}"  
 [tool/end] [1:chain:AgentExecutor > 3:tool:Search] [3.84s] Exiting Tool run with output:  
 "10:00 am · Feels Like85° · WindSE 4 mph · Humidity78% · UV Index3 of 11 · Cloud Cover81% · Rain Amount0 in ..."  
 [llm/start] [1:chain:AgentExecutor > 4:llm:ChatOpenAI] Entering LLM run with input:  
 {  
 "prompts": [  
 "System: You are a helpful AI assistant.\nHuman: What is the weather in NYC today, yesterday, and the day before?\nAI: {'name': 'Search', 'arguments': '{\\n \"query\": \"weather in NYC today\"\\n}'}\nFunction: 10:00 am · Feels Like85° · WindSE 4 mph · Humidity78% · UV Index3 of 11 · Cloud Cover81% · Rain Amount0 in ..."  
 ]  
 }  
 [llm/end] [1:chain:AgentExecutor > 4:llm:ChatOpenAI] [1.24s] Exiting LLM run with output:  
 {  
 "generations": [  
 [  
 {  
 "text": "",  
 "generation\_info": null,  
 "message": {  
 "lc": 1,  
 "type": "constructor",  
 "id": [  
 "langchain",  
 "schema",  
 "messages",  
 "AIMessage"  
 ],  
 "kwargs": {  
 "content": "",  
 "additional\_kwargs": {  
 "function\_call": {  
 "name": "Search",  
 "arguments": "{\n \"query\": \"weather in NYC yesterday\"\n}"  
 }  
 }  
 }  
 }  
 }  
 ]  
 ],  
 "llm\_output": {  
 "token\_usage": {  
 "prompt\_tokens": 142,  
 "completion\_tokens": 17,  
 "total\_tokens": 159  
 },  
 "model\_name": "gpt-3.5-turbo-0613"  
 },  
 "run": null  
 }  
 [tool/start] [1:chain:AgentExecutor > 5:tool:Search] Entering Tool run with input:  
 "{'query': 'weather in NYC yesterday'}"  
 [tool/end] [1:chain:AgentExecutor > 5:tool:Search] [1.15s] Exiting Tool run with output:  
 "New York Temperature Yesterday. Maximum temperature yesterday: 81 °F (at 1:51 pm) Minimum temperature yesterday: 72 °F (at 7:17 pm) Average temperature ..."  
 [llm/start] [1:llm:ChatOpenAI] Entering LLM run with input:  
 {  
 "prompts": [  
 "System: You are a helpful AI assistant.\nHuman: What is the weather in NYC today, yesterday, and the day before?\nAI: {'name': 'Search', 'arguments': '{\\n \"query\": \"weather in NYC today\"\\n}'}\nFunction: 10:00 am · Feels Like85° · WindSE 4 mph · Humidity78% · UV Index3 of 11 · Cloud Cover81% · Rain Amount0 in ...\nAI: {'name': 'Search', 'arguments': '{\\n \"query\": \"weather in NYC yesterday\"\\n}'}\nFunction: New York Temperature Yesterday. Maximum temperature yesterday: 81 °F (at 1:51 pm) Minimum temperature yesterday: 72 °F (at 7:17 pm) Average temperature ..."  
 ]  
 }  
 [llm/end] [1:llm:ChatOpenAI] [2.68s] Exiting LLM run with output:  
 {  
 "generations": [  
 [  
 {  
 "text": "Today in NYC, the weather is currently 85°F with a southeast wind of 4 mph. The humidity is at 78% and there is 81% cloud cover. There is no rain expected today.\n\nYesterday in NYC, the maximum temperature was 81°F at 1:51 pm, and the minimum temperature was 72°F at 7:17 pm.\n\nFor the day before yesterday, I do not have the specific weather information.",  
 "generation\_info": null,  
 "message": {  
 "lc": 1,  
 "type": "constructor",  
 "id": [  
 "langchain",  
 "schema",  
 "messages",  
 "AIMessage"  
 ],  
 "kwargs": {  
 "content": "Today in NYC, the weather is currently 85°F with a southeast wind of 4 mph. The humidity is at 78% and there is 81% cloud cover. There is no rain expected today.\n\nYesterday in NYC, the maximum temperature was 81°F at 1:51 pm, and the minimum temperature was 72°F at 7:17 pm.\n\nFor the day before yesterday, I do not have the specific weather information.",  
 "additional\_kwargs": {}  
 }  
 }  
 }  
 ]  
 ],  
 "llm\_output": {  
 "token\_usage": {  
 "prompt\_tokens": 160,  
 "completion\_tokens": 91,  
 "total\_tokens": 251  
 },  
 "model\_name": "gpt-3.5-turbo-0613"  
 },  
 "run": null  
 }  
 [chain/end] [1:chain:AgentExecutor] [10.18s] Exiting Chain run with output:  
 {  
 "output": "Today in NYC, the weather is currently 85°F with a southeast wind of 4 mph. The humidity is at 78% and there is 81% cloud cover. There is no rain expected today.\n\nYesterday in NYC, the maximum temperature was 81°F at 1:51 pm, and the minimum temperature was 72°F at 7:17 pm.\n\nFor the day before yesterday, I do not have the specific weather information."  
 }  
  
  
  
  
  
 'Today in NYC, the weather is currently 85°F with a southeast wind of 4 mph. The humidity is at 78% and there is 81% cloud cover. There is no rain expected today.\n\nYesterday in NYC, the maximum temperature was 81°F at 1:51 pm, and the minimum temperature was 72°F at 7:17 pm.\n\nFor the day before yesterday, I do not have the specific weather information.'  

```

Notice that we never get around to looking up the weather the day before yesterday, due to hitting our `max_iterations` limit.

- [Configuring max iteration behavior](#configuring-max-iteration-behavior)

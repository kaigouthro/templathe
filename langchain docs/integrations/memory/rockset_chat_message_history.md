# Rockset

[Rockset](https://rockset.com/product/) is a real-time analytics database service for serving low latency, high concurrency analytical queries at scale. It builds a Converged Index™ on structured and semi-structured data with an efficient store for vector embeddings. Its support for running SQL on schemaless data makes it a perfect choice for running vector search with metadata filters.

This notebook goes over how to use [Rockset](https://rockset.com/docs) to store chat message history.

## Setting up[​](#setting-up "Direct link to Setting up")

```bash
pip install rockset  

```

To begin, with get your API key from the [Rockset console](https://console.rockset.com/apikeys). Find your API region for the Rockset [API reference](https://rockset.com/docs/rest-api#introduction).

## Example[​](#example "Direct link to Example")

```python
from langchain.memory.chat\_message\_histories import RocksetChatMessageHistory  
from rockset import RocksetClient, Regions  
  
history = RocksetChatMessageHistory(  
 session\_id="MySession",  
 client=RocksetClient(  
 api\_key="YOUR API KEY",   
 host=Regions.usw2a1 # us-west-2 Oregon  
 ),  
 collection="langchain\_demo",  
 sync=True  
)  
history.add\_user\_message("hi!")  
history.add\_ai\_message("whats up?")  
print(history.messages)  

```

The output should be something like:

```python
[  
 HumanMessage(content='hi!', additional\_kwargs={'id': '2e62f1c2-e9f7-465e-b551-49bae07fe9f0'}, example=False),   
 AIMessage(content='whats up?', additional\_kwargs={'id': 'b9be8eda-4c18-4cf8-81c3-e91e876927d0'}, example=False)  
]  
  

```

- [Setting up](#setting-up)
- [Example](#example)

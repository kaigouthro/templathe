# DataForSeo

This notebook demonstrates how to use the `DataForSeo API` to obtain search engine results. The `DataForSeo API` retrieves `SERP` from most popular search engines like `Google`, `Bing`, `Yahoo`. It also allows to get SERPs from different search engine types like `Maps`, `News`, `Events`, etc.

```python
from langchain.utilities.dataforseo\_api\_search import DataForSeoAPIWrapper  

```

## Setting up the API credentials[​](#setting-up-the-api-credentials "Direct link to Setting up the API credentials")

You can obtain your API credentials by registering on the `DataForSeo` website.

```python
import os  
  
os.environ["DATAFORSEO\_LOGIN"] = "your\_api\_access\_username"  
os.environ["DATAFORSEO\_PASSWORD"] = "your\_api\_access\_password"  
  
wrapper = DataForSeoAPIWrapper()  

```

The run method will return the first result snippet from one of the following elements: answer_box, knowledge_graph, featured_snippet, shopping, organic.

```python
wrapper.run("Weather in Los Angeles")  

```

## The Difference Between `run` and `results`[​](#the-difference-between-run-and-results "Direct link to the-difference-between-run-and-results")

`run` and `results` are two methods provided by the `DataForSeoAPIWrapper` class.

The `run` method executes the search and returns the first result snippet from the answer box, knowledge graph, featured snippet, shopping, or organic results. These elements are sorted by priority from highest to lowest.

The `results` method returns a JSON response configured according to the parameters set in the wrapper. This allows for more flexibility in terms of what data you want to return from the API.

## Getting Results as JSON[​](#getting-results-as-json "Direct link to Getting Results as JSON")

You can customize the result types and fields you want to return in the JSON response. You can also set a maximum count for the number of top results to return.

```python
json\_wrapper = DataForSeoAPIWrapper(  
 json\_result\_types=["organic", "knowledge\_graph", "answer\_box"],  
 json\_result\_fields=["type", "title", "description", "text"],  
 top\_count=3,  
)  

```

```python
json\_wrapper.results("Bill Gates")  

```

## Customizing Location and Language[​](#customizing-location-and-language "Direct link to Customizing Location and Language")

You can specify the location and language of your search results by passing additional parameters to the API wrapper.

```python
customized\_wrapper = DataForSeoAPIWrapper(  
 top\_count=10,  
 json\_result\_types=["organic", "local\_pack"],  
 json\_result\_fields=["title", "description", "type"],  
 params={"location\_name": "Germany", "language\_code": "en"},  
)  
customized\_wrapper.results("coffee near me")  

```

## Customizing the Search Engine[​](#customizing-the-search-engine "Direct link to Customizing the Search Engine")

You can also specify the search engine you want to use.

```python
customized\_wrapper = DataForSeoAPIWrapper(  
 top\_count=10,  
 json\_result\_types=["organic", "local\_pack"],  
 json\_result\_fields=["title", "description", "type"],  
 params={"location\_name": "Germany", "language\_code": "en", "se\_name": "bing"},  
)  
customized\_wrapper.results("coffee near me")  

```

## Customizing the Search Type[​](#customizing-the-search-type "Direct link to Customizing the Search Type")

The API wrapper also allows you to specify the type of search you want to perform. For example, you can perform a maps search.

```python
maps\_search = DataForSeoAPIWrapper(  
 top\_count=10,  
 json\_result\_fields=["title", "value", "address", "rating", "type"],  
 params={  
 "location\_coordinate": "52.512,13.36,12z",  
 "language\_code": "en",  
 "se\_type": "maps",  
 },  
)  
maps\_search.results("coffee near me")  

```

## Integration with Langchain Agents[​](#integration-with-langchain-agents "Direct link to Integration with Langchain Agents")

You can use the `Tool` class from the `langchain.agents` module to integrate the `DataForSeoAPIWrapper` with a langchain agent. The `Tool` class encapsulates a function that the agent can call.

```python
from langchain.agents import Tool  
  
search = DataForSeoAPIWrapper(  
 top\_count=3,  
 json\_result\_types=["organic"],  
 json\_result\_fields=["title", "description", "type"],  
)  
tool = Tool(  
 name="google-search-answer",  
 description="My new answer tool",  
 func=search.run,  
)  
json\_tool = Tool(  
 name="google-search-json",  
 description="My new json tool",  
 func=search.results,  
)  

```

- [Setting up the API credentials](#setting-up-the-api-credentials)
- [The Difference Between `run` and `results`](#the-difference-between-run-and-results)
- [Getting Results as JSON](#getting-results-as-json)
- [Customizing Location and Language](#customizing-location-and-language)
- [Customizing the Search Engine](#customizing-the-search-engine)
- [Customizing the Search Type](#customizing-the-search-type)
- [Integration with Langchain Agents](#integration-with-langchain-agents)

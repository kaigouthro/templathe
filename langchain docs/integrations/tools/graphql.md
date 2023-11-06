# GraphQL

[GraphQL](https://graphql.org/) is a query language for APIs and a runtime for executing those queries against your data. `GraphQL` provides a complete and understandable description of the data in your API, gives clients the power to ask for exactly what they need and nothing more, makes it easier to evolve APIs over time, and enables powerful developer tools.

By including a `BaseGraphQLTool` in the list of tools provided to an Agent, you can grant your Agent the ability to query data from GraphQL APIs for any purposes you need.

This Jupyter Notebook demonstrates how to use the `GraphQLAPIWrapper` component with an Agent.

In this example, we'll be using the public `Star Wars GraphQL API` available at the following endpoint: <https://swapi-graphql.netlify.app/.netlify/functions/index>.

First, you need to install `httpx` and `gql` Python packages.

```python
pip install httpx gql > /dev/null  

```

Now, let's create a BaseGraphQLTool instance with the specified Star Wars API endpoint and initialize an Agent with the tool.

```python
from langchain.llms import OpenAI  
from langchain.agents import load\_tools, initialize\_agent, AgentType  
from langchain.utilities import GraphQLAPIWrapper  
  
llm = OpenAI(temperature=0)  
  
tools = load\_tools(  
 ["graphql"],  
 graphql\_endpoint="https://swapi-graphql.netlify.app/.netlify/functions/index",  
)  
  
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

Now, we can use the Agent to run queries against the Star Wars GraphQL API. Let's ask the Agent to list all the Star Wars films and their release dates.

```python
graphql\_fields = """allFilms {  
 films {  
 title  
 director  
 releaseDate  
 speciesConnection {  
 species {  
 name  
 classification  
 homeworld {  
 name  
 }  
 }  
 }  
 }  
 }  
  
"""  
  
suffix = "Search for the titles of all the stawars films stored in the graphql database that has this schema "  
  
  
agent.run(suffix + graphql\_fields)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to query the graphql database to get the titles of all the star wars films  
 Action: query\_graphql  
 Action Input: query { allFilms { films { title } } }  
 Observation: "{\n \"allFilms\": {\n \"films\": [\n {\n \"title\": \"A New Hope\"\n },\n {\n \"title\": \"The Empire Strikes Back\"\n },\n {\n \"title\": \"Return of the Jedi\"\n },\n {\n \"title\": \"The Phantom Menace\"\n },\n {\n \"title\": \"Attack of the Clones\"\n },\n {\n \"title\": \"Revenge of the Sith\"\n }\n ]\n }\n}"  
 Thought: I now know the titles of all the star wars films  
 Final Answer: The titles of all the star wars films are: A New Hope, The Empire Strikes Back, Return of the Jedi, The Phantom Menace, Attack of the Clones, and Revenge of the Sith.  
   
 > Finished chain.  
  
  
  
  
  
 'The titles of all the star wars films are: A New Hope, The Empire Strikes Back, Return of the Jedi, The Phantom Menace, Attack of the Clones, and Revenge of the Sith.'  

```

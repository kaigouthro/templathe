# Natural Language APIs

`Natural Language API` Toolkits (`NLAToolkits`) permit LangChain Agents to efficiently plan and combine calls across endpoints.

This notebook demonstrates a sample composition of the `Speak`, `Klarna`, and `Spoonacluar` APIs.

For a detailed walkthrough of the OpenAPI chains wrapped within the NLAToolkit, see the [OpenAPI Operation Chain](/docs/use_cases/apis/openapi.html) notebook.

### First, import dependencies and load the LLM[​](#first-import-dependencies-and-load-the-llm "Direct link to First, import dependencies and load the LLM")

```python
from typing import List, Optional  
from langchain.chains import LLMChain  
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
from langchain.requests import Requests  
from langchain.tools import APIOperation, OpenAPISpec  
from langchain.agents import AgentType, Tool, initialize\_agent  
from langchain.agents.agent\_toolkits import NLAToolkit  

```

```python
# Select the LLM to use. Here, we use text-davinci-003  
llm = OpenAI(  
 temperature=0, max\_tokens=700  
) # You can swap between different core LLM's here.  

```

### Next, load the Natural Language API Toolkits[​](#next-load-the-natural-language-api-toolkits "Direct link to Next, load the Natural Language API Toolkits")

```python
speak\_toolkit = NLAToolkit.from\_llm\_and\_url(llm, "https://api.speak.com/openapi.yaml")  
klarna\_toolkit = NLAToolkit.from\_llm\_and\_url(  
 llm, "https://www.klarna.com/us/shopping/public/openai/v0/api-docs/"  
)  

```

```text
 Attempting to load an OpenAPI 3.0.1 spec. This may result in degraded performance. Convert your OpenAPI spec to 3.1.\* spec for better support.  
 Attempting to load an OpenAPI 3.0.1 spec. This may result in degraded performance. Convert your OpenAPI spec to 3.1.\* spec for better support.  
 Attempting to load an OpenAPI 3.0.1 spec. This may result in degraded performance. Convert your OpenAPI spec to 3.1.\* spec for better support.  

```

### Create the Agent[​](#create-the-agent "Direct link to Create the Agent")

```python
# Slightly tweak the instructions from the default agent  
openapi\_format\_instructions = """Use the following format:  
  
Question: the input question you must answer  
Thought: you should always think about what to do  
Action: the action to take, should be one of [{tool\_names}]  
Action Input: what to instruct the AI Action representative.  
Observation: The Agent's response  
... (this Thought/Action/Action Input/Observation can repeat N times)  
Thought: I now know the final answer. User can't see any of my observations, API responses, links, or tools.  
Final Answer: the final answer to the original input question with the right amount of detail  
  
When responding with your Final Answer, remember that the person you are responding to CANNOT see any of your Thought/Action/Action Input/Observations, so if there is any relevant information there you need to include it explicitly in your response."""  

```

```python
natural\_language\_tools = speak\_toolkit.get\_tools() + klarna\_toolkit.get\_tools()  
mrkl = initialize\_agent(  
 natural\_language\_tools,  
 llm,  
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
 agent\_kwargs={"format\_instructions": openapi\_format\_instructions},  
)  

```

```python
mrkl.run(  
 "I have an end of year party for my Italian class and have to buy some Italian clothes for it"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find out what kind of Italian clothes are available  
 Action: Open\_AI\_Klarna\_product\_Api.productsUsingGET  
 Action Input: Italian clothes  
 Observation: The API response contains two products from the Alé brand in Italian Blue. The first is the Alé Colour Block Short Sleeve Jersey Men - Italian Blue, which costs $86.49, and the second is the Alé Dolid Flash Jersey Men - Italian Blue, which costs $40.00.  
 Thought: I now know what kind of Italian clothes are available and how much they cost.  
 Final Answer: You can buy two products from the Alé brand in Italian Blue for your end of year party. The Alé Colour Block Short Sleeve Jersey Men - Italian Blue costs $86.49, and the Alé Dolid Flash Jersey Men - Italian Blue costs $40.00.  
   
 > Finished chain.  
  
  
  
  
  
 'You can buy two products from the Alé brand in Italian Blue for your end of year party. The Alé Colour Block Short Sleeve Jersey Men - Italian Blue costs $86.49, and the Alé Dolid Flash Jersey Men - Italian Blue costs $40.00.'  

```

### Use Auth and add more Endpoints[​](#use-auth-and-add-more-endpoints "Direct link to Use Auth and add more Endpoints")

Some endpoints may require user authentication via things like access tokens. Here we show how to pass in the authentication information via the `Requests` wrapper object.

Since each NLATool exposes a concisee natural language interface to its wrapped API, the top level conversational agent has an easier job incorporating each endpoint to satisfy a user's request.

**Adding the Spoonacular endpoints.**

1. Go to the [Spoonacular API Console](https://spoonacular.com/food-api/console#Profile) and make a free account.
1. Click on `Profile` and copy your API key below.

```python
spoonacular\_api\_key = "" # Copy from the API Console  

```

```python
requests = Requests(headers={"x-api-key": spoonacular\_api\_key})  
spoonacular\_toolkit = NLAToolkit.from\_llm\_and\_url(  
 llm,  
 "https://spoonacular.com/application/frontend/downloads/spoonacular-openapi-3.json",  
 requests=requests,  
 max\_text\_length=1800, # If you want to truncate the response text  
)  

```

```text
 Attempting to load an OpenAPI 3.0.0 spec. This may result in degraded performance. Convert your OpenAPI spec to 3.1.\* spec for better support.  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Accept. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Accept. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Accept. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Accept. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Accept. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Accept. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Accept. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Accept. Valid values are ['path', 'query'] Ignoring optional parameter  
 Unsupported APIPropertyLocation "header" for parameter Content-Type. Valid values are ['path', 'query'] Ignoring optional parameter  

```

```python
natural\_language\_api\_tools = (  
 speak\_toolkit.get\_tools()  
 + klarna\_toolkit.get\_tools()  
 + spoonacular\_toolkit.get\_tools()[:30]  
)  
print(f"{len(natural\_language\_api\_tools)} tools loaded.")  

```

```text
 34 tools loaded.  

```

```python
# Create an agent with the new tools  
mrkl = initialize\_agent(  
 natural\_language\_api\_tools,  
 llm,  
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
 agent\_kwargs={"format\_instructions": openapi\_format\_instructions},  
)  

```

```python
# Make the query more complex!  
user\_input = (  
 "I'm learning Italian, and my language class is having an end of year party... "  
 " Could you help me find an Italian outfit to wear and"  
 " an appropriate recipe to prepare so I can present for the class in Italian?"  
)  

```

```python
mrkl.run(user\_input)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find a recipe and an outfit that is Italian-themed.  
 Action: spoonacular\_API.searchRecipes  
 Action Input: Italian  
 Observation: The API response contains 10 Italian recipes, including Turkey Tomato Cheese Pizza, Broccolini Quinoa Pilaf, Bruschetta Style Pork & Pasta, Salmon Quinoa Risotto, Italian Tuna Pasta, Roasted Brussels Sprouts With Garlic, Asparagus Lemon Risotto, Italian Steamed Artichokes, Crispy Italian Cauliflower Poppers Appetizer, and Pappa Al Pomodoro.  
 Thought: I need to find an Italian-themed outfit.  
 Action: Open\_AI\_Klarna\_product\_Api.productsUsingGET  
 Action Input: Italian  
 Observation: I found 10 products related to 'Italian' in the API response. These products include Italian Gold Sparkle Perfectina Necklace - Gold, Italian Design Miami Cuban Link Chain Necklace - Gold, Italian Gold Miami Cuban Link Chain Necklace - Gold, Italian Gold Herringbone Necklace - Gold, Italian Gold Claddagh Ring - Gold, Italian Gold Herringbone Chain Necklace - Gold, Garmin QuickFit 22mm Italian Vacchetta Leather Band, Macy's Italian Horn Charm - Gold, Dolce & Gabbana Light Blue Italian Love Pour Homme EdT 1.7 fl oz.  
 Thought: I now know the final answer.  
 Final Answer: To present for your Italian language class, you could wear an Italian Gold Sparkle Perfectina Necklace - Gold, an Italian Design Miami Cuban Link Chain Necklace - Gold, or an Italian Gold Miami Cuban Link Chain Necklace - Gold. For a recipe, you could make Turkey Tomato Cheese Pizza, Broccolini Quinoa Pilaf, Bruschetta Style Pork & Pasta, Salmon Quinoa Risotto, Italian Tuna Pasta, Roasted Brussels Sprouts With Garlic, Asparagus Lemon Risotto, Italian Steamed Artichokes, Crispy Italian Cauliflower Poppers Appetizer, or Pappa Al Pomodoro.  
   
 > Finished chain.  
  
  
  
  
  
 'To present for your Italian language class, you could wear an Italian Gold Sparkle Perfectina Necklace - Gold, an Italian Design Miami Cuban Link Chain Necklace - Gold, or an Italian Gold Miami Cuban Link Chain Necklace - Gold. For a recipe, you could make Turkey Tomato Cheese Pizza, Broccolini Quinoa Pilaf, Bruschetta Style Pork & Pasta, Salmon Quinoa Risotto, Italian Tuna Pasta, Roasted Brussels Sprouts With Garlic, Asparagus Lemon Risotto, Italian Steamed Artichokes, Crispy Italian Cauliflower Poppers Appetizer, or Pappa Al Pomodoro.'  

```

## Thank you![​](#thank-you "Direct link to Thank you!")

```python
natural\_language\_api\_tools[1].run(  
 "Tell the LangChain audience to 'enjoy the meal' in Italian, please!"  
)  

```

```text
 "In Italian, you can say 'Buon appetito' to someone to wish them to enjoy their meal. This phrase is commonly used in Italy when someone is about to eat, often at the beginning of a meal. It's similar to saying 'Bon appétit' in French or 'Guten Appetit' in German."  

```

- [First, import dependencies and load the LLM](#first-import-dependencies-and-load-the-llm)
- [Next, load the Natural Language API Toolkits](#next-load-the-natural-language-api-toolkits)
- [Create the Agent](#create-the-agent)
- [Use Auth and add more Endpoints](#use-auth-and-add-more-endpoints)
- [Thank you!](#thank-you)

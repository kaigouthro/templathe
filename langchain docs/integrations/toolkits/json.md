# JSON

This notebook showcases an agent interacting with large `JSON/dict` objects.
This is useful when you want to answer questions about a JSON blob that's too large to fit in the context window of an LLM. The agent is able to iteratively explore the blob to find what it needs to answer the user's question.

In the below example, we are using the OpenAPI spec for the OpenAI API, which you can find [here](https://github.com/openai/openai-openapi/blob/master/openapi.yaml).

We will use the JSON agent to answer some questions about the API spec.

## Initialization[​](#initialization "Direct link to Initialization")

```python
import os  
import yaml  
  
from langchain.agents import create\_json\_agent, AgentExecutor  
from langchain.agents.agent\_toolkits import JsonToolkit  
from langchain.chains import LLMChain  
from langchain.llms.openai import OpenAI  
from langchain.requests import TextRequestsWrapper  
from langchain.tools.json.tool import JsonSpec  

```

```python
with open("openai\_openapi.yml") as f:  
 data = yaml.load(f, Loader=yaml.FullLoader)  
json\_spec = JsonSpec(dict\_=data, max\_value\_length=4000)  
json\_toolkit = JsonToolkit(spec=json\_spec)  
  
json\_agent\_executor = create\_json\_agent(  
 llm=OpenAI(temperature=0), toolkit=json\_toolkit, verbose=True  
)  

```

## Example: getting the required POST parameters for a request[​](#example-getting-the-required-post-parameters-for-a-request "Direct link to Example: getting the required POST parameters for a request")

```python
json\_agent\_executor.run(  
 "What are the required parameters in the request body to the /completions endpoint?"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Action: json\_spec\_list\_keys  
 Action Input: data  
 Observation: ['openapi', 'info', 'servers', 'tags', 'paths', 'components', 'x-oaiMeta']  
 Thought: I should look at the paths key to see what endpoints exist  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]  
 Observation: ['/engines', '/engines/{engine\_id}', '/completions', '/edits', '/images/generations', '/images/edits', '/images/variations', '/embeddings', '/engines/{engine\_id}/search', '/files', '/files/{file\_id}', '/files/{file\_id}/content', '/answers', '/classifications', '/fine-tunes', '/fine-tunes/{fine\_tune\_id}', '/fine-tunes/{fine\_tune\_id}/cancel', '/fine-tunes/{fine\_tune\_id}/events', '/models', '/models/{model}', '/moderations']  
 Thought: I should look at the /completions endpoint to see what parameters are required  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]["/completions"]  
 Observation: ['post']  
 Thought: I should look at the post key to see what parameters are required  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]["/completions"]["post"]  
 Observation: ['operationId', 'tags', 'summary', 'requestBody', 'responses', 'x-oaiMeta']  
 Thought: I should look at the requestBody key to see what parameters are required  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]["/completions"]["post"]["requestBody"]  
 Observation: ['required', 'content']  
 Thought: I should look at the required key to see what parameters are required  
 Action: json\_spec\_get\_value  
 Action Input: data["paths"]["/completions"]["post"]["requestBody"]["required"]  
 Observation: True  
 Thought: I should look at the content key to see what parameters are required  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"]  
 Observation: ['application/json']  
 Thought: I should look at the application/json key to see what parameters are required  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"]["application/json"]  
 Observation: ['schema']  
 Thought: I should look at the schema key to see what parameters are required  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"]["application/json"]["schema"]  
 Observation: ['$ref']  
 Thought: I should look at the $ref key to see what parameters are required  
 Action: json\_spec\_get\_value  
 Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"]["application/json"]["schema"]["$ref"]  
 Observation: #/components/schemas/CreateCompletionRequest  
 Thought: I should look at the CreateCompletionRequest schema to see what parameters are required  
 Action: json\_spec\_list\_keys  
 Action Input: data["components"]["schemas"]["CreateCompletionRequest"]  
 Observation: ['type', 'properties', 'required']  
 Thought: I should look at the required key to see what parameters are required  
 Action: json\_spec\_get\_value  
 Action Input: data["components"]["schemas"]["CreateCompletionRequest"]["required"]  
 Observation: ['model']  
 Thought: I now know the final answer  
 Final Answer: The required parameters in the request body to the /completions endpoint are 'model'.  
   
 > Finished chain.  
  
  
  
  
  
 "The required parameters in the request body to the /completions endpoint are 'model'."  

```

- [Initialization](#initialization)
- [Example: getting the required POST parameters for a request](#example-getting-the-required-post-parameters-for-a-request)

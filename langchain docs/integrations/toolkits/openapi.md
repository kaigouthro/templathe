# OpenAPI

We can construct agents to consume arbitrary APIs, here APIs conformant to the `OpenAPI`/`Swagger` specification.

## 1st example: hierarchical planning agent[​](#1st-example-hierarchical-planning-agent "Direct link to 1st example: hierarchical planning agent")

In this example, we'll consider an approach called hierarchical planning, common in robotics and appearing in recent works for LLMs X robotics. We'll see it's a viable approach to start working with a massive API spec AND to assist with user queries that require multiple steps against the API.

The idea is simple: to get coherent agent behavior over long sequences behavior & to save on tokens, we'll separate concerns: a "planner" will be responsible for what endpoints to call and a "controller" will be responsible for how to call them.

In the initial implementation, the planner is an LLM chain that has the name and a short description for each endpoint in context. The controller is an LLM agent that is instantiated with documentation for only the endpoints for a particular plan. There's a lot left to get this working very robustly :)

### To start, let's collect some OpenAPI specs.[​](#to-start-lets-collect-some-openapi-specs "Direct link to To start, let's collect some OpenAPI specs.")

```python
import os, yaml  

```

```bash
wget https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml  
mv openapi.yaml openai\_openapi.yaml  
wget https://www.klarna.com/us/shopping/public/openai/v0/api-docs  
mv api-docs klarna\_openapi.yaml  
wget https://raw.githubusercontent.com/APIs-guru/openapi-directory/main/APIs/spotify.com/1.0.0/openapi.yaml  
mv openapi.yaml spotify\_openapi.yaml  

```

```text
 --2023-03-31 15:45:56-- https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml  
 Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.110.133, 185.199.109.133, 185.199.111.133, ...  
 Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.110.133|:443... connected.  
 HTTP request sent, awaiting response... 200 OK  
 Length: 122995 (120K) [text/plain]  
 Saving to: ‘openapi.yaml’  
   
 openapi.yaml 100%[===================>] 120.11K --.-KB/s in 0.01s   
   
 2023-03-31 15:45:56 (10.4 MB/s) - ‘openapi.yaml’ saved [122995/122995]  
   
 --2023-03-31 15:45:57-- https://www.klarna.com/us/shopping/public/openai/v0/api-docs  
 Resolving www.klarna.com (www.klarna.com)... 52.84.150.34, 52.84.150.46, 52.84.150.61, ...  
 Connecting to www.klarna.com (www.klarna.com)|52.84.150.34|:443... connected.  
 HTTP request sent, awaiting response... 200 OK  
 Length: unspecified [application/json]  
 Saving to: ‘api-docs’  
   
 api-docs [ <=> ] 1.87K --.-KB/s in 0s   
   
 2023-03-31 15:45:57 (261 MB/s) - ‘api-docs’ saved [1916]  
   
 --2023-03-31 15:45:57-- https://raw.githubusercontent.com/APIs-guru/openapi-directory/main/APIs/spotify.com/1.0.0/openapi.yaml  
 Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.110.133, 185.199.109.133, 185.199.111.133, ...  
 Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.110.133|:443... connected.  
 HTTP request sent, awaiting response... 200 OK  
 Length: 286747 (280K) [text/plain]  
 Saving to: ‘openapi.yaml’  
   
 openapi.yaml 100%[===================>] 280.03K --.-KB/s in 0.02s   
   
 2023-03-31 15:45:58 (13.3 MB/s) - ‘openapi.yaml’ saved [286747/286747]  
   

```

```python
from langchain.agents.agent\_toolkits.openapi.spec import reduce\_openapi\_spec  

```

```python
with open("openai\_openapi.yaml") as f:  
 raw\_openai\_api\_spec = yaml.load(f, Loader=yaml.Loader)  
openai\_api\_spec = reduce\_openapi\_spec(raw\_openai\_api\_spec)  
  
with open("klarna\_openapi.yaml") as f:  
 raw\_klarna\_api\_spec = yaml.load(f, Loader=yaml.Loader)  
klarna\_api\_spec = reduce\_openapi\_spec(raw\_klarna\_api\_spec)  
  
with open("spotify\_openapi.yaml") as f:  
 raw\_spotify\_api\_spec = yaml.load(f, Loader=yaml.Loader)  
spotify\_api\_spec = reduce\_openapi\_spec(raw\_spotify\_api\_spec)  

```

We'll work with the Spotify API as one of the examples of a somewhat complex API. There's a bit of auth-related setup to do if you want to replicate this.

- You'll have to set up an application in the Spotify developer console, documented [here](https://developer.spotify.com/documentation/general/guides/authorization/), to get credentials: `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI`.
- To get an access tokens (and keep them fresh), you can implement the oauth flows, or you can use `spotipy`. If you've set your Spotify creedentials as environment variables `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI`, you can use the helper functions below:

```python
import spotipy.util as util  
from langchain.requests import RequestsWrapper  
  
  
def construct\_spotify\_auth\_headers(raw\_spec: dict):  
 scopes = list(  
 raw\_spec["components"]["securitySchemes"]["oauth\_2\_0"]["flows"][  
 "authorizationCode"  
 ]["scopes"].keys()  
 )  
 access\_token = util.prompt\_for\_user\_token(scope=",".join(scopes))  
 return {"Authorization": f"Bearer {access\_token}"}  
  
  
# Get API credentials.  
headers = construct\_spotify\_auth\_headers(raw\_spotify\_api\_spec)  
requests\_wrapper = RequestsWrapper(headers=headers)  

```

### How big is this spec?[​](#how-big-is-this-spec "Direct link to How big is this spec?")

```python
endpoints = [  
 (route, operation)  
 for route, operations in raw\_spotify\_api\_spec["paths"].items()  
 for operation in operations  
 if operation in ["get", "post"]  
]  
len(endpoints)  

```

```text
 63  

```

```python
import tiktoken  
  
enc = tiktoken.encoding\_for\_model("text-davinci-003")  
  
  
def count\_tokens(s):  
 return len(enc.encode(s))  
  
  
count\_tokens(yaml.dump(raw\_spotify\_api\_spec))  

```

```text
 80326  

```

### Let's see some examples![​](#lets-see-some-examples "Direct link to Let's see some examples!")

Starting with GPT-4. (Some robustness iterations under way for GPT-3 family.)

```python
from langchain.llms.openai import OpenAI  
from langchain.agents.agent\_toolkits.openapi import planner  
  
llm = OpenAI(model\_name="gpt-4", temperature=0.0)  

```

```text
 /Users/jeremywelborn/src/langchain/langchain/llms/openai.py:169: UserWarning: You are trying to use a chat model. This way of initializing it is no longer supported. Instead, please use: `from langchain.chat\_models import ChatOpenAI`  
 warnings.warn(  
 /Users/jeremywelborn/src/langchain/langchain/llms/openai.py:608: UserWarning: You are trying to use a chat model. This way of initializing it is no longer supported. Instead, please use: `from langchain.chat\_models import ChatOpenAI`  
 warnings.warn(  

```

```python
spotify\_agent = planner.create\_openapi\_agent(spotify\_api\_spec, requests\_wrapper, llm)  
user\_query = (  
 "make me a playlist with the first song from kind of blue. call it machine blues."  
)  
spotify\_agent.run(user\_query)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Action: api\_planner  
 Action Input: I need to find the right API calls to create a playlist with the first song from Kind of Blue and name it Machine Blues  
 Observation: 1. GET /search to search for the album "Kind of Blue"  
 2. GET /albums/{id}/tracks to get the tracks from the "Kind of Blue" album  
 3. GET /me to get the current user's information  
 4. POST /users/{user\_id}/playlists to create a new playlist named "Machine Blues" for the current user  
 5. POST /playlists/{playlist\_id}/tracks to add the first song from "Kind of Blue" to the "Machine Blues" playlist  
 Thought:I have the plan, now I need to execute the API calls.  
 Action: api\_controller  
 Action Input: 1. GET /search to search for the album "Kind of Blue"  
 2. GET /albums/{id}/tracks to get the tracks from the "Kind of Blue" album  
 3. GET /me to get the current user's information  
 4. POST /users/{user\_id}/playlists to create a new playlist named "Machine Blues" for the current user  
 5. POST /playlists/{playlist\_id}/tracks to add the first song from "Kind of Blue" to the "Machine Blues" playlist  
   
 > Entering new AgentExecutor chain...  
 Action: requests\_get  
 Action Input: {"url": "https://api.spotify.com/v1/search?q=Kind%20of%20Blue&type=album", "output\_instructions": "Extract the id of the first album in the search results"}  
 Observation: 1weenld61qoidwYuZ1GESA  
 Thought:Action: requests\_get  
 Action Input: {"url": "https://api.spotify.com/v1/albums/1weenld61qoidwYuZ1GESA/tracks", "output\_instructions": "Extract the id of the first track in the album"}  
 Observation: 7q3kkfAVpmcZ8g6JUThi3o  
 Thought:Action: requests\_get  
 Action Input: {"url": "https://api.spotify.com/v1/me", "output\_instructions": "Extract the id of the current user"}  
 Observation: 22rhrz4m4kvpxlsb5hezokzwi  
 Thought:Action: requests\_post  
 Action Input: {"url": "https://api.spotify.com/v1/users/22rhrz4m4kvpxlsb5hezokzwi/playlists", "data": {"name": "Machine Blues"}, "output\_instructions": "Extract the id of the created playlist"}  
 Observation: 7lzoEi44WOISnFYlrAIqyX  
 Thought:Action: requests\_post  
 Action Input: {"url": "https://api.spotify.com/v1/playlists/7lzoEi44WOISnFYlrAIqyX/tracks", "data": {"uris": ["spotify:track:7q3kkfAVpmcZ8g6JUThi3o"]}, "output\_instructions": "Confirm that the track was added to the playlist"}  
   
 Observation: The track was added to the playlist, confirmed by the snapshot\_id: MiwxODMxNTMxZTFlNzg3ZWFlZmMxYTlmYWQyMDFiYzUwNDEwMTAwZmE1.  
 Thought:I am finished executing the plan.  
 Final Answer: The first song from the "Kind of Blue" album has been added to the "Machine Blues" playlist.  
   
 > Finished chain.  
   
 Observation: The first song from the "Kind of Blue" album has been added to the "Machine Blues" playlist.  
 Thought:I am finished executing the plan and have created the playlist with the first song from Kind of Blue.  
 Final Answer: I have created a playlist called "Machine Blues" with the first song from the "Kind of Blue" album.  
   
 > Finished chain.  
  
  
  
  
  
 'I have created a playlist called "Machine Blues" with the first song from the "Kind of Blue" album.'  

```

```python
user\_query = "give me a song I'd like, make it blues-ey"  
spotify\_agent.run(user\_query)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Action: api\_planner  
 Action Input: I need to find the right API calls to get a blues song recommendation for the user  
 Observation: 1. GET /me to get the current user's information  
 2. GET /recommendations/available-genre-seeds to retrieve a list of available genres  
 3. GET /recommendations with the seed\_genre parameter set to "blues" to get a blues song recommendation for the user  
 Thought:I have the plan, now I need to execute the API calls.  
 Action: api\_controller  
 Action Input: 1. GET /me to get the current user's information  
 2. GET /recommendations/available-genre-seeds to retrieve a list of available genres  
 3. GET /recommendations with the seed\_genre parameter set to "blues" to get a blues song recommendation for the user  
   
 > Entering new AgentExecutor chain...  
 Action: requests\_get  
 Action Input: {"url": "https://api.spotify.com/v1/me", "output\_instructions": "Extract the user's id and username"}  
 Observation: ID: 22rhrz4m4kvpxlsb5hezokzwi, Username: Jeremy Welborn  
 Thought:Action: requests\_get  
 Action Input: {"url": "https://api.spotify.com/v1/recommendations/available-genre-seeds", "output\_instructions": "Extract the list of available genres"}  
 Observation: acoustic, afrobeat, alt-rock, alternative, ambient, anime, black-metal, bluegrass, blues, bossanova, brazil, breakbeat, british, cantopop, chicago-house, children, chill, classical, club, comedy, country, dance, dancehall, death-metal, deep-house, detroit-techno, disco, disney, drum-and-bass, dub, dubstep, edm, electro, electronic, emo, folk, forro, french, funk, garage, german, gospel, goth, grindcore, groove, grunge, guitar, happy, hard-rock, hardcore, hardstyle, heavy-metal, hip-hop, holidays, honky-tonk, house, idm, indian, indie, indie-pop, industrial, iranian, j-dance, j-idol, j-pop, j-rock, jazz, k-pop, kids, latin, latino, malay, mandopop, metal, metal-misc, metalcore, minimal-techno, movies, mpb, new-age, new-release, opera, pagode, party, philippines-  
 Thought:  
  
 Retrying langchain.llms.openai.completion\_with\_retry.<locals>.\_completion\_with\_retry in 4.0 seconds as it raised RateLimitError: That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists. (Please include the request ID 2167437a0072228238f3c0c5b3882764 in your message.).  
  
  
 Action: requests\_get  
 Action Input: {"url": "https://api.spotify.com/v1/recommendations?seed\_genres=blues", "output\_instructions": "Extract the list of recommended tracks with their ids and names"}  
 Observation: [  
 {  
 id: '03lXHmokj9qsXspNsPoirR',  
 name: 'Get Away Jordan'  
 }  
 ]  
 Thought:I am finished executing the plan.  
 Final Answer: The recommended blues song for user Jeremy Welborn (ID: 22rhrz4m4kvpxlsb5hezokzwi) is "Get Away Jordan" with the track ID: 03lXHmokj9qsXspNsPoirR.  
   
 > Finished chain.  
   
 Observation: The recommended blues song for user Jeremy Welborn (ID: 22rhrz4m4kvpxlsb5hezokzwi) is "Get Away Jordan" with the track ID: 03lXHmokj9qsXspNsPoirR.  
 Thought:I am finished executing the plan and have the information the user asked for.  
 Final Answer: The recommended blues song for you is "Get Away Jordan" with the track ID: 03lXHmokj9qsXspNsPoirR.  
   
 > Finished chain.  
  
  
  
  
  
 'The recommended blues song for you is "Get Away Jordan" with the track ID: 03lXHmokj9qsXspNsPoirR.'  

```

#### Try another API.[​](#try-another-api "Direct link to Try another API.")

```python
headers = {"Authorization": f"Bearer {os.getenv('OPENAI\_API\_KEY')}"}  
openai\_requests\_wrapper = RequestsWrapper(headers=headers)  

```

```python
# Meta!  
llm = OpenAI(model\_name="gpt-4", temperature=0.25)  
openai\_agent = planner.create\_openapi\_agent(  
 openai\_api\_spec, openai\_requests\_wrapper, llm  
)  
user\_query = "generate a short piece of advice"  
openai\_agent.run(user\_query)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Action: api\_planner  
 Action Input: I need to find the right API calls to generate a short piece of advice  
 Observation: 1. GET /engines to retrieve the list of available engines  
 2. POST /completions with the selected engine and a prompt for generating a short piece of advice  
 Thought:I have the plan, now I need to execute the API calls.  
 Action: api\_controller  
 Action Input: 1. GET /engines to retrieve the list of available engines  
 2. POST /completions with the selected engine and a prompt for generating a short piece of advice  
   
 > Entering new AgentExecutor chain...  
 Action: requests\_get  
 Action Input: {"url": "https://api.openai.com/v1/engines", "output\_instructions": "Extract the ids of the engines"}  
 Observation: babbage, davinci, text-davinci-edit-001, babbage-code-search-code, text-similarity-babbage-001, code-davinci-edit-001, text-davinci-001, ada, babbage-code-search-text, babbage-similarity, whisper-1, code-search-babbage-text-001, text-curie-001, code-search-babbage-code-001, text-ada-001, text-embedding-ada-002, text-similarity-ada-001, curie-instruct-beta, ada-code-search-code, ada-similarity, text-davinci-003, code-search-ada-text-001, text-search-ada-query-001, davinci-search-document, ada-code-search-text, text-search-ada-doc-001, davinci-instruct-beta, text-similarity-curie-001, code-search-ada-code-001  
 Thought:I will use the "davinci" engine to generate a short piece of advice.  
 Action: requests\_post  
 Action Input: {"url": "https://api.openai.com/v1/completions", "data": {"engine": "davinci", "prompt": "Give me a short piece of advice on how to be more productive."}, "output\_instructions": "Extract the text from the first choice"}  
 Observation: "you must provide a model parameter"  
 Thought:!! Could not \_extract\_tool\_and\_input from "I cannot finish executing the plan without knowing how to provide the model parameter correctly." in \_get\_next\_action  
 I cannot finish executing the plan without knowing how to provide the model parameter correctly.  
   
 > Finished chain.  
   
 Observation: I need more information on how to provide the model parameter correctly in the POST request to generate a short piece of advice.  
 Thought:I need to adjust my plan to include the model parameter in the POST request.  
 Action: api\_planner  
 Action Input: I need to find the right API calls to generate a short piece of advice, including the model parameter in the POST request  
 Observation: 1. GET /models to retrieve the list of available models  
 2. Choose a suitable model from the list  
 3. POST /completions with the chosen model as a parameter to generate a short piece of advice  
 Thought:I have an updated plan, now I need to execute the API calls.  
 Action: api\_controller  
 Action Input: 1. GET /models to retrieve the list of available models  
 2. Choose a suitable model from the list  
 3. POST /completions with the chosen model as a parameter to generate a short piece of advice  
   
 > Entering new AgentExecutor chain...  
 Action: requests\_get  
 Action Input: {"url": "https://api.openai.com/v1/models", "output\_instructions": "Extract the ids of the available models"}  
 Observation: babbage, davinci, text-davinci-edit-001, babbage-code-search-code, text-similarity-babbage-001, code-davinci-edit-001, text-davinci-edit-001, ada  
 Thought:Action: requests\_post  
 Action Input: {"url": "https://api.openai.com/v1/completions", "data": {"model": "davinci", "prompt": "Give me a short piece of advice on how to improve communication skills."}, "output\_instructions": "Extract the text from the first choice"}  
 Observation: "I'd like to broaden my horizon.\n\nI was trying to"  
 Thought:I cannot finish executing the plan without knowing some other information.  
   
 Final Answer: The generated text is not a piece of advice on improving communication skills. I would need to retry the API call with a different prompt or model to get a more relevant response.  
   
 > Finished chain.  
   
 Observation: The generated text is not a piece of advice on improving communication skills. I would need to retry the API call with a different prompt or model to get a more relevant response.  
 Thought:I need to adjust my plan to include a more specific prompt for generating a short piece of advice on improving communication skills.  
 Action: api\_planner  
 Action Input: I need to find the right API calls to generate a short piece of advice on improving communication skills, including the model parameter in the POST request  
 Observation: 1. GET /models to retrieve the list of available models  
 2. Choose a suitable model for generating text (e.g., text-davinci-002)  
 3. POST /completions with the chosen model and a prompt related to improving communication skills to generate a short piece of advice  
 Thought:I have an updated plan, now I need to execute the API calls.  
 Action: api\_controller  
 Action Input: 1. GET /models to retrieve the list of available models  
 2. Choose a suitable model for generating text (e.g., text-davinci-002)  
 3. POST /completions with the chosen model and a prompt related to improving communication skills to generate a short piece of advice  
   
 > Entering new AgentExecutor chain...  
 Action: requests\_get  
 Action Input: {"url": "https://api.openai.com/v1/models", "output\_instructions": "Extract the names of the models"}  
 Observation: babbage, davinci, text-davinci-edit-001, babbage-code-search-code, text-similarity-babbage-001, code-davinci-edit-001, text-davinci-edit-001, ada  
 Thought:Action: requests\_post  
 Action Input: {"url": "https://api.openai.com/v1/completions", "data": {"model": "text-davinci-002", "prompt": "Give a short piece of advice on how to improve communication skills"}, "output\_instructions": "Extract the text from the first choice"}  
 Observation: "Some basic advice for improving communication skills would be to make sure to listen"  
 Thought:I am finished executing the plan.  
   
 Final Answer: Some basic advice for improving communication skills would be to make sure to listen.  
   
 > Finished chain.  
   
 Observation: Some basic advice for improving communication skills would be to make sure to listen.  
 Thought:I am finished executing the plan and have the information the user asked for.  
 Final Answer: A short piece of advice for improving communication skills is to make sure to listen.  
   
 > Finished chain.  
  
  
  
  
  
 'A short piece of advice for improving communication skills is to make sure to listen.'  

```

Takes awhile to get there!

## 2nd example: "json explorer" agent[​](#2nd-example-json-explorer-agent "Direct link to 2nd example: \"json explorer\" agent")

Here's an agent that's not particularly practical, but neat! The agent has access to 2 toolkits. One comprises tools to interact with json: one tool to list the keys of a json object and another tool to get the value for a given key. The other toolkit comprises `requests` wrappers to send GET and POST requests. This agent consumes a lot calls to the language model, but does a surprisingly decent job.

```python
from langchain.agents import create\_openapi\_agent  
from langchain.agents.agent\_toolkits import OpenAPIToolkit  
from langchain.llms.openai import OpenAI  
from langchain.requests import TextRequestsWrapper  
from langchain.tools.json.tool import JsonSpec  

```

```python
with open("openai\_openapi.yaml") as f:  
 data = yaml.load(f, Loader=yaml.FullLoader)  
json\_spec = JsonSpec(dict\_=data, max\_value\_length=4000)  
  
  
openapi\_toolkit = OpenAPIToolkit.from\_llm(  
 OpenAI(temperature=0), json\_spec, openai\_requests\_wrapper, verbose=True  
)  
openapi\_agent\_executor = create\_openapi\_agent(  
 llm=OpenAI(temperature=0), toolkit=openapi\_toolkit, verbose=True  
)  

```

```python
openapi\_agent\_executor.run(  
 "Make a post request to openai /completions. The prompt should be 'tell me a joke.'"  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Action: json\_explorer  
 Action Input: What is the base url for the API?  
   
 > Entering new AgentExecutor chain...  
 Action: json\_spec\_list\_keys  
 Action Input: data  
 Observation: ['openapi', 'info', 'servers', 'tags', 'paths', 'components', 'x-oaiMeta']  
 Thought: I should look at the servers key to see what the base url is  
 Action: json\_spec\_list\_keys  
 Action Input: data["servers"][0]  
 Observation: ValueError('Value at path `data["servers"][0]` is not a dict, get the value directly.')  
 Thought: I should get the value of the servers key  
 Action: json\_spec\_get\_value  
 Action Input: data["servers"][0]  
 Observation: {'url': 'https://api.openai.com/v1'}  
 Thought: I now know the base url for the API  
 Final Answer: The base url for the API is https://api.openai.com/v1  
   
 > Finished chain.  
   
 Observation: The base url for the API is https://api.openai.com/v1  
 Thought: I should find the path for the /completions endpoint.  
 Action: json\_explorer  
 Action Input: What is the path for the /completions endpoint?  
   
 > Entering new AgentExecutor chain...  
 Action: json\_spec\_list\_keys  
 Action Input: data  
 Observation: ['openapi', 'info', 'servers', 'tags', 'paths', 'components', 'x-oaiMeta']  
 Thought: I should look at the paths key to see what endpoints exist  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]  
 Observation: ['/engines', '/engines/{engine\_id}', '/completions', '/chat/completions', '/edits', '/images/generations', '/images/edits', '/images/variations', '/embeddings', '/audio/transcriptions', '/audio/translations', '/engines/{engine\_id}/search', '/files', '/files/{file\_id}', '/files/{file\_id}/content', '/answers', '/classifications', '/fine-tunes', '/fine-tunes/{fine\_tune\_id}', '/fine-tunes/{fine\_tune\_id}/cancel', '/fine-tunes/{fine\_tune\_id}/events', '/models', '/models/{model}', '/moderations']  
 Thought: I now know the path for the /completions endpoint  
 Final Answer: The path for the /completions endpoint is data["paths"][2]  
   
 > Finished chain.  
   
 Observation: The path for the /completions endpoint is data["paths"][2]  
 Thought: I should find the required parameters for the POST request.  
 Action: json\_explorer  
 Action Input: What are the required parameters for a POST request to the /completions endpoint?  
   
 > Entering new AgentExecutor chain...  
 Action: json\_spec\_list\_keys  
 Action Input: data  
 Observation: ['openapi', 'info', 'servers', 'tags', 'paths', 'components', 'x-oaiMeta']  
 Thought: I should look at the paths key to see what endpoints exist  
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]  
 Observation: ['/engines', '/engines/{engine\_id}', '/completions', '/chat/completions', '/edits', '/images/generations', '/images/edits', '/images/variations', '/embeddings', '/audio/transcriptions', '/audio/translations', '/engines/{engine\_id}/search', '/files', '/files/{file\_id}', '/files/{file\_id}/content', '/answers', '/classifications', '/fine-tunes', '/fine-tunes/{fine\_tune\_id}', '/fine-tunes/{fine\_tune\_id}/cancel', '/fine-tunes/{fine\_tune\_id}/events', '/models', '/models/{model}', '/moderations']  
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
 Action: json\_spec\_list\_keys  
 Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"]["application/json"]["schema"]["$ref"]  
 Observation: ValueError('Value at path `data["paths"]["/completions"]["post"]["requestBody"]["content"]["application/json"]["schema"]["$ref"]` is not a dict, get the value directly.')  
 Thought: I should look at the $ref key to get the value directly  
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
 Final Answer: The required parameters for a POST request to the /completions endpoint are 'model'.  
   
 > Finished chain.  
   
 Observation: The required parameters for a POST request to the /completions endpoint are 'model'.  
 Thought: I now know the parameters needed to make the request.  
 Action: requests\_post  
 Action Input: { "url": "https://api.openai.com/v1/completions", "data": { "model": "davinci", "prompt": "tell me a joke" } }  
 Observation: {"id":"cmpl-70Ivzip3dazrIXU8DSVJGzFJj2rdv","object":"text\_completion","created":1680307139,"model":"davinci","choices":[{"text":" with mummy not there”\n\nYou dig deep and come up with,","index":0,"logprobs":null,"finish\_reason":"length"}],"usage":{"prompt\_tokens":4,"completion\_tokens":16,"total\_tokens":20}}  
   
 Thought: I now know the final answer.  
 Final Answer: The response of the POST request is {"id":"cmpl-70Ivzip3dazrIXU8DSVJGzFJj2rdv","object":"text\_completion","created":1680307139,"model":"davinci","choices":[{"text":" with mummy not there”\n\nYou dig deep and come up with,","index":0,"logprobs":null,"finish\_reason":"length"}],"usage":{"prompt\_tokens":4,"completion\_tokens":16,"total\_tokens":20}}  
   
 > Finished chain.  
  
  
  
  
  
 'The response of the POST request is {"id":"cmpl-70Ivzip3dazrIXU8DSVJGzFJj2rdv","object":"text\_completion","created":1680307139,"model":"davinci","choices":[{"text":" with mummy not there”\\n\\nYou dig deep and come up with,","index":0,"logprobs":null,"finish\_reason":"length"}],"usage":{"prompt\_tokens":4,"completion\_tokens":16,"total\_tokens":20}}'  

```

- [1st example: hierarchical planning agent](#1st-example-hierarchical-planning-agent)

  - [To start, let's collect some OpenAPI specs.](#to-start-lets-collect-some-openapi-specs)
  - [How big is this spec?](#how-big-is-this-spec)
  - [Let's see some examples!](#lets-see-some-examples)

- [2nd example: "json explorer" agent](#2nd-example-json-explorer-agent)

- [To start, let's collect some OpenAPI specs.](#to-start-lets-collect-some-openapi-specs)

- [How big is this spec?](#how-big-is-this-spec)

- [Let's see some examples!](#lets-see-some-examples)

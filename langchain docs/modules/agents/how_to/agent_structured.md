# Returning Structured Output

This notebook covers how to have an agent return a structured output.
By default, most of the agents return a single string.
It can often be useful to have an agent return something with more structure.

A good example of this is an agent tasked with doing question-answering over some sources.
Let's say we want the agent to respond not only with the answer, but also a list of the sources used.
We then want our output to roughly follow the schema below:

```python
class Response(BaseModel):  
 """Final response to the question being asked"""  
 answer: str = Field(description = "The final answer to respond to the user")  
 sources: List[int] = Field(description="List of page chunks that contain answer to the question. Only include a page chunk if it contains relevant information")  

```

In this notebook we will go over an agent that has a retriever tool and responds in the correct format.

## Create the Retriever[​](#create-the-retriever "Direct link to Create the Retriever")

In this section we will do some setup work to create our retriever over some mock data containing the "State of the Union" address. Importantly, we will add a "page_chunk" tag to the metadata of each document. This is just some fake data intended to simulate a source field. In practice, this would more likely be the URL or path of a document.

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import Chroma  
from langchain.text\_splitter import RecursiveCharacterTextSplitter  
from langchain.document\_loaders import TextLoader  

```

```python
# Load in document to retrieve over  
loader = TextLoader('../../state\_of\_the\_union.txt')  
documents = loader.load()  
  
# Split document into chunks  
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_documents(documents)  
  
# Here is where we add in the fake source information  
for i, doc in enumerate(texts):  
 doc.metadata['page\_chunk'] = i  
  
# Create our retriever  
embeddings = OpenAIEmbeddings()  
vectorstore = Chroma.from\_documents(texts, embeddings, collection\_name="state-of-union")  
retriever = vectorstore.as\_retriever()  

```

## Create the tools[​](#create-the-tools "Direct link to Create the tools")

We will now create the tools we want to give to the agent. In this case, it is just one - a tool that wraps our retriever.

```python
from langchain.agents.agent\_toolkits.conversational\_retrieval.tool import create\_retriever\_tool  
  
retriever\_tool = create\_retriever\_tool(  
 retriever,  
 "state-of-union-retriever",  
 "Query a retriever to get information about state of the union address"  
)  

```

## Create response schema[​](#create-response-schema "Direct link to Create response schema")

Here is where we will define the response schema. In this case, we want the final answer to have two fields: one for the `answer`, and then another that is a list of `sources`

```python
from pydantic import BaseModel, Field  
from typing import List  
from langchain.utils.openai\_functions import convert\_pydantic\_to\_openai\_function  
  
class Response(BaseModel):  
 """Final response to the question being asked"""  
 answer: str = Field(description = "The final answer to respond to the user")  
 sources: List[int] = Field(description="List of page chunks that contain answer to the question. Only include a page chunk if it contains relevant information")  

```

## Create the custom parsing logic[​](#create-the-custom-parsing-logic "Direct link to Create the custom parsing logic")

We now create some custom parsing logic.
How this works is that we will pass the `Response` schema to the OpenAI LLM via their `functions` parameter.
This is similar to how we pass tools for the agent to use.

When the `Response` function is called by OpenAI, we want to use that as a signal to return to the user.
When any other function is called by OpenAI, we treat that as a tool invocation.

Therefore, our parsing logic has the following blocks:

- If no function is called, assume that we should use the response to respond to the user, and therefore return `AgentFinish`
- If the `Response` function is called, respond to the user with the inputs to that function (our structured output), and therefore return `AgentFinish`
- If any other function is called, treat that as a tool invocation, and therefore return `AgentActionMessageLog`

Note that we are using `AgentActionMessageLog` rather than `AgentAction` because it lets us attach a log of messages that we can use in the future to pass back into the agent prompt.

```python
from langchain.schema.agent import AgentActionMessageLog, AgentFinish  
import json  

```

```python
def parse(output):  
 # If no function was invoked, return to user  
 if "function\_call" not in output.additional\_kwargs:  
 return AgentFinish(return\_values={"output": output.content}, log=output.content)  
   
 # Parse out the function call  
 function\_call = output.additional\_kwargs["function\_call"]  
 name = function\_call['name']  
 inputs = json.loads(function\_call['arguments'])  
   
 # If the Response function was invoked, return to the user with the function inputs  
 if name == "Response":  
 return AgentFinish(return\_values=inputs, log=str(function\_call))  
 # Otherwise, return an agent action  
 else:  
 return AgentActionMessageLog(tool=name, tool\_input=inputs, log="", message\_log=[output])  

```

## Create the Agent[​](#create-the-agent "Direct link to Create the Agent")

We can now put this all together! The components of this agent are:

- prompt: a simple prompt with placeholders for the user's question and then the `agent_scratchpad` (any intermediate steps)
- tools: we can attach the tools and `Response` format to the LLM as functions
- format scratchpad: in order to format the `agent_scratchpad` from intermediate steps, we will use the standard `format_to_openai_functions`. This takes intermediate steps and formats them as AIMessages and FunctionMessages.
- output parser: we will use our custom parser above to parse the response of the LLM
- AgentExecutor: we will use the standard AgentExecutor to run the loop of agent-tool-agent-tool...

```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder  
from langchain.chat\_models import ChatOpenAI  
from langchain.tools.render import format\_tool\_to\_openai\_function  
from langchain.agents.format\_scratchpad import format\_to\_openai\_functions  
from langchain.agents import AgentExecutor  

```

```python
prompt = ChatPromptTemplate.from\_messages([  
 ("system", "You are a helpful assistant"),  
 ("user", "{input}"),  
 MessagesPlaceholder(variable\_name="agent\_scratchpad"),  
])  

```

```python
llm = ChatOpenAI(temperature=0)  

```

```python
llm\_with\_tools = llm.bind(  
 functions=[  
 # The retriever tool  
 format\_tool\_to\_openai\_function(retriever\_tool),   
 # Response schema  
 convert\_pydantic\_to\_openai\_function(Response)  
 ]  
)  

```

```python
agent = {  
 "input": lambda x: x["input"],  
 # Format agent scratchpad from intermediate steps  
 "agent\_scratchpad": lambda x: format\_to\_openai\_functions(x['intermediate\_steps'])  
} | prompt | llm\_with\_tools | parse  

```

```python
agent\_executor = AgentExecutor(tools=[retriever\_tool], agent=agent, verbose=True)  

```

## Run the agent[​](#run-the-agent "Direct link to Run the agent")

We can now run the agent! Notice how it responds with a dictionary with two keys: `answer` and `sources`

```python
agent\_executor.invoke({"input": "what did the president say about kentaji brown jackson"}, return\_only\_outputs=True)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 [Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'page\_chunk': 31, 'source': '../../state\_of\_the\_union.txt'}), Document(page\_content='One was stationed at bases and breathing in toxic smoke from “burn pits” that incinerated wastes of war—medical and hazard material, jet fuel, and more. \n\nWhen they came home, many of the world’s fittest and best trained warriors were never the same. \n\nHeadaches. Numbness. Dizziness. \n\nA cancer that would put them in a flag-draped coffin. \n\nI know. \n\nOne of those soldiers was my son Major Beau Biden. \n\nWe don’t know for sure if a burn pit was the cause of his brain cancer, or the diseases of so many of our troops. \n\nBut I’m committed to finding out everything we can. \n\nCommitted to military families like Danielle Robinson from Ohio. \n\nThe widow of Sergeant First Class Heath Robinson. \n\nHe was born a soldier. Army National Guard. Combat medic in Kosovo and Iraq. \n\nStationed near Baghdad, just yards from burn pits the size of football fields. \n\nHeath’s widow Danielle is here with us tonight. They loved going to Ohio State football games. He loved building Legos with their daughter.', metadata={'page\_chunk': 37, 'source': '../../state\_of\_the\_union.txt'}), Document(page\_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling. \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers. \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'page\_chunk': 32, 'source': '../../state\_of\_the\_union.txt'}), Document(page\_content='But cancer from prolonged exposure to burn pits ravaged Heath’s lungs and body. \n\nDanielle says Heath was a fighter to the very end. \n\nHe didn’t know how to stop fighting, and neither did she. \n\nThrough her pain she found purpose to demand we do better. \n\nTonight, Danielle—we are. \n\nThe VA is pioneering new ways of linking toxic exposures to diseases, already helping more veterans get benefits. \n\nAnd tonight, I’m announcing we’re expanding eligibility to veterans suffering from nine respiratory cancers. \n\nI’m also calling on Congress: pass a law to make sure veterans devastated by toxic exposures in Iraq and Afghanistan finally get the benefits and comprehensive health care they deserve. \n\nAnd fourth, let’s end cancer as we know it. \n\nThis is personal to me and Jill, to Kamala, and to so many of you. \n\nCancer is the #2 cause of death in America–second only to heart disease.', metadata={'page\_chunk': 38, 'source': '../../state\_of\_the\_union.txt'})]{'name': 'Response', 'arguments': '{\n "answer": "President mentioned Ketanji Brown Jackson as a nominee for the United States Supreme Court and praised her as one of the nation\'s top legal minds.",\n "sources": [31]\n}'}  
   
 > Finished chain.  
  
  
  
  
  
 {'answer': "President mentioned Ketanji Brown Jackson as a nominee for the United States Supreme Court and praised her as one of the nation's top legal minds.",  
 'sources': [31]}  

```

- [Create the Retriever](#create-the-retriever)
- [Create the tools](#create-the-tools)
- [Create response schema](#create-response-schema)
- [Create the custom parsing logic](#create-the-custom-parsing-logic)
- [Create the Agent](#create-the-agent)
- [Run the agent](#run-the-agent)

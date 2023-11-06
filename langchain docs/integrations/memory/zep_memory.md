# Zep

[Zep](https://docs.getzep.com/) is a long-term memory store for LLM applications.

`Zep` stores, summarizes, embeds, indexes, and enriches conversational AI chat histories, and exposes them via simple, low-latency APIs.

Key Features:

- **Fast!** Zep’s async extractors operate independently of your chat loop, ensuring a snappy user experience.
- **Long-term memory persistence**, with access to historical messages irrespective of your summarization strategy.
- **Auto-summarization** of memory messages based on a configurable message window. A series of summaries are stored, providing flexibility for future summarization strategies.
- **Hybrid search** over memories and metadata, with messages automatically embedded upon creation.
- **Entity Extractor** that automatically extracts named entities from messages and stores them in the message metadata.
- **Auto-token counting** of memories and summaries, allowing finer-grained control over prompt assembly.
- Python and JavaScript SDKs.

`Zep` project: <https://github.com/getzep/zep>
Docs: <https://docs.getzep.com/>

## Example[​](#example "Direct link to Example")

This notebook demonstrates how to use the [Zep Long-term Memory Store](https://docs.getzep.com/) as memory for your chatbot.
REACT Agent Chat Message History with Zep - A long-term memory store for LLM applications.

We'll demonstrate:

1. Adding conversation history to the Zep memory store.
1. Running an agent and having message automatically added to the store.
1. Viewing the enriched messages.
1. Vector search over the conversation history.

```python
from langchain.memory import ZepMemory  
from langchain.retrievers import ZepRetriever  
from langchain.llms import OpenAI  
from langchain.schema import HumanMessage, AIMessage  
from langchain.utilities import WikipediaAPIWrapper  
from langchain.agents import initialize\_agent, AgentType, Tool  
from uuid import uuid4  
  
  
# Set this to your Zep server URL  
ZEP\_API\_URL = "http://localhost:8000"  
  
session\_id = str(uuid4()) # This is a unique identifier for the user  

```

```python
# Provide your OpenAI key  
import getpass  
  
openai\_key = getpass.getpass()  

```

```python
# Provide your Zep API key. Note that this is optional. See https://docs.getzep.com/deployment/auth  
  
zep\_api\_key = getpass.getpass()  

```

### Initialize the Zep Chat Message History Class and initialize the Agent[​](#initialize-the-zep-chat-message-history-class-and-initialize-the-agent "Direct link to Initialize the Zep Chat Message History Class and initialize the Agent")

```python
search = WikipediaAPIWrapper()  
tools = [  
 Tool(  
 name="Search",  
 func=search.run,  
 description="useful for when you need to search online for answers. You should ask targeted questions",  
 ),  
]  
  
# Set up Zep Chat History  
memory = ZepMemory(  
 session\_id=session\_id,  
 url=ZEP\_API\_URL,  
 api\_key=zep\_api\_key,  
 memory\_key="chat\_history",  
)  
  
# Initialize the agent  
llm = OpenAI(temperature=0, openai\_api\_key=openai\_key)  
agent\_chain = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.CONVERSATIONAL\_REACT\_DESCRIPTION,  
 verbose=True,  
 memory=memory,  
)  

```

### Add some history data[​](#add-some-history-data "Direct link to Add some history data")

```python
# Preload some messages into the memory. The default message window is 12 messages. We want to push beyond this to demonstrate auto-summarization.  
test\_history = [  
 {"role": "human", "content": "Who was Octavia Butler?"},  
 {  
 "role": "ai",  
 "content": (  
 "Octavia Estelle Butler (June 22, 1947 – February 24, 2006) was an American"  
 " science fiction author."  
 ),  
 },  
 {"role": "human", "content": "Which books of hers were made into movies?"},  
 {  
 "role": "ai",  
 "content": (  
 "The most well-known adaptation of Octavia Butler's work is the FX series"  
 " Kindred, based on her novel of the same name."  
 ),  
 },  
 {"role": "human", "content": "Who were her contemporaries?"},  
 {  
 "role": "ai",  
 "content": (  
 "Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R."  
 " Delany, and Joanna Russ."  
 ),  
 },  
 {"role": "human", "content": "What awards did she win?"},  
 {  
 "role": "ai",  
 "content": (  
 "Octavia Butler won the Hugo Award, the Nebula Award, and the MacArthur"  
 " Fellowship."  
 ),  
 },  
 {  
 "role": "human",  
 "content": "Which other women sci-fi writers might I want to read?",  
 },  
 {  
 "role": "ai",  
 "content": "You might want to read Ursula K. Le Guin or Joanna Russ.",  
 },  
 {  
 "role": "human",  
 "content": (  
 "Write a short synopsis of Butler's book, Parable of the Sower. What is it"  
 " about?"  
 ),  
 },  
 {  
 "role": "ai",  
 "content": (  
 "Parable of the Sower is a science fiction novel by Octavia Butler,"  
 " published in 1993. It follows the story of Lauren Olamina, a young woman"  
 " living in a dystopian future where society has collapsed due to"  
 " environmental disasters, poverty, and violence."  
 ),  
 "metadata": {"foo": "bar"},  
 },  
]  
  
for msg in test\_history:  
 memory.chat\_memory.add\_message(  
 HumanMessage(content=msg["content"])  
 if msg["role"] == "human"  
 else AIMessage(content=msg["content"]),  
 metadata=msg.get("metadata", {}),  
 )  

```

### Run the agent[​](#run-the-agent "Direct link to Run the agent")

Doing so will automatically add the input and response to the Zep memory.

```python
agent\_chain.run(  
 input="What is the book's relevance to the challenges facing contemporary society?",  
)  

```

```text
   
   
 > Entering new chain...  
 Thought: Do I need to use a tool? No  
 AI: Parable of the Sower is a prescient novel that speaks to the challenges facing contemporary society, such as climate change, inequality, and violence. It is a cautionary tale that warns of the dangers of unchecked greed and the need for individuals to take responsibility for their own lives and the lives of those around them.  
   
 > Finished chain.  
  
  
  
  
  
 'Parable of the Sower is a prescient novel that speaks to the challenges facing contemporary society, such as climate change, inequality, and violence. It is a cautionary tale that warns of the dangers of unchecked greed and the need for individuals to take responsibility for their own lives and the lives of those around them.'  

```

### Inspect the Zep memory[​](#inspect-the-zep-memory "Direct link to Inspect the Zep memory")

Note the summary, and that the history has been enriched with token counts, UUIDs, and timestamps.

Summaries are biased towards the most recent messages.

```python
def print\_messages(messages):  
 for m in messages:  
 print(m.type, ":\n", m.dict())  
  
  
print(memory.chat\_memory.zep\_summary)  
print("\n")  
print\_messages(memory.chat\_memory.messages)  

```

```text
 The human inquires about Octavia Butler. The AI identifies her as an American science fiction author. The human then asks which books of hers were made into movies. The AI responds by mentioning the FX series Kindred, based on her novel of the same name. The human then asks about her contemporaries, and the AI lists Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.  
   
   
 system :  
 {'content': 'The human inquires about Octavia Butler. The AI identifies her as an American science fiction author. The human then asks which books of hers were made into movies. The AI responds by mentioning the FX series Kindred, based on her novel of the same name. The human then asks about her contemporaries, and the AI lists Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.', 'additional\_kwargs': {}}  
 human :  
 {'content': 'What awards did she win?', 'additional\_kwargs': {'uuid': '6b733f0b-6778-49ae-b3ec-4e077c039f31', 'created\_at': '2023-07-09T19:23:16.611232Z', 'token\_count': 8, 'metadata': {'system': {'entities': [], 'intent': 'The subject is inquiring about the awards that someone, whose identity is not specified, has won.'}}}, 'example': False}  
 ai :  
 {'content': 'Octavia Butler won the Hugo Award, the Nebula Award, and the MacArthur Fellowship.', 'additional\_kwargs': {'uuid': '2f6d80c6-3c08-4fd4-8d4e-7bbee341ac90', 'created\_at': '2023-07-09T19:23:16.618947Z', 'token\_count': 21, 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 14, 'Start': 0, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}, {'Label': 'WORK\_OF\_ART', 'Matches': [{'End': 33, 'Start': 19, 'Text': 'the Hugo Award'}], 'Name': 'the Hugo Award'}, {'Label': 'EVENT', 'Matches': [{'End': 81, 'Start': 57, 'Text': 'the MacArthur Fellowship'}], 'Name': 'the MacArthur Fellowship'}], 'intent': 'The subject is stating that Octavia Butler received the Hugo Award, the Nebula Award, and the MacArthur Fellowship.'}}}, 'example': False}  
 human :  
 {'content': 'Which other women sci-fi writers might I want to read?', 'additional\_kwargs': {'uuid': 'ccdcc901-ea39-4981-862f-6fe22ab9289b', 'created\_at': '2023-07-09T19:23:16.62678Z', 'token\_count': 14, 'metadata': {'system': {'entities': [], 'intent': 'The subject is seeking recommendations for additional women science fiction writers to explore.'}}}, 'example': False}  
 ai :  
 {'content': 'You might want to read Ursula K. Le Guin or Joanna Russ.', 'additional\_kwargs': {'uuid': '7977099a-0c62-4c98-bfff-465bbab6c9c3', 'created\_at': '2023-07-09T19:23:16.631721Z', 'token\_count': 18, 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 40, 'Start': 23, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 55, 'Start': 44, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}], 'intent': 'The subject is suggesting that the person should consider reading the works of Ursula K. Le Guin or Joanna Russ.'}}}, 'example': False}  
 human :  
 {'content': "Write a short synopsis of Butler's book, Parable of the Sower. What is it about?", 'additional\_kwargs': {'uuid': 'e439b7e6-286a-4278-a8cb-dc260fa2e089', 'created\_at': '2023-07-09T19:23:16.63623Z', 'token\_count': 23, 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 32, 'Start': 26, 'Text': 'Butler'}], 'Name': 'Butler'}, {'Label': 'WORK\_OF\_ART', 'Matches': [{'End': 61, 'Start': 41, 'Text': 'Parable of the Sower'}], 'Name': 'Parable of the Sower'}], 'intent': 'The subject is requesting a brief summary or explanation of the book "Parable of the Sower" by Butler.'}}}, 'example': False}  
 ai :  
 {'content': 'Parable of the Sower is a science fiction novel by Octavia Butler, published in 1993. It follows the story of Lauren Olamina, a young woman living in a dystopian future where society has collapsed due to environmental disasters, poverty, and violence.', 'additional\_kwargs': {'uuid': '6760489b-19c9-41aa-8b45-fae6cb1d7ee6', 'created\_at': '2023-07-09T19:23:16.647524Z', 'token\_count': 56, 'metadata': {'foo': 'bar', 'system': {'entities': [{'Label': 'GPE', 'Matches': [{'End': 20, 'Start': 15, 'Text': 'Sower'}], 'Name': 'Sower'}, {'Label': 'PERSON', 'Matches': [{'End': 65, 'Start': 51, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}, {'Label': 'DATE', 'Matches': [{'End': 84, 'Start': 80, 'Text': '1993'}], 'Name': '1993'}, {'Label': 'PERSON', 'Matches': [{'End': 124, 'Start': 110, 'Text': 'Lauren Olamina'}], 'Name': 'Lauren Olamina'}], 'intent': 'The subject is providing information about the novel "Parable of the Sower" by Octavia Butler, including its genre, publication date, and a brief summary of the plot.'}}}, 'example': False}  
 human :  
 {'content': "What is the book's relevance to the challenges facing contemporary society?", 'additional\_kwargs': {'uuid': '7dbbbb93-492b-4739-800f-cad2b6e0e764', 'created\_at': '2023-07-09T19:23:19.315182Z', 'token\_count': 15, 'metadata': {'system': {'entities': [], 'intent': 'The subject is asking about the relevance of a book to the challenges currently faced by society.'}}}, 'example': False}  
 ai :  
 {'content': 'Parable of the Sower is a prescient novel that speaks to the challenges facing contemporary society, such as climate change, inequality, and violence. It is a cautionary tale that warns of the dangers of unchecked greed and the need for individuals to take responsibility for their own lives and the lives of those around them.', 'additional\_kwargs': {'uuid': '3e14ac8f-b7c1-4360-958b-9f3eae1f784f', 'created\_at': '2023-07-09T19:23:19.332517Z', 'token\_count': 66, 'metadata': {'system': {'entities': [{'Label': 'GPE', 'Matches': [{'End': 20, 'Start': 15, 'Text': 'Sower'}], 'Name': 'Sower'}], 'intent': 'The subject is providing an analysis and evaluation of the novel "Parable of the Sower" and highlighting its relevance to contemporary societal challenges.'}}}, 'example': False}  

```

### Vector search over the Zep memory[​](#vector-search-over-the-zep-memory "Direct link to Vector search over the Zep memory")

Zep provides native vector search over historical conversation memory via the `ZepRetriever`.

You can use the `ZepRetriever` with chains that support passing in a Langchain `Retriever` object.

```python
retriever = ZepRetriever(  
 session\_id=session\_id,  
 url=ZEP\_API\_URL,  
 api\_key=zep\_api\_key,  
)  
  
search\_results = memory.chat\_memory.search("who are some famous women sci-fi authors?")  
for r in search\_results:  
 if r.dist > 0.8: # Only print results with similarity of 0.8 or higher  
 print(r.message, r.dist)  

```

```text
 {'uuid': 'ccdcc901-ea39-4981-862f-6fe22ab9289b', 'created\_at': '2023-07-09T19:23:16.62678Z', 'role': 'human', 'content': 'Which other women sci-fi writers might I want to read?', 'metadata': {'system': {'entities': [], 'intent': 'The subject is seeking recommendations for additional women science fiction writers to explore.'}}, 'token\_count': 14} 0.9119619869747062  
 {'uuid': '7977099a-0c62-4c98-bfff-465bbab6c9c3', 'created\_at': '2023-07-09T19:23:16.631721Z', 'role': 'ai', 'content': 'You might want to read Ursula K. Le Guin or Joanna Russ.', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 40, 'Start': 23, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 55, 'Start': 44, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}], 'intent': 'The subject is suggesting that the person should consider reading the works of Ursula K. Le Guin or Joanna Russ.'}}, 'token\_count': 18} 0.8534346954749745  
 {'uuid': 'b05e2eb5-c103-4973-9458-928726f08655', 'created\_at': '2023-07-09T19:23:16.603098Z', 'role': 'ai', 'content': "Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.", 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 16, 'Start': 0, 'Text': "Octavia Butler's"}], 'Name': "Octavia Butler's"}, {'Label': 'ORG', 'Matches': [{'End': 58, 'Start': 41, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 76, 'Start': 60, 'Text': 'Samuel R. Delany'}], 'Name': 'Samuel R. Delany'}, {'Label': 'PERSON', 'Matches': [{'End': 93, 'Start': 82, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}], 'intent': "The subject is stating that Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ."}}, 'token\_count': 27} 0.8523831524040919  
 {'uuid': 'e346f02b-f854-435d-b6ba-fb394a416b9b', 'created\_at': '2023-07-09T19:23:16.556587Z', 'role': 'human', 'content': 'Who was Octavia Butler?', 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 22, 'Start': 8, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}], 'intent': 'The subject is asking for information about the identity or background of Octavia Butler.'}}, 'token\_count': 8} 0.8236355436055457  
 {'uuid': '42ff41d2-c63a-4d5b-b19b-d9a87105cfc3', 'created\_at': '2023-07-09T19:23:16.578022Z', 'role': 'ai', 'content': 'Octavia Estelle Butler (June 22, 1947 – February 24, 2006) was an American science fiction author.', 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 22, 'Start': 0, 'Text': 'Octavia Estelle Butler'}], 'Name': 'Octavia Estelle Butler'}, {'Label': 'DATE', 'Matches': [{'End': 37, 'Start': 24, 'Text': 'June 22, 1947'}], 'Name': 'June 22, 1947'}, {'Label': 'DATE', 'Matches': [{'End': 57, 'Start': 40, 'Text': 'February 24, 2006'}], 'Name': 'February 24, 2006'}, {'Label': 'NORP', 'Matches': [{'End': 74, 'Start': 66, 'Text': 'American'}], 'Name': 'American'}], 'intent': 'The subject is providing information about Octavia Estelle Butler, who was an American science fiction author.'}}, 'token\_count': 31} 0.8206687242257686  
 {'uuid': '2f6d80c6-3c08-4fd4-8d4e-7bbee341ac90', 'created\_at': '2023-07-09T19:23:16.618947Z', 'role': 'ai', 'content': 'Octavia Butler won the Hugo Award, the Nebula Award, and the MacArthur Fellowship.', 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 14, 'Start': 0, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}, {'Label': 'WORK\_OF\_ART', 'Matches': [{'End': 33, 'Start': 19, 'Text': 'the Hugo Award'}], 'Name': 'the Hugo Award'}, {'Label': 'EVENT', 'Matches': [{'End': 81, 'Start': 57, 'Text': 'the MacArthur Fellowship'}], 'Name': 'the MacArthur Fellowship'}], 'intent': 'The subject is stating that Octavia Butler received the Hugo Award, the Nebula Award, and the MacArthur Fellowship.'}}, 'token\_count': 21} 0.8199012397683285  

```

- [Example](#example)

  - [Initialize the Zep Chat Message History Class and initialize the Agent](#initialize-the-zep-chat-message-history-class-and-initialize-the-agent)
  - [Add some history data](#add-some-history-data)
  - [Run the agent](#run-the-agent)
  - [Inspect the Zep memory](#inspect-the-zep-memory)
  - [Vector search over the Zep memory](#vector-search-over-the-zep-memory)

- [Initialize the Zep Chat Message History Class and initialize the Agent](#initialize-the-zep-chat-message-history-class-and-initialize-the-agent)

- [Add some history data](#add-some-history-data)

- [Run the agent](#run-the-agent)

- [Inspect the Zep memory](#inspect-the-zep-memory)

- [Vector search over the Zep memory](#vector-search-over-the-zep-memory)

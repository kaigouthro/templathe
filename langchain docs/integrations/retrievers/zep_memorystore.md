# Zep

## Retriever Example for [Zep](https://docs.getzep.com/) - Fast, scalable building blocks for LLM Apps[​](#retriever-example-for-zep---fast-scalable-building-blocks-for-llm-apps "Direct link to retriever-example-for-zep---fast-scalable-building-blocks-for-llm-apps")

### More on Zep:[​](#more-on-zep "Direct link to More on Zep:")

Zep is an open source platform for productionizing LLM apps. Go from a prototype
built in LangChain or LlamaIndex, or a custom app, to production in minutes without
rewriting code.

Key Features:

- **Fast!** Zep’s async extractors operate independently of the your chat loop, ensuring a snappy user experience.
- **Long-term memory persistence**, with access to historical messages irrespective of your summarization strategy.
- **Auto-summarization** of memory messages based on a configurable message window. A series of summaries are stored, providing flexibility for future summarization strategies.
- **Hybrid search** over memories and metadata, with messages automatically embedded on creation.
- **Entity Extractor** that automatically extracts named entities from messages and stores them in the message metadata.
- **Auto-token counting** of memories and summaries, allowing finer-grained control over prompt assembly.
- Python and JavaScript SDKs.

Zep project: <https://github.com/getzep/zep>
Docs: <https://docs.getzep.com/>

## Retriever Example[​](#retriever-example "Direct link to Retriever Example")

This notebook demonstrates how to search historical chat message histories using the [Zep Long-term Memory Store](https://getzep.github.io/).

We'll demonstrate:

1. Adding conversation history to the Zep memory store.
1. Vector search over the conversation history.

```python
import getpass  
import time  
from uuid import uuid4  
  
from langchain.memory import ZepMemory  
from langchain.schema import HumanMessage, AIMessage  
  
# Set this to your Zep server URL  
ZEP\_API\_URL = "http://localhost:8000"  

```

### Initialize the Zep Chat Message History Class and add a chat message history to the memory store[​](#initialize-the-zep-chat-message-history-class-and-add-a-chat-message-history-to-the-memory-store "Direct link to Initialize the Zep Chat Message History Class and add a chat message history to the memory store")

**NOTE:** Unlike other Retrievers, the content returned by the Zep Retriever is session/user specific. A `session_id` is required when instantiating the Retriever.

```python
# Provide your Zep API key. Note that this is optional. See https://docs.getzep.com/deployment/auth  
AUTHENTICATE = False  
  
zep\_api\_key = None  
if AUTHENTICATE:  
 zep\_api\_key = getpass.getpass()  

```

```python
session\_id = str(uuid4()) # This is a unique identifier for the user/session  
  
# Initialize the Zep Memory Class  
zep\_memory = ZepMemory(session\_id=session\_id, url=ZEP\_API\_URL, api\_key=zep\_api\_key)  

```

```text
 /Users/danielchalef/dev/langchain/.venv/lib/python3.11/site-packages/zep\_python/zep\_client.py:86: Warning: You are using an incompatible Zep server version. Please upgrade to {MINIMUM\_SERVER\_VERSION} or later.  
 self.\_healthcheck(base\_url)  

```

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
 },  
]  
  
for msg in test\_history:  
 zep\_memory.chat\_memory.add\_message(  
 HumanMessage(content=msg["content"])  
 if msg["role"] == "human"  
 else AIMessage(content=msg["content"])  
 )  
  
time.sleep(2) # Wait for the messages to be embedded  

```

### Use the Zep Retriever to vector search over the Zep memory[​](#use-the-zep-retriever-to-vector-search-over-the-zep-memory "Direct link to Use the Zep Retriever to vector search over the Zep memory")

Zep provides native vector search over historical conversation memory. Embedding happens automatically.

NOTE: Embedding of messages occurs asynchronously, so the first query may not return results. Subsequent queries will return results as the embeddings are generated.

```python
from langchain.retrievers import ZepRetriever  
from langchain.retrievers.zep import SearchType  
  
zep\_retriever = ZepRetriever(  
 session\_id=session\_id, # Ensure that you provide the session\_id when instantiating the Retriever  
 url=ZEP\_API\_URL,  
 top\_k=5,  
 api\_key=zep\_api\_key,  
)  
  
await zep\_retriever.aget\_relevant\_documents("Who wrote Parable of the Sower?")  

```

```text
 [Document(page\_content='Parable of the Sower is a science fiction novel by Octavia Butler, published in 1993. It follows the story of Lauren Olamina, a young woman living in a dystopian future where society has collapsed due to environmental disasters, poverty, and violence.', metadata={'score': 0.8897589445114136, 'uuid': 'f99ecec3-f778-4bfd-8bb7-c3c00ae919c0', 'created\_at': '2023-10-17T22:53:08.664849Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'GPE', 'Matches': [{'End': 20, 'Start': 15, 'Text': 'Sower'}], 'Name': 'Sower'}, {'Label': 'PERSON', 'Matches': [{'End': 65, 'Start': 51, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}, {'Label': 'DATE', 'Matches': [{'End': 84, 'Start': 80, 'Text': '1993'}], 'Name': '1993'}, {'Label': 'PERSON', 'Matches': [{'End': 124, 'Start': 110, 'Text': 'Lauren Olamina'}], 'Name': 'Lauren Olamina'}]}}, 'token\_count': 56}),  
 Document(page\_content="Write a short synopsis of Butler's book, Parable of the Sower. What is it about?", metadata={'score': 0.8856973648071289, 'uuid': 'f6aba470-f15f-4b22-84ef-1c0d315a31de', 'created\_at': '2023-10-17T22:53:08.642659Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 32, 'Start': 26, 'Text': 'Butler'}], 'Name': 'Butler'}, {'Label': 'WORK\_OF\_ART', 'Matches': [{'End': 61, 'Start': 41, 'Text': 'Parable of the Sower'}], 'Name': 'Parable of the Sower'}]}}, 'token\_count': 23}),  
 Document(page\_content='Who was Octavia Butler?', metadata={'score': 0.7759557962417603, 'uuid': '26aab7b5-34b1-4aff-9be0-7834a7702be4', 'created\_at': '2023-10-17T22:53:08.585297Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 22, 'Start': 8, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}], 'intent': 'The subject is asking for information about Octavia Butler, a specific person.'}}, 'token\_count': 8}),  
 Document(page\_content="Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.", metadata={'score': 0.760245680809021, 'uuid': 'ee4aa8e9-9913-4e69-a2a5-77a85294d24e', 'created\_at': '2023-10-17T22:53:08.611466Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 16, 'Start': 0, 'Text': "Octavia Butler's"}], 'Name': "Octavia Butler's"}, {'Label': 'ORG', 'Matches': [{'End': 58, 'Start': 41, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 76, 'Start': 60, 'Text': 'Samuel R. Delany'}], 'Name': 'Samuel R. Delany'}, {'Label': 'PERSON', 'Matches': [{'End': 93, 'Start': 82, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}]}}, 'token\_count': 27}),  
 Document(page\_content='You might want to read Ursula K. Le Guin or Joanna Russ.', metadata={'score': 0.7596070170402527, 'uuid': '9fa630e6-0b17-4d77-80b0-ba99249850c0', 'created\_at': '2023-10-17T22:53:08.630731Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 40, 'Start': 23, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 55, 'Start': 44, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}]}}, 'token\_count': 18})]  

```

We can also use the Zep sync API to retrieve results:

```python
zep\_retriever.get\_relevant\_documents("Who wrote Parable of the Sower?")  

```

```text
 [Document(page\_content='Parable of the Sower is a science fiction novel by Octavia Butler, published in 1993. It follows the story of Lauren Olamina, a young woman living in a dystopian future where society has collapsed due to environmental disasters, poverty, and violence.', metadata={'score': 0.8897120952606201, 'uuid': 'f99ecec3-f778-4bfd-8bb7-c3c00ae919c0', 'created\_at': '2023-10-17T22:53:08.664849Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'GPE', 'Matches': [{'End': 20, 'Start': 15, 'Text': 'Sower'}], 'Name': 'Sower'}, {'Label': 'PERSON', 'Matches': [{'End': 65, 'Start': 51, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}, {'Label': 'DATE', 'Matches': [{'End': 84, 'Start': 80, 'Text': '1993'}], 'Name': '1993'}, {'Label': 'PERSON', 'Matches': [{'End': 124, 'Start': 110, 'Text': 'Lauren Olamina'}], 'Name': 'Lauren Olamina'}]}}, 'token\_count': 56}),  
 Document(page\_content="Write a short synopsis of Butler's book, Parable of the Sower. What is it about?", metadata={'score': 0.8857351541519165, 'uuid': 'f6aba470-f15f-4b22-84ef-1c0d315a31de', 'created\_at': '2023-10-17T22:53:08.642659Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 32, 'Start': 26, 'Text': 'Butler'}], 'Name': 'Butler'}, {'Label': 'WORK\_OF\_ART', 'Matches': [{'End': 61, 'Start': 41, 'Text': 'Parable of the Sower'}], 'Name': 'Parable of the Sower'}]}}, 'token\_count': 23}),  
 Document(page\_content='Who was Octavia Butler?', metadata={'score': 0.7759560942649841, 'uuid': '26aab7b5-34b1-4aff-9be0-7834a7702be4', 'created\_at': '2023-10-17T22:53:08.585297Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 22, 'Start': 8, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}], 'intent': 'The subject is asking for information about Octavia Butler, a specific person.'}}, 'token\_count': 8}),  
 Document(page\_content="Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.", metadata={'score': 0.7602507472038269, 'uuid': 'ee4aa8e9-9913-4e69-a2a5-77a85294d24e', 'created\_at': '2023-10-17T22:53:08.611466Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'PERSON', 'Matches': [{'End': 16, 'Start': 0, 'Text': "Octavia Butler's"}], 'Name': "Octavia Butler's"}, {'Label': 'ORG', 'Matches': [{'End': 58, 'Start': 41, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 76, 'Start': 60, 'Text': 'Samuel R. Delany'}], 'Name': 'Samuel R. Delany'}, {'Label': 'PERSON', 'Matches': [{'End': 93, 'Start': 82, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}], 'intent': "The subject is stating a fact about Octavia Butler's contemporaries, including Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ."}}, 'token\_count': 27}),  
 Document(page\_content='You might want to read Ursula K. Le Guin or Joanna Russ.', metadata={'score': 0.7595934867858887, 'uuid': '9fa630e6-0b17-4d77-80b0-ba99249850c0', 'created\_at': '2023-10-17T22:53:08.630731Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 40, 'Start': 23, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 55, 'Start': 44, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}]}}, 'token\_count': 18})]  

```

### Reranking using MMR (Maximal Marginal Relevance)[​](#reranking-using-mmr-maximal-marginal-relevance "Direct link to Reranking using MMR (Maximal Marginal Relevance)")

Zep has native, SIMD-accelerated support for reranking results using MMR. This is useful for removing redundancy in results.

```python
zep\_retriever = ZepRetriever(  
 session\_id=session\_id, # Ensure that you provide the session\_id when instantiating the Retriever  
 url=ZEP\_API\_URL,  
 top\_k=5,  
 api\_key=zep\_api\_key,  
 search\_type=SearchType.mmr,  
 mmr\_lambda=0.5,  
)  
  
await zep\_retriever.aget\_relevant\_documents("Who wrote Parable of the Sower?")  

```

```text
 /Users/danielchalef/dev/langchain/.venv/lib/python3.11/site-packages/zep\_python/zep\_client.py:86: Warning: You are using an incompatible Zep server version. Please upgrade to {MINIMUM\_SERVER\_VERSION} or later.  
 self.\_healthcheck(base\_url)  
  
  
  
  
  
 [Document(page\_content='Parable of the Sower is a science fiction novel by Octavia Butler, published in 1993. It follows the story of Lauren Olamina, a young woman living in a dystopian future where society has collapsed due to environmental disasters, poverty, and violence.', metadata={'score': 0.8897120952606201, 'uuid': 'f99ecec3-f778-4bfd-8bb7-c3c00ae919c0', 'created\_at': '2023-10-17T22:53:08.664849Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'GPE', 'Matches': [{'End': 20, 'Start': 15, 'Text': 'Sower'}], 'Name': 'Sower'}, {'Label': 'PERSON', 'Matches': [{'End': 65, 'Start': 51, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}, {'Label': 'DATE', 'Matches': [{'End': 84, 'Start': 80, 'Text': '1993'}], 'Name': '1993'}, {'Label': 'PERSON', 'Matches': [{'End': 124, 'Start': 110, 'Text': 'Lauren Olamina'}], 'Name': 'Lauren Olamina'}]}}, 'token\_count': 56}),  
 Document(page\_content='Which books of hers were made into movies?', metadata={'score': 0.7496200799942017, 'uuid': '1047ff15-96f1-4101-bb0f-9ed073b8081d', 'created\_at': '2023-10-17T22:53:08.596614Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'intent': 'The subject is inquiring about the books of the person referred to as "hers" that have been made into movies.'}}, 'token\_count': 11}),  
 Document(page\_content="Write a short synopsis of Butler's book, Parable of the Sower. What is it about?", metadata={'score': 0.8857351541519165, 'uuid': 'f6aba470-f15f-4b22-84ef-1c0d315a31de', 'created\_at': '2023-10-17T22:53:08.642659Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 32, 'Start': 26, 'Text': 'Butler'}], 'Name': 'Butler'}, {'Label': 'WORK\_OF\_ART', 'Matches': [{'End': 61, 'Start': 41, 'Text': 'Parable of the Sower'}], 'Name': 'Parable of the Sower'}]}}, 'token\_count': 23}),  
 Document(page\_content='You might want to read Ursula K. Le Guin or Joanna Russ.', metadata={'score': 0.7595934867858887, 'uuid': '9fa630e6-0b17-4d77-80b0-ba99249850c0', 'created\_at': '2023-10-17T22:53:08.630731Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 40, 'Start': 23, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 55, 'Start': 44, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}]}}, 'token\_count': 18}),  
 Document(page\_content='Who were her contemporaries?', metadata={'score': 0.7575579881668091, 'uuid': 'b2dfd1f7-cac6-4e37-94ea-7c15b0a5af2c', 'created\_at': '2023-10-17T22:53:08.606283Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'intent': 'The subject is asking about the people who were contemporaries of someone else.'}}, 'token\_count': 8})]  

```

### Using metadata filters to refine search results[​](#using-metadata-filters-to-refine-search-results "Direct link to Using metadata filters to refine search results")

Zep supports filtering results by metadata. This is useful for filtering results by entity type, or other metadata.

More information here: <https://docs.getzep.com/sdk/search_query/>

```python
filter = {"where": {"jsonpath": '$[\*] ? (@.Label == "WORK\_OF\_ART")'}}  
  
await zep\_retriever.aget\_relevant\_documents(  
 "Who wrote Parable of the Sower?", metadata=filter  
)  

```

```text
 [Document(page\_content='Parable of the Sower is a science fiction novel by Octavia Butler, published in 1993. It follows the story of Lauren Olamina, a young woman living in a dystopian future where society has collapsed due to environmental disasters, poverty, and violence.', metadata={'score': 0.8897120952606201, 'uuid': 'f99ecec3-f778-4bfd-8bb7-c3c00ae919c0', 'created\_at': '2023-10-17T22:53:08.664849Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'GPE', 'Matches': [{'End': 20, 'Start': 15, 'Text': 'Sower'}], 'Name': 'Sower'}, {'Label': 'PERSON', 'Matches': [{'End': 65, 'Start': 51, 'Text': 'Octavia Butler'}], 'Name': 'Octavia Butler'}, {'Label': 'DATE', 'Matches': [{'End': 84, 'Start': 80, 'Text': '1993'}], 'Name': '1993'}, {'Label': 'PERSON', 'Matches': [{'End': 124, 'Start': 110, 'Text': 'Lauren Olamina'}], 'Name': 'Lauren Olamina'}], 'intent': 'None'}}, 'token\_count': 56}),  
 Document(page\_content='Which books of hers were made into movies?', metadata={'score': 0.7496200799942017, 'uuid': '1047ff15-96f1-4101-bb0f-9ed073b8081d', 'created\_at': '2023-10-17T22:53:08.596614Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'intent': 'The subject is inquiring about the books of the person referred to as "hers" that have been made into movies.'}}, 'token\_count': 11}),  
 Document(page\_content="Write a short synopsis of Butler's book, Parable of the Sower. What is it about?", metadata={'score': 0.8857351541519165, 'uuid': 'f6aba470-f15f-4b22-84ef-1c0d315a31de', 'created\_at': '2023-10-17T22:53:08.642659Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 32, 'Start': 26, 'Text': 'Butler'}], 'Name': 'Butler'}, {'Label': 'WORK\_OF\_ART', 'Matches': [{'End': 61, 'Start': 41, 'Text': 'Parable of the Sower'}], 'Name': 'Parable of the Sower'}], 'intent': 'The subject is requesting a brief summary or description of Butler\'s book, "Parable of the Sower."'}}, 'token\_count': 23}),  
 Document(page\_content='You might want to read Ursula K. Le Guin or Joanna Russ.', metadata={'score': 0.7595934867858887, 'uuid': '9fa630e6-0b17-4d77-80b0-ba99249850c0', 'created\_at': '2023-10-17T22:53:08.630731Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'ai', 'metadata': {'system': {'entities': [{'Label': 'ORG', 'Matches': [{'End': 40, 'Start': 23, 'Text': 'Ursula K. Le Guin'}], 'Name': 'Ursula K. Le Guin'}, {'Label': 'PERSON', 'Matches': [{'End': 55, 'Start': 44, 'Text': 'Joanna Russ'}], 'Name': 'Joanna Russ'}], 'intent': 'The subject is providing a suggestion or recommendation for the person to read Ursula K. Le Guin or Joanna Russ.'}}, 'token\_count': 18}),  
 Document(page\_content='Who were her contemporaries?', metadata={'score': 0.7575579881668091, 'uuid': 'b2dfd1f7-cac6-4e37-94ea-7c15b0a5af2c', 'created\_at': '2023-10-17T22:53:08.606283Z', 'updated\_at': '0001-01-01T00:00:00Z', 'role': 'human', 'metadata': {'system': {'intent': 'The subject is asking about the people who were contemporaries of someone else.'}}, 'token\_count': 8})]  

```

- [Retriever Example for Zep - Fast, scalable building blocks for LLM Apps](#retriever-example-for-zep---fast-scalable-building-blocks-for-llm-apps)

  - [More on Zep:](#more-on-zep)

- [Retriever Example](#retriever-example)

  - [Initialize the Zep Chat Message History Class and add a chat message history to the memory store](#initialize-the-zep-chat-message-history-class-and-add-a-chat-message-history-to-the-memory-store)
  - [Use the Zep Retriever to vector search over the Zep memory](#use-the-zep-retriever-to-vector-search-over-the-zep-memory)
  - [Reranking using MMR (Maximal Marginal Relevance)](#reranking-using-mmr-maximal-marginal-relevance)
  - [Using metadata filters to refine search results](#using-metadata-filters-to-refine-search-results)

- [More on Zep:](#more-on-zep)

- [Initialize the Zep Chat Message History Class and add a chat message history to the memory store](#initialize-the-zep-chat-message-history-class-and-add-a-chat-message-history-to-the-memory-store)

- [Use the Zep Retriever to vector search over the Zep memory](#use-the-zep-retriever-to-vector-search-over-the-zep-memory)

- [Reranking using MMR (Maximal Marginal Relevance)](#reranking-using-mmr-maximal-marginal-relevance)

- [Using metadata filters to refine search results](#using-metadata-filters-to-refine-search-results)

# Chat Over Documents with Vectara

This notebook is based on the [chat_vector_db](https://github.com/langchain-ai/langchain/blob/master/docs/modules/chains/index_examples/chat_vector_db.html) notebook, but using Vectara as the vector database.

```python
import os  
from langchain.vectorstores import Vectara  
from langchain.vectorstores.vectara import VectaraRetriever  
from langchain.llms import OpenAI  
from langchain.chains import ConversationalRetrievalChain  

```

Load in documents. You can replace this with a loader for whatever type of data you want

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  

```

We now split the documents, create embeddings for them, and put them in a vectorstore. This allows us to do semantic search over them.

```python
vectorstore = Vectara.from\_documents(documents, embedding=None)  

```

We can now create a memory object, which is neccessary to track the inputs/outputs and hold a conversation.

```python
from langchain.memory import ConversationBufferMemory  
  
memory = ConversationBufferMemory(memory\_key="chat\_history", return\_messages=True)  

```

We now initialize the `ConversationalRetrievalChain`

```python
openai\_api\_key = os.environ["OPENAI\_API\_KEY"]  
llm = OpenAI(openai\_api\_key=openai\_api\_key, temperature=0)  
retriever = vectorstore.as\_retriever(lambda\_val=0.025, k=5, filter=None)  
d = retriever.get\_relevant\_documents(  
 "What did the president say about Ketanji Brown Jackson"  
)  
  
qa = ConversationalRetrievalChain.from\_llm(llm, retriever, memory=memory)  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
result = qa({"question": query})  

```

```python
result["answer"]  

```

```text
 " The president said that Ketanji Brown Jackson is one of the nation's top legal minds and a former top litigator in private practice, and that she will continue Justice Breyer's legacy of excellence."  

```

```python
query = "Did he mention who she succeeded"  
result = qa({"question": query})  

```

```python
result["answer"]  

```

```text
 ' Ketanji Brown Jackson succeeded Justice Breyer.'  

```

## Pass in chat history[​](#pass-in-chat-history "Direct link to Pass in chat history")

In the above example, we used a Memory object to track chat history. We can also just pass it in explicitly. In order to do this, we need to initialize a chain without any memory object.

```python
qa = ConversationalRetrievalChain.from\_llm(  
 OpenAI(temperature=0), vectorstore.as\_retriever()  
)  

```

Here's an example of asking a question with no chat history

```python
chat\_history = []  
query = "What did the president say about Ketanji Brown Jackson"  
result = qa({"question": query, "chat\_history": chat\_history})  

```

```python
result["answer"]  

```

```text
 " The president said that Ketanji Brown Jackson is one of the nation's top legal minds and a former top litigator in private practice, and that she will continue Justice Breyer's legacy of excellence."  

```

Here's an example of asking a question with some chat history

```python
chat\_history = [(query, result["answer"])]  
query = "Did he mention who she succeeded"  
result = qa({"question": query, "chat\_history": chat\_history})  

```

```python
result["answer"]  

```

```text
 ' Ketanji Brown Jackson succeeded Justice Breyer.'  

```

## Return Source Documents[​](#return-source-documents "Direct link to Return Source Documents")

You can also easily return source documents from the ConversationalRetrievalChain. This is useful for when you want to inspect what documents were returned.

```python
qa = ConversationalRetrievalChain.from\_llm(  
 llm, vectorstore.as\_retriever(), return\_source\_documents=True  
)  

```

```python
chat\_history = []  
query = "What did the president say about Ketanji Brown Jackson"  
result = qa({"question": query, "chat\_history": chat\_history})  

```

```python
result["source\_documents"][0]  

```

```text
 Document(page\_content='Justice Breyer, thank you for your service. One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence. A former top litigator in private practice.', metadata={'source': '../../../modules/state\_of\_the\_union.txt'})  

```

## ConversationalRetrievalChain with `search_distance`[​](#conversationalretrievalchain-with-search_distance "Direct link to conversationalretrievalchain-with-search_distance")

If you are using a vector store that supports filtering by search distance, you can add a threshold value parameter.

```python
vectordbkwargs = {"search\_distance": 0.9}  

```

```python
qa = ConversationalRetrievalChain.from\_llm(  
 OpenAI(temperature=0), vectorstore.as\_retriever(), return\_source\_documents=True  
)  
chat\_history = []  
query = "What did the president say about Ketanji Brown Jackson"  
result = qa(  
 {"question": query, "chat\_history": chat\_history, "vectordbkwargs": vectordbkwargs}  
)  

```

```python
print(result["answer"])  

```

```text
 The president said that Ketanji Brown Jackson is one of the nation's top legal minds and a former top litigator in private practice, and that she will continue Justice Breyer's legacy of excellence.  

```

## ConversationalRetrievalChain with `map_reduce`[​](#conversationalretrievalchain-with-map_reduce "Direct link to conversationalretrievalchain-with-map_reduce")

We can also use different types of combine document chains with the ConversationalRetrievalChain chain.

```python
from langchain.chains import LLMChain  
from langchain.chains.question\_answering import load\_qa\_chain  
from langchain.chains.conversational\_retrieval.prompts import CONDENSE\_QUESTION\_PROMPT  

```

```python
question\_generator = LLMChain(llm=llm, prompt=CONDENSE\_QUESTION\_PROMPT)  
doc\_chain = load\_qa\_chain(llm, chain\_type="map\_reduce")  
  
chain = ConversationalRetrievalChain(  
 retriever=vectorstore.as\_retriever(),  
 question\_generator=question\_generator,  
 combine\_docs\_chain=doc\_chain,  
)  

```

```python
chat\_history = []  
query = "What did the president say about Ketanji Brown Jackson"  
result = chain({"question": query, "chat\_history": chat\_history})  

```

```python
result["answer"]  

```

```text
 " The president said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson, who is one of the nation's top legal minds and a former top litigator in private practice."  

```

## ConversationalRetrievalChain with Question Answering with sources[​](#conversationalretrievalchain-with-question-answering-with-sources "Direct link to ConversationalRetrievalChain with Question Answering with sources")

You can also use this chain with the question answering with sources chain.

```python
from langchain.chains.qa\_with\_sources import load\_qa\_with\_sources\_chain  

```

```python
question\_generator = LLMChain(llm=llm, prompt=CONDENSE\_QUESTION\_PROMPT)  
doc\_chain = load\_qa\_with\_sources\_chain(llm, chain\_type="map\_reduce")  
  
chain = ConversationalRetrievalChain(  
 retriever=vectorstore.as\_retriever(),  
 question\_generator=question\_generator,  
 combine\_docs\_chain=doc\_chain,  
)  

```

```python
chat\_history = []  
query = "What did the president say about Ketanji Brown Jackson"  
result = chain({"question": query, "chat\_history": chat\_history})  

```

```python
result["answer"]  

```

```text
 " The president said that Ketanji Brown Jackson is one of the nation's top legal minds and a former top litigator in private practice.\nSOURCES: ../../../modules/state\_of\_the\_union.txt"  

```

## ConversationalRetrievalChain with streaming to `stdout`[​](#conversationalretrievalchain-with-streaming-to-stdout "Direct link to conversationalretrievalchain-with-streaming-to-stdout")

Output from the chain will be streamed to `stdout` token by token in this example.

```python
from langchain.chains.llm import LLMChain  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
from langchain.chains.conversational\_retrieval.prompts import (  
 CONDENSE\_QUESTION\_PROMPT,  
 QA\_PROMPT,  
)  
from langchain.chains.question\_answering import load\_qa\_chain  
  
# Construct a ConversationalRetrievalChain with a streaming llm for combine docs  
# and a separate, non-streaming llm for question generation  
llm = OpenAI(temperature=0, openai\_api\_key=openai\_api\_key)  
streaming\_llm = OpenAI(  
 streaming=True,  
 callbacks=[StreamingStdOutCallbackHandler()],  
 temperature=0,  
 openai\_api\_key=openai\_api\_key,  
)  
  
question\_generator = LLMChain(llm=llm, prompt=CONDENSE\_QUESTION\_PROMPT)  
doc\_chain = load\_qa\_chain(streaming\_llm, chain\_type="stuff", prompt=QA\_PROMPT)  
  
qa = ConversationalRetrievalChain(  
 retriever=vectorstore.as\_retriever(),  
 combine\_docs\_chain=doc\_chain,  
 question\_generator=question\_generator,  
)  

```

```python
chat\_history = []  
query = "What did the president say about Ketanji Brown Jackson"  
result = qa({"question": query, "chat\_history": chat\_history})  

```

```text
 The president said that Ketanji Brown Jackson is one of the nation's top legal minds and a former top litigator in private practice, and that she will continue Justice Breyer's legacy of excellence.  

```

```python
chat\_history = [(query, result["answer"])]  
query = "Did he mention who she succeeded"  
result = qa({"question": query, "chat\_history": chat\_history})  

```

```text
 Justice Breyer  

```

## get_chat_history Function[​](#get_chat_history-function "Direct link to get_chat_history Function")

You can also specify a `get_chat_history` function, which can be used to format the chat_history string.

```python
def get\_chat\_history(inputs) -> str:  
 res = []  
 for human, ai in inputs:  
 res.append(f"Human:{human}\nAI:{ai}")  
 return "\n".join(res)  
  
  
qa = ConversationalRetrievalChain.from\_llm(  
 llm, vectorstore.as\_retriever(), get\_chat\_history=get\_chat\_history  
)  

```

```python
chat\_history = []  
query = "What did the president say about Ketanji Brown Jackson"  
result = qa({"question": query, "chat\_history": chat\_history})  

```

```python
result["answer"]  

```

```text
 " The president said that Ketanji Brown Jackson is one of the nation's top legal minds and a former top litigator in private practice, and that she will continue Justice Breyer's legacy of excellence."  

```

- [Pass in chat history](#pass-in-chat-history)
- [Return Source Documents](#return-source-documents)
- [ConversationalRetrievalChain with `search_distance`](#conversationalretrievalchain-with-search_distance)
- [ConversationalRetrievalChain with `map_reduce`](#conversationalretrievalchain-with-map_reduce)
- [ConversationalRetrievalChain with Question Answering with sources](#conversationalretrievalchain-with-question-answering-with-sources)
- [ConversationalRetrievalChain with streaming to `stdout`](#conversationalretrievalchain-with-streaming-to-stdout)
- [get_chat_history Function](#get_chat_history-function)

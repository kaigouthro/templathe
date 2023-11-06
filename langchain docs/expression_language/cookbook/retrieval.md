# RAG

Let's look at adding in a retrieval step to a prompt and LLM, which adds up to a "retrieval-augmented generation" chain

```bash
pip install langchain openai faiss-cpu tiktoken  

```

```python
from operator import itemgetter  
  
from langchain.prompts import ChatPromptTemplate  
from langchain.chat\_models import ChatOpenAI  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.schema.output\_parser import StrOutputParser  
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda  
from langchain.vectorstores import FAISS  

```

```python
vectorstore = FAISS.from\_texts(["harrison worked at kensho"], embedding=OpenAIEmbeddings())  
retriever = vectorstore.as\_retriever()  
  
template = """Answer the question based only on the following context:  
{context}  
  
Question: {question}  
"""  
prompt = ChatPromptTemplate.from\_template(template)  
  
model = ChatOpenAI()  

```

```python
chain = (  
 {"context": retriever, "question": RunnablePassthrough()}   
 | prompt   
 | model   
 | StrOutputParser()  
)  

```

```python
chain.invoke("where did harrison work?")  

```

```text
 'Harrison worked at Kensho.'  

```

```python
template = """Answer the question based only on the following context:  
{context}  
  
Question: {question}  
  
Answer in the following language: {language}  
"""  
prompt = ChatPromptTemplate.from\_template(template)  
  
chain = {  
 "context": itemgetter("question") | retriever,   
 "question": itemgetter("question"),   
 "language": itemgetter("language")  
} | prompt | model | StrOutputParser()  

```

```python
chain.invoke({"question": "where did harrison work", "language": "italian"})  

```

```text
 'Harrison ha lavorato a Kensho.'  

```

## Conversational Retrieval Chain[​](#conversational-retrieval-chain "Direct link to Conversational Retrieval Chain")

We can easily add in conversation history. This primarily means adding in chat_message_history

```python
from langchain.schema.runnable import RunnableMap  
from langchain.schema import format\_document  

```

```python
from langchain.prompts.prompt import PromptTemplate  
  
\_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.  
  
Chat History:  
{chat\_history}  
Follow Up Input: {question}  
Standalone question:"""  
CONDENSE\_QUESTION\_PROMPT = PromptTemplate.from\_template(\_template)  

```

```python
template = """Answer the question based only on the following context:  
{context}  
  
Question: {question}  
"""  
ANSWER\_PROMPT = ChatPromptTemplate.from\_template(template)  

```

```python
DEFAULT\_DOCUMENT\_PROMPT = PromptTemplate.from\_template(template="{page\_content}")  
def \_combine\_documents(docs, document\_prompt = DEFAULT\_DOCUMENT\_PROMPT, document\_separator="\n\n"):  
 doc\_strings = [format\_document(doc, document\_prompt) for doc in docs]  
 return document\_separator.join(doc\_strings)  

```

```python
from typing import Tuple, List  
def \_format\_chat\_history(chat\_history: List[Tuple]) -> str:  
 buffer = ""  
 for dialogue\_turn in chat\_history:  
 human = "Human: " + dialogue\_turn[0]  
 ai = "Assistant: " + dialogue\_turn[1]  
 buffer += "\n" + "\n".join([human, ai])  
 return buffer  

```

```python
\_inputs = RunnableMap(  
 standalone\_question=RunnablePassthrough.assign(  
 chat\_history=lambda x: \_format\_chat\_history(x['chat\_history'])  
 ) | CONDENSE\_QUESTION\_PROMPT | ChatOpenAI(temperature=0) | StrOutputParser(),  
)  
\_context = {  
 "context": itemgetter("standalone\_question") | retriever | \_combine\_documents,  
 "question": lambda x: x["standalone\_question"]  
}  
conversational\_qa\_chain = \_inputs | \_context | ANSWER\_PROMPT | ChatOpenAI()  

```

```python
conversational\_qa\_chain.invoke({  
 "question": "where did harrison work?",  
 "chat\_history": [],  
})  

```

```text
 AIMessage(content='Harrison was employed at Kensho.', additional\_kwargs={}, example=False)  

```

```python
conversational\_qa\_chain.invoke({  
 "question": "where did he work?",  
 "chat\_history": [("Who wrote this notebook?", "Harrison")],  
})  

```

```text
 AIMessage(content='Harrison worked at Kensho.', additional\_kwargs={}, example=False)  

```

### With Memory and returning source documents[​](#with-memory-and-returning-source-documents "Direct link to With Memory and returning source documents")

This shows how to use memory with the above. For memory, we need to manage that outside at the memory. For returning the retrieved documents, we just need to pass them through all the way.

```python
from operator import itemgetter  
from langchain.memory import ConversationBufferMemory  

```

```python
memory = ConversationBufferMemory(return\_messages=True, output\_key="answer", input\_key="question")  

```

```python
# First we add a step to load memory  
# This adds a "memory" key to the input object  
loaded\_memory = RunnablePassthrough.assign(  
 chat\_history=RunnableLambda(memory.load\_memory\_variables) | itemgetter("history"),  
)  
# Now we calculate the standalone question  
standalone\_question = {  
 "standalone\_question": {  
 "question": lambda x: x["question"],  
 "chat\_history": lambda x: \_format\_chat\_history(x['chat\_history'])  
 } | CONDENSE\_QUESTION\_PROMPT | ChatOpenAI(temperature=0) | StrOutputParser(),  
}  
# Now we retrieve the documents  
retrieved\_documents = {  
 "docs": itemgetter("standalone\_question") | retriever,  
 "question": lambda x: x["standalone\_question"]  
}  
# Now we construct the inputs for the final prompt  
final\_inputs = {  
 "context": lambda x: \_combine\_documents(x["docs"]),  
 "question": itemgetter("question")  
}  
# And finally, we do the part that returns the answers  
answer = {  
 "answer": final\_inputs | ANSWER\_PROMPT | ChatOpenAI(),  
 "docs": itemgetter("docs"),  
}  
# And now we put it all together!  
final\_chain = loaded\_memory | standalone\_question | retrieved\_documents | answer  

```

```python
inputs = {"question": "where did harrison work?"}  
result = final\_chain.invoke(inputs)  
result  

```

```text
 {'answer': AIMessage(content='Harrison was employed at Kensho.', additional\_kwargs={}, example=False),  
 'docs': [Document(page\_content='harrison worked at kensho', metadata={})]}  

```

```python
# Note that the memory does not save automatically  
# This will be improved in the future  
# For now you need to save it yourself  
memory.save\_context(inputs, {"answer": result["answer"].content})  

```

```python
memory.load\_memory\_variables({})  

```

```text
 {'history': [HumanMessage(content='where did harrison work?', additional\_kwargs={}, example=False),  
 AIMessage(content='Harrison was employed at Kensho.', additional\_kwargs={}, example=False)]}  

```

- [Conversational Retrieval Chain](#conversational-retrieval-chain)

  - [With Memory and returning source documents](#with-memory-and-returning-source-documents)

- [With Memory and returning source documents](#with-memory-and-returning-source-documents)

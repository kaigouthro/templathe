# Memory in the Multi-Input Chain

Most memory objects assume a single input. In this notebook, we go over how to add memory to a chain that has multiple inputs. We will add memory to a question/answering chain. This chain takes as inputs both related documents and a user question.

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.embeddings.cohere import CohereEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores.elastic\_vector\_search import ElasticVectorSearch  
from langchain.vectorstores import Chroma  
from langchain.docstore.document import Document  

```

```python
with open("../../state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_text(state\_of\_the\_union)  
  
embeddings = OpenAIEmbeddings()  

```

```python
docsearch = Chroma.from\_texts(  
 texts, embeddings, metadatas=[{"source": i} for i in range(len(texts))]  
)  

```

```text
 Running Chroma using direct local API.  
 Using DuckDB in-memory for database. Data will be transient.  

```

```python
query = "What did the president say about Justice Breyer"  
docs = docsearch.similarity\_search(query)  

```

```python
from langchain.chains.question\_answering import load\_qa\_chain  
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
from langchain.memory import ConversationBufferMemory  

```

```python
template = """You are a chatbot having a conversation with a human.  
  
Given the following extracted parts of a long document and a question, create a final answer.  
  
{context}  
  
{chat\_history}  
Human: {human\_input}  
Chatbot:"""  
  
prompt = PromptTemplate(  
 input\_variables=["chat\_history", "human\_input", "context"], template=template  
)  
memory = ConversationBufferMemory(memory\_key="chat\_history", input\_key="human\_input")  
chain = load\_qa\_chain(  
 OpenAI(temperature=0), chain\_type="stuff", memory=memory, prompt=prompt  
)  

```

```python
query = "What did the president say about Justice Breyer"  
chain({"input\_documents": docs, "human\_input": query}, return\_only\_outputs=True)  

```

```text
 {'output\_text': ' Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.'}  

```

```python
print(chain.memory.buffer)  

```

```text
   
 Human: What did the president say about Justice Breyer  
 AI: Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.  

```

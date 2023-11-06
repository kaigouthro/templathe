# RePhraseQuery

`RePhraseQuery` is a simple retriever that applies an LLM between the user input and the query passed by the retriever.

It can be used to pre-process the user input in any way.

## Example[​](#example "Direct link to Example")

### Setting up[​](#setting-up "Direct link to Setting up")

Create a vector store.

```python
import logging  
from langchain.document\_loaders import WebBaseLoader  
from langchain.text\_splitter import RecursiveCharacterTextSplitter  
from langchain.vectorstores import Chroma  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.chat\_models import ChatOpenAI  
  
from langchain.retrievers import RePhraseQueryRetriever  

```

```python
logging.basicConfig()  
logging.getLogger("langchain.retrievers.re\_phraser").setLevel(logging.INFO)  
  
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")  
data = loader.load()  
  
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=500, chunk\_overlap=0)  
all\_splits = text\_splitter.split\_documents(data)  
  
vectorstore = Chroma.from\_documents(documents=all\_splits, embedding=OpenAIEmbeddings())  

```

### Using the default prompt[​](#using-the-default-prompt "Direct link to Using the default prompt")

The default prompt used in the `from_llm` classmethod:

```text
DEFAULT\_TEMPLATE = """You are an assistant tasked with taking a natural language \  
query from a user and converting it into a query for a vectorstore. \  
In this process, you strip out information that is not relevant for \  
the retrieval task. Here is the user query: {question}"""  

```

```python
llm = ChatOpenAI(temperature=0)  
retriever\_from\_llm = RePhraseQueryRetriever.from\_llm(  
 retriever=vectorstore.as\_retriever(), llm=llm  
)  

```

```python
docs = retriever\_from\_llm.get\_relevant\_documents(  
 "Hi I'm Lance. What are the approaches to Task Decomposition?"  
)  

```

```text
 INFO:langchain.retrievers.re\_phraser:Re-phrased question: The user query can be converted into a query for a vectorstore as follows:  
   
 "approaches to Task Decomposition"  

```

```python
docs = retriever\_from\_llm.get\_relevant\_documents(  
 "I live in San Francisco. What are the Types of Memory?"  
)  

```

```text
 INFO:langchain.retrievers.re\_phraser:Re-phrased question: Query for vectorstore: "Types of Memory"  

```

### Custom prompt[​](#custom-prompt "Direct link to Custom prompt")

```python
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  
  
QUERY\_PROMPT = PromptTemplate(  
 input\_variables=["question"],  
 template="""You are an assistant tasked with taking a natural languge query from a user  
 and converting it into a query for a vectorstore. In the process, strip out all   
 information that is not relevant for the retrieval task and return a new, simplified  
 question for vectorstore retrieval. The new user query should be in pirate speech.  
 Here is the user query: {question} """,  
)  
llm = ChatOpenAI(temperature=0)  
llm\_chain = LLMChain(llm=llm, prompt=QUERY\_PROMPT)  

```

```python
retriever\_from\_llm\_chain = RePhraseQueryRetriever(  
 retriever=vectorstore.as\_retriever(), llm\_chain=llm\_chain  
)  

```

```python
docs = retriever\_from\_llm\_chain.get\_relevant\_documents(  
 "Hi I'm Lance. What is Maximum Inner Product Search?"  
)  

```

```text
 INFO:langchain.retrievers.re\_phraser:Re-phrased question: Ahoy matey! What be Maximum Inner Product Search, ye scurvy dog?  

```

- [Example](#example)

  - [Setting up](#setting-up)
  - [Using the default prompt](#using-the-default-prompt)
  - [Custom prompt](#custom-prompt)

- [Setting up](#setting-up)

- [Using the default prompt](#using-the-default-prompt)

- [Custom prompt](#custom-prompt)

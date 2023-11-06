# Loading from LangChainHub

This notebook covers how to load chains from [LangChainHub](https://github.com/hwchase17/langchain-hub).

```python
from langchain.chains import load\_chain  
  
chain = load\_chain("lc://chains/llm-math/chain.json")  

```

```python
chain.run("whats 2 raised to .12")  

```

```text
   
   
 > Entering new LLMMathChain chain...  
 whats 2 raised to .12  
 Answer: 1.0791812460476249  
 > Finished chain.  
  
  
  
  
  
 'Answer: 1.0791812460476249'  

```

Sometimes chains will require extra arguments that were not serialized with the chain. For example, a chain that does question answering over a vector database will require a vector database.

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import Chroma  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.llms import OpenAI  
from langchain.chains import VectorDBQA  

```

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
texts = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  
vectorstore = Chroma.from\_documents(texts, embeddings)  

```

```text
 Running Chroma using direct local API.  
 Using DuckDB in-memory for database. Data will be transient.  

```

```python
chain = load\_chain("lc://chains/vector-db-qa/stuff/chain.json", vectorstore=vectorstore)  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
chain.run(query)  

```

```text
 " The president said that Ketanji Brown Jackson is a Circuit Court of Appeals Judge, one of the nation's top legal minds, a former top litigator in private practice, a former federal public defender, has received a broad range of support from the Fraternal Order of Police to former judges appointed by Democrats and Republicans, and will continue Justice Breyer's legacy of excellence."  

```

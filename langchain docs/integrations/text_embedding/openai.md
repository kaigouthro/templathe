# OpenAI

Let's load the OpenAI Embedding class.

```python
from langchain.embeddings import OpenAIEmbeddings  

```

```python
embeddings = OpenAIEmbeddings()  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

```python
query\_result[:5]  

```

```text
 [-0.003186025367556387,  
 0.011071979803637493,  
 -0.004020420763285827,  
 -0.011658221276953042,  
 -0.0010534035786864363]  

```

```python
doc\_result = embeddings.embed\_documents([text])  

```

```python
doc\_result[0][:5]  

```

```text
 [-0.003186025367556387,  
 0.011071979803637493,  
 -0.004020420763285827,  
 -0.011658221276953042,  
 -0.0010534035786864363]  

```

Let's load the OpenAI Embedding class with first generation models (e.g. text-search-ada-doc-001/text-search-ada-query-001). Note: These are not recommended models - see [here](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings)

```python
from langchain.embeddings.openai import OpenAIEmbeddings  

```

```python
embeddings = OpenAIEmbeddings(model="text-search-ada-doc-001")  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

```python
query\_result[:5]  

```

```text
 [0.004452846988523035,  
 0.034550655976098514,  
 -0.015029939040690051,  
 0.03827273883655212,  
 0.005785414075152477]  

```

```python
doc\_result = embeddings.embed\_documents([text])  

```

```python
doc\_result[0][:5]  

```

```text
 [0.004452846988523035,  
 0.034550655976098514,  
 -0.015029939040690051,  
 0.03827273883655212,  
 0.005785414075152477]  

```

```python
# if you are behind an explicit proxy, you can use the OPENAI\_PROXY environment variable to pass through  
os.environ["OPENAI\_PROXY"] = "http://proxy.yourcompany.com:8080"  

```

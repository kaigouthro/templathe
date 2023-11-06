# Ollama

Let's load the Ollama Embeddings class.

```python
from langchain.embeddings import OllamaEmbeddings  

```

```python
embeddings = OllamaEmbeddings()  

```

```python
text = "This is a test document."  

```

To generate embeddings, you can either query an invidivual text, or you can query a list of texts.

```python
query\_result = embeddings.embed\_query(text)  
query\_result[:5]  

```

```text
 [-0.09996652603149414,  
 0.015568195842206478,  
 0.17670190334320068,  
 0.16521021723747253,  
 0.21193109452724457]  

```

```python
doc\_result = embeddings.embed\_documents([text])  
doc\_result[0][:5]  

```

```text
 [-0.04242777079343796,  
 0.016536075621843338,  
 0.10052520781755447,  
 0.18272875249385834,  
 0.2079043835401535]  

```

Let's load the Ollama Embeddings class with smaller model (e.g. llama:7b). Note: See other supported models <https://ollama.ai/library>

```python
embeddings = OllamaEmbeddings(model="llama2:7b")  

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
 [-0.09996627271175385,  
 0.015567859634757042,  
 0.17670205235481262,  
 0.16521376371383667,  
 0.21193283796310425]  

```

```python
doc\_result = embeddings.embed\_documents([text])  

```

```python
doc\_result[0][:5]  

```

```text
 [-0.042427532374858856,  
 0.01653730869293213,  
 0.10052604228258133,  
 0.18272635340690613,  
 0.20790338516235352]  

```

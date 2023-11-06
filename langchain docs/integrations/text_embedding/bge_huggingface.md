# BGE on Hugging Face

[BGE models on the HuggingFace](https://huggingface.co/BAAI/bge-large-en) are [the best open-source embedding models](https://huggingface.co/spaces/mteb/leaderboard).
BGE model is created by the [Beijing Academy of Artificial Intelligence (BAAI)](https://www.baai.ac.cn/english.html). `BAAI` is a private non-profit organization engaged in AI research and development.

This notebook shows how to use `BGE Embeddings` through `Hugging Face`

```python
#!pip install sentence\_transformers  

```

```python
from langchain.embeddings import HuggingFaceBgeEmbeddings  
  
model\_name = "BAAI/bge-small-en"  
model\_kwargs = {'device': 'cpu'}  
encode\_kwargs = {'normalize\_embeddings': True}  
hf = HuggingFaceBgeEmbeddings(  
 model\_name=model\_name,  
 model\_kwargs=model\_kwargs,  
 encode\_kwargs=encode\_kwargs  
)  

```

```python
embedding = hf.embed\_query("hi this is harrison")  
len(embedding)  

```

```text
 384  

```

# NLP Cloud

[NLP Cloud](https://docs.nlpcloud.com/#introduction) is an artificial intelligence platform that allows you to use the most advanced AI engines, and even train your own engines with your own data.

The [embeddings](https://docs.nlpcloud.com/#embeddings) endpoint offers the following model:

- `paraphrase-multilingual-mpnet-base-v2`: Paraphrase Multilingual MPNet Base V2 is a very fast model based on Sentence Transformers that is perfectly suited for embeddings extraction in more than 50 languages (see the full list here).

```bash
pip install nlpcloud  

```

```python
from langchain.embeddings import NLPCloudEmbeddings  

```

```python
import os  
  
os.environ["NLPCLOUD\_API\_KEY"] = "xxx"  
nlpcloud\_embd = NLPCloudEmbeddings()  

```

```python
text = "This is a test document."  

```

```python
query\_result = nlpcloud\_embd.embed\_query(text)  

```

```python
doc\_result = nlpcloud\_embd.embed\_documents([text])  

```

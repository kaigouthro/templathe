# Sentence Transformers

[SentenceTransformers](https://www.sbert.net/) embeddings are called using the `HuggingFaceEmbeddings` integration. We have also added an alias for `SentenceTransformerEmbeddings` for users who are more familiar with directly using that package.

`SentenceTransformers` is a python package that can generate text and image embeddings, originating from [Sentence-BERT](https://arxiv.org/abs/1908.10084)

```bash
pip install sentence\_transformers > /dev/null  

```

```text
   
 [notice] A new release of pip is available: 23.0.1 -> 23.1.1  
 [notice] To update, run: pip install --upgrade pip  

```

```python
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings  

```

```python
embeddings = HuggingFaceEmbeddings(model\_name="all-MiniLM-L6-v2")  
# Equivalent to SentenceTransformerEmbeddings(model\_name="all-MiniLM-L6-v2")  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

```python
doc\_result = embeddings.embed\_documents([text, "This is not a test document."])  

```

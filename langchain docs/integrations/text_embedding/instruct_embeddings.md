# InstructEmbeddings

Let's load the HuggingFace instruct Embeddings class.

```python
from langchain.embeddings import HuggingFaceInstructEmbeddings  

```

```python
embeddings = HuggingFaceInstructEmbeddings(  
 query\_instruction="Represent the query for retrieval: "  
)  

```

```text
 load INSTRUCTOR\_Transformer  
 max\_seq\_length 512  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

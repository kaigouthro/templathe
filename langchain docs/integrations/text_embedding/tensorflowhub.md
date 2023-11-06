# TensorflowHub

Let's load the TensorflowHub Embedding class.

```python
from langchain.embeddings import TensorflowHubEmbeddings  

```

```python
embeddings = TensorflowHubEmbeddings()  

```

```text
 2023-01-30 23:53:01.652176: I tensorflow/core/platform/cpu\_feature\_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations: AVX2 FMA  
 To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.  
 2023-01-30 23:53:34.362802: I tensorflow/core/platform/cpu\_feature\_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations: AVX2 FMA  
 To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.  

```

```python
text = "This is a test document."  

```

```python
query\_result = embeddings.embed\_query(text)  

```

```python
doc\_results = embeddings.embed\_documents(["foo"])  

```

```python
doc\_results  

```

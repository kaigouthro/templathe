# Llama-cpp

This notebook goes over how to use Llama-cpp embeddings within LangChain

```bash
pip install llama-cpp-python  

```

```python
from langchain.embeddings import LlamaCppEmbeddings  

```

```python
llama = LlamaCppEmbeddings(model\_path="/path/to/model/ggml-model-q4\_0.bin")  

```

```python
text = "This is a test document."  

```

```python
query\_result = llama.embed\_query(text)  

```

```python
doc\_result = llama.embed\_documents([text])  

```

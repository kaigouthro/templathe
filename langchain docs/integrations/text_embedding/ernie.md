# ERNIE Embedding-V1

[ERNIE Embedding-V1](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/alj562vvu) is a text representation model based on Baidu Wenxin's large-scale model technology,
which converts text into a vector form represented by numerical values, and is used in text retrieval, information recommendation, knowledge mining and other scenarios.

```text
from langchain.embeddings import ErnieEmbeddings  

```

```text
embeddings = ErnieEmbeddings()  

```

```text
query\_result = embeddings.embed\_query("foo")  

```

```text
doc\_results = embeddings.embed\_documents(["foo"])  

```

# Merge Documents Loader

Merge the documents returned from a set of specified data loaders.

```python
from langchain.document\_loaders import WebBaseLoader  
  
loader\_web = WebBaseLoader(  
 "https://github.com/basecamp/handbook/blob/master/37signals-is-you.md"  
)  

```

```python
from langchain.document\_loaders import PyPDFLoader  
  
loader\_pdf = PyPDFLoader("../MachineLearning-Lecture01.pdf")  

```

```python
from langchain.document\_loaders.merge import MergedDataLoader  
  
loader\_all = MergedDataLoader(loaders=[loader\_web, loader\_pdf])  

```

```python
docs\_all = loader\_all.load()  

```

```python
len(docs\_all)  

```

```text
 23  

```

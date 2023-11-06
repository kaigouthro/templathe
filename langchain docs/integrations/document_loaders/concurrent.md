# Concurrent Loader

Works just like the GenericLoader but concurrently for those who choose to optimize their workflow.

```python
from langchain.document\_loaders import ConcurrentLoader  

```

```python
loader = ConcurrentLoader.from\_filesystem('example\_data/', glob="\*\*/\*.txt")  

```

```python
files = loader.load()  

```

```python
len(files)  

```

```text
 2  

```

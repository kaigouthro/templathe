# Git

[Git](https://en.wikipedia.org/wiki/Git) is a distributed version control system that tracks changes in any set of computer files, usually used for coordinating work among programmers collaboratively developing source code during software development.

This notebook shows how to load text files from `Git` repository.

## Load existing repository from disk[​](#load-existing-repository-from-disk "Direct link to Load existing repository from disk")

```bash
pip install GitPython  

```

```python
from git import Repo  
  
repo = Repo.clone\_from(  
 "https://github.com/langchain-ai/langchain", to\_path="./example\_data/test\_repo1"  
)  
branch = repo.head.reference  

```

```python
from langchain.document\_loaders import GitLoader  

```

```python
loader = GitLoader(repo\_path="./example\_data/test\_repo1/", branch=branch)  

```

```python
data = loader.load()  

```

```python
len(data)  

```

```python
print(data[0])  

```

```text
 page\_content='.venv\n.github\n.git\n.mypy\_cache\n.pytest\_cache\nDockerfile' metadata={'file\_path': '.dockerignore', 'file\_name': '.dockerignore', 'file\_type': ''}  

```

## Clone repository from url[​](#clone-repository-from-url "Direct link to Clone repository from url")

```python
from langchain.document\_loaders import GitLoader  

```

```python
loader = GitLoader(  
 clone\_url="https://github.com/langchain-ai/langchain",  
 repo\_path="./example\_data/test\_repo2/",  
 branch="master",  
)  

```

```python
data = loader.load()  

```

```python
len(data)  

```

```text
 1074  

```

## Filtering files to load[​](#filtering-files-to-load "Direct link to Filtering files to load")

```python
from langchain.document\_loaders import GitLoader  
  
# e.g. loading only python files  
loader = GitLoader(  
 repo\_path="./example\_data/test\_repo1/",  
 file\_filter=lambda file\_path: file\_path.endswith(".py"),  
)  

```

- [Load existing repository from disk](#load-existing-repository-from-disk)
- [Clone repository from url](#clone-repository-from-url)
- [Filtering files to load](#filtering-files-to-load)

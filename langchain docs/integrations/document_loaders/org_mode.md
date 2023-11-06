# Org-mode

A [Org Mode document](https://en.wikipedia.org/wiki/Org-mode) is a document editing, formatting, and organizing mode, designed for notes, planning, and authoring within the free software text editor Emacs.

## `UnstructuredOrgModeLoader`[​](#unstructuredorgmodeloader "Direct link to unstructuredorgmodeloader")

You can load data from Org-mode files with `UnstructuredOrgModeLoader` using the following workflow.

```python
from langchain.document\_loaders import UnstructuredOrgModeLoader  

```

```python
loader = UnstructuredOrgModeLoader(file\_path="example\_data/README.org", mode="elements")  
docs = loader.load()  

```

```python
print(docs[0])  

```

```text
 page\_content='Example Docs' metadata={'source': 'example\_data/README.org', 'filename': 'README.org', 'file\_directory': 'example\_data', 'filetype': 'text/org', 'page\_number': 1, 'category': 'Title'}  

```

- [`UnstructuredOrgModeLoader`](#unstructuredorgmodeloader)

# Microsoft Word

[Microsoft Word](https://www.microsoft.com/en-us/microsoft-365/word) is a word processor developed by Microsoft.

This covers how to load `Word` documents into a document format that we can use downstream.

## Using Docx2txt[​](#using-docx2txt "Direct link to Using Docx2txt")

Load .docx using `Docx2txt` into a document.

```bash
pip install docx2txt  

```

```python
from langchain.document\_loaders import Docx2txtLoader  

```

```python
loader = Docx2txtLoader("example\_data/fake.docx")  

```

```python
data = loader.load()  

```

```python
data  

```

```text
 [Document(page\_content='Lorem ipsum dolor sit amet.', metadata={'source': 'example\_data/fake.docx'})]  

```

## Using Unstructured[​](#using-unstructured "Direct link to Using Unstructured")

```python
from langchain.document\_loaders import UnstructuredWordDocumentLoader  

```

```python
loader = UnstructuredWordDocumentLoader("example\_data/fake.docx")  

```

```python
data = loader.load()  

```

```python
data  

```

```text
 [Document(page\_content='Lorem ipsum dolor sit amet.', lookup\_str='', metadata={'source': 'fake.docx'}, lookup\_index=0)]  

```

## Retain Elements[​](#retain-elements "Direct link to Retain Elements")

Under the hood, Unstructured creates different "elements" for different chunks of text. By default we combine those together, but you can easily keep that separation by specifying `mode="elements"`.

```python
loader = UnstructuredWordDocumentLoader("example\_data/fake.docx", mode="elements")  

```

```python
data = loader.load()  

```

```python
data[0]  

```

```text
 Document(page\_content='Lorem ipsum dolor sit amet.', lookup\_str='', metadata={'source': 'fake.docx', 'filename': 'fake.docx', 'category': 'Title'}, lookup\_index=0)  

```

- [Using Docx2txt](#using-docx2txt)
- [Using Unstructured](#using-unstructured)
- [Retain Elements](#retain-elements)

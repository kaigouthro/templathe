# Microsoft PowerPoint

[Microsoft PowerPoint](https://en.wikipedia.org/wiki/Microsoft_PowerPoint) is a presentation program by Microsoft.

This covers how to load `Microsoft PowerPoint` documents into a document format that we can use downstream.

```python
from langchain.document\_loaders import UnstructuredPowerPointLoader  

```

```python
loader = UnstructuredPowerPointLoader("example\_data/fake-power-point.pptx")  

```

```python
data = loader.load()  

```

```python
data  

```

```text
 [Document(page\_content='Adding a Bullet Slide\n\nFind the bullet slide layout\n\nUse \_TextFrame.text for first bullet\n\nUse \_TextFrame.add\_paragraph() for subsequent bullets\n\nHere is a lot of text!\n\nHere is some text in a text box!', metadata={'source': 'example\_data/fake-power-point.pptx'})]  

```

## Retain Elements[​](#retain-elements "Direct link to Retain Elements")

Under the hood, `Unstructured` creates different "elements" for different chunks of text. By default we combine those together, but you can easily keep that separation by specifying `mode="elements"`.

```python
loader = UnstructuredPowerPointLoader(  
 "example\_data/fake-power-point.pptx", mode="elements"  
)  

```

```python
data = loader.load()  

```

```python
data[0]  

```

```text
 Document(page\_content='Adding a Bullet Slide', lookup\_str='', metadata={'source': 'example\_data/fake-power-point.pptx'}, lookup\_index=0)  

```

- [Retain Elements](#retain-elements)

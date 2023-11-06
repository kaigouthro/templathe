# HTML

[The HyperText Markup Language or HTML](https://en.wikipedia.org/wiki/HTML) is the standard markup language for documents designed to be displayed in a web browser.

This covers how to load `HTML` documents into a document format that we can use downstream.

```python
from langchain.document\_loaders import UnstructuredHTMLLoader  

```

```python
loader = UnstructuredHTMLLoader("example\_data/fake-content.html")  

```

```python
data = loader.load()  

```

```python
data  

```

```text
 [Document(page\_content='My First Heading\n\nMy first paragraph.', lookup\_str='', metadata={'source': 'example\_data/fake-content.html'}, lookup\_index=0)]  

```

## Loading HTML with BeautifulSoup4[​](#loading-html-with-beautifulsoup4 "Direct link to Loading HTML with BeautifulSoup4")

We can also use `BeautifulSoup4` to load HTML documents using the `BSHTMLLoader`. This will extract the text from the HTML into `page_content`, and the page title as `title` into `metadata`.

```python
from langchain.document\_loaders import BSHTMLLoader  

```

```python
loader = BSHTMLLoader("example\_data/fake-content.html")  
data = loader.load()  
data  

```

```text
 [Document(page\_content='\n\nTest Title\n\n\nMy First Heading\nMy first paragraph.\n\n\n', metadata={'source': 'example\_data/fake-content.html', 'title': 'Test Title'})]  

```

- [Loading HTML with BeautifulSoup4](#loading-html-with-beautifulsoup4)

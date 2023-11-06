# MarkdownHeaderTextSplitter

### Motivation[​](#motivation "Direct link to Motivation")

Many chat or Q+A applications involve chunking input documents prior to embedding and vector storage.

[These notes](https://www.pinecone.io/learn/chunking-strategies/) from Pinecone provide some useful tips:

```text
When a full paragraph or document is embedded, the embedding process considers both the overall context and the relationships between the sentences and phrases within the text. This can result in a more comprehensive vector representation that captures the broader meaning and themes of the text.  

```

As mentioned, chunking often aims to keep text with common context together. With this in mind, we might want to specifically honor the structure of the document itself. For example, a markdown file is organized by headers. Creating chunks within specific header groups is an intuitive idea. To address this challenge, we can use `MarkdownHeaderTextSplitter`. This will split a markdown file by a specified set of headers.

For example, if we want to split this markdown:

```text
md = '# Foo\n\n ## Bar\n\nHi this is Jim \nHi this is Joe\n\n ## Baz\n\n Hi this is Molly'   

```

We can specify the headers to split on:

```text
[("#", "Header 1"),("##", "Header 2")]  

```

And content is grouped or split by common headers:

```text
{'content': 'Hi this is Jim \nHi this is Joe', 'metadata': {'Header 1': 'Foo', 'Header 2': 'Bar'}}  
{'content': 'Hi this is Molly', 'metadata': {'Header 1': 'Foo', 'Header 2': 'Baz'}}  

```

Let's have a look at some examples below.

```python
from langchain.text\_splitter import MarkdownHeaderTextSplitter  

```

```python
markdown\_document = "# Foo\n\n ## Bar\n\nHi this is Jim\n\nHi this is Joe\n\n ### Boo \n\n Hi this is Lance \n\n ## Baz\n\n Hi this is Molly"  
  
headers\_to\_split\_on = [  
 ("#", "Header 1"),  
 ("##", "Header 2"),  
 ("###", "Header 3"),  
]  
  
markdown\_splitter = MarkdownHeaderTextSplitter(headers\_to\_split\_on=headers\_to\_split\_on)  
md\_header\_splits = markdown\_splitter.split\_text(markdown\_document)  
md\_header\_splits  

```

```text
 [Document(page\_content='Hi this is Jim \nHi this is Joe', metadata={'Header 1': 'Foo', 'Header 2': 'Bar'}),  
 Document(page\_content='Hi this is Lance', metadata={'Header 1': 'Foo', 'Header 2': 'Bar', 'Header 3': 'Boo'}),  
 Document(page\_content='Hi this is Molly', metadata={'Header 1': 'Foo', 'Header 2': 'Baz'})]  

```

```python
type(md\_header\_splits[0])  

```

```text
 langchain.schema.document.Document  

```

Within each markdown group we can then apply any text splitter we want.

```python
markdown\_document = "# Intro \n\n ## History \n\n Markdown[9] is a lightweight markup language for creating formatted text using a plain-text editor. John Gruber created Markdown in 2004 as a markup language that is appealing to human readers in its source code form.[9] \n\n Markdown is widely used in blogging, instant messaging, online forums, collaborative software, documentation pages, and readme files. \n\n ## Rise and divergence \n\n As Markdown popularity grew rapidly, many Markdown implementations appeared, driven mostly by the need for \n\n additional features such as tables, footnotes, definition lists,[note 1] and Markdown inside HTML blocks. \n\n #### Standardization \n\n From 2012, a group of people, including Jeff Atwood and John MacFarlane, launched what Atwood characterised as a standardisation effort. \n\n ## Implementations \n\n Implementations of Markdown are available for over a dozen programming languages."  
  
headers\_to\_split\_on = [  
 ("#", "Header 1"),  
 ("##", "Header 2"),  
]  
  
# MD splits  
markdown\_splitter = MarkdownHeaderTextSplitter(headers\_to\_split\_on=headers\_to\_split\_on)  
md\_header\_splits = markdown\_splitter.split\_text(markdown\_document)  
  
# Char-level splits  
from langchain.text\_splitter import RecursiveCharacterTextSplitter  
  
chunk\_size = 250  
chunk\_overlap = 30  
text\_splitter = RecursiveCharacterTextSplitter(  
 chunk\_size=chunk\_size, chunk\_overlap=chunk\_overlap  
)  
  
# Split  
splits = text\_splitter.split\_documents(md\_header\_splits)  
splits  

```

```text
 [Document(page\_content='Markdown[9] is a lightweight markup language for creating formatted text using a plain-text editor. John Gruber created Markdown in 2004 as a markup language that is appealing to human readers in its source code form.[9]', metadata={'Header 1': 'Intro', 'Header 2': 'History'}),  
 Document(page\_content='Markdown is widely used in blogging, instant messaging, online forums, collaborative software, documentation pages, and readme files.', metadata={'Header 1': 'Intro', 'Header 2': 'History'}),  
 Document(page\_content='As Markdown popularity grew rapidly, many Markdown implementations appeared, driven mostly by the need for \nadditional features such as tables, footnotes, definition lists,[note 1] and Markdown inside HTML blocks. \n#### Standardization', metadata={'Header 1': 'Intro', 'Header 2': 'Rise and divergence'}),  
 Document(page\_content='#### Standardization \nFrom 2012, a group of people, including Jeff Atwood and John MacFarlane, launched what Atwood characterised as a standardisation effort.', metadata={'Header 1': 'Intro', 'Header 2': 'Rise and divergence'}),  
 Document(page\_content='Implementations of Markdown are available for over a dozen programming languages.', metadata={'Header 1': 'Intro', 'Header 2': 'Implementations'})]  

```

- [Motivation](#motivation)

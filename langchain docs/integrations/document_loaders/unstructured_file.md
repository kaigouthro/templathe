# Unstructured File

This notebook covers how to use `Unstructured` package to load files of many types. `Unstructured` currently supports loading of text files, powerpoints, html, pdfs, images, and more.

```bash
# # Install package  
pip install "unstructured[all-docs]"  

```

```python
# # Install other dependencies  
# # https://github.com/Unstructured-IO/unstructured/blob/main/docs/source/installing.rst  
# !brew install libmagic  
# !brew install poppler  
# !brew install tesseract  
# # If parsing xml / html documents:  
# !brew install libxml2  
# !brew install libxslt  

```

```python
# import nltk  
# nltk.download('punkt')  

```

```python
from langchain.document\_loaders import UnstructuredFileLoader  

```

```python
loader = UnstructuredFileLoader("./example\_data/state\_of\_the\_union.txt")  

```

```python
docs = loader.load()  

```

```python
docs[0].page\_content[:400]  

```

```text
 'Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.\n\nLast year COVID-19 kept us apart. This year we are finally together again.\n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans.\n\nWith a duty to one another to the American people to the Constit'  

```

## Retain Elements[​](#retain-elements "Direct link to Retain Elements")

Under the hood, Unstructured creates different "elements" for different chunks of text. By default we combine those together, but you can easily keep that separation by specifying `mode="elements"`.

```python
loader = UnstructuredFileLoader(  
 "./example\_data/state\_of\_the\_union.txt", mode="elements"  
)  

```

```python
docs = loader.load()  

```

```python
docs[:5]  

```

```text
 [Document(page\_content='Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.', lookup\_str='', metadata={'source': '../../state\_of\_the\_union.txt'}, lookup\_index=0),  
 Document(page\_content='Last year COVID-19 kept us apart. This year we are finally together again.', lookup\_str='', metadata={'source': '../../state\_of\_the\_union.txt'}, lookup\_index=0),  
 Document(page\_content='Tonight, we meet as Democrats Republicans and Independents. But most importantly as Americans.', lookup\_str='', metadata={'source': '../../state\_of\_the\_union.txt'}, lookup\_index=0),  
 Document(page\_content='With a duty to one another to the American people to the Constitution.', lookup\_str='', metadata={'source': '../../state\_of\_the\_union.txt'}, lookup\_index=0),  
 Document(page\_content='And with an unwavering resolve that freedom will always triumph over tyranny.', lookup\_str='', metadata={'source': '../../state\_of\_the\_union.txt'}, lookup\_index=0)]  

```

## Define a Partitioning Strategy[​](#define-a-partitioning-strategy "Direct link to Define a Partitioning Strategy")

Unstructured document loader allow users to pass in a `strategy` parameter that lets `unstructured` know how to partition the document. Currently supported strategies are `"hi_res"` (the default) and `"fast"`. Hi res partitioning strategies are more accurate, but take longer to process. Fast strategies partition the document more quickly, but trade-off accuracy. Not all document types have separate hi res and fast partitioning strategies. For those document types, the `strategy` kwarg is ignored. In some cases, the high res strategy will fallback to fast if there is a dependency missing (i.e. a model for document partitioning). You can see how to apply a strategy to an `UnstructuredFileLoader` below.

```python
from langchain.document\_loaders import UnstructuredFileLoader  

```

```python
loader = UnstructuredFileLoader(  
 "layout-parser-paper-fast.pdf", strategy="fast", mode="elements"  
)  

```

```python
docs = loader.load()  

```

```python
docs[:5]  

```

```text
 [Document(page\_content='1', lookup\_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page\_number': 1, 'category': 'UncategorizedText'}, lookup\_index=0),  
 Document(page\_content='2', lookup\_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page\_number': 1, 'category': 'UncategorizedText'}, lookup\_index=0),  
 Document(page\_content='0', lookup\_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page\_number': 1, 'category': 'UncategorizedText'}, lookup\_index=0),  
 Document(page\_content='2', lookup\_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page\_number': 1, 'category': 'UncategorizedText'}, lookup\_index=0),  
 Document(page\_content='n', lookup\_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page\_number': 1, 'category': 'Title'}, lookup\_index=0)]  

```

## PDF Example[​](#pdf-example "Direct link to PDF Example")

Processing PDF documents works exactly the same way. Unstructured detects the file type and extracts the same types of elements. Modes of operation are

- `single` all the text from all elements are combined into one (default)
- `elements` maintain individual elements
- `paged` texts from each page are only combined

```bash
wget https://raw.githubusercontent.com/Unstructured-IO/unstructured/main/example-docs/layout-parser-paper.pdf -P "../../"  

```

```python
loader = UnstructuredFileLoader(  
 "./example\_data/layout-parser-paper.pdf", mode="elements"  
)  

```

```python
docs = loader.load()  

```

```python
docs[:5]  

```

```text
 [Document(page\_content='LayoutParser : A Uniﬁed Toolkit for Deep Learning Based Document Image Analysis', lookup\_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup\_index=0),  
 Document(page\_content='Zejiang Shen 1 ( (ea)\n ), Ruochen Zhang 2 , Melissa Dell 3 , Benjamin Charles Germain Lee 4 , Jacob Carlson 3 , and Weining Li 5', lookup\_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup\_index=0),  
 Document(page\_content='Allen Institute for AI shannons@allenai.org', lookup\_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup\_index=0),  
 Document(page\_content='Brown University ruochen zhang@brown.edu', lookup\_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup\_index=0),  
 Document(page\_content='Harvard University { melissadell,jacob carlson } @fas.harvard.edu', lookup\_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup\_index=0)]  

```

If you need to post process the `unstructured` elements after extraction, you can pass in a list of `str` -> `str` functions to the `post_processors` kwarg when you instantiate the `UnstructuredFileLoader`. This applies to other Unstructured loaders as well. Below is an example.

```python
from langchain.document\_loaders import UnstructuredFileLoader  
from unstructured.cleaners.core import clean\_extra\_whitespace  

```

```python
loader = UnstructuredFileLoader(  
 "./example\_data/layout-parser-paper.pdf",  
 mode="elements",  
 post\_processors=[clean\_extra\_whitespace],  
)  

```

```python
docs = loader.load()  

```

```python
docs[:5]  

```

```text
 [Document(page\_content='LayoutParser: A Uniﬁed Toolkit for Deep Learning Based Document Image Analysis', metadata={'source': './example\_data/layout-parser-paper.pdf', 'coordinates': {'points': ((157.62199999999999, 114.23496279999995), (157.62199999999999, 146.5141628), (457.7358962799999, 146.5141628), (457.7358962799999, 114.23496279999995)), 'system': 'PixelSpace', 'layout\_width': 612, 'layout\_height': 792}, 'filename': 'layout-parser-paper.pdf', 'file\_directory': './example\_data', 'filetype': 'application/pdf', 'page\_number': 1, 'category': 'Title'}),  
 Document(page\_content='Zejiang Shen1 ((cid:0)), Ruochen Zhang2, Melissa Dell3, Benjamin Charles Germain Lee4, Jacob Carlson3, and Weining Li5', metadata={'source': './example\_data/layout-parser-paper.pdf', 'coordinates': {'points': ((134.809, 168.64029940800003), (134.809, 192.2517444), (480.5464199080001, 192.2517444), (480.5464199080001, 168.64029940800003)), 'system': 'PixelSpace', 'layout\_width': 612, 'layout\_height': 792}, 'filename': 'layout-parser-paper.pdf', 'file\_directory': './example\_data', 'filetype': 'application/pdf', 'page\_number': 1, 'category': 'UncategorizedText'}),  
 Document(page\_content='1 Allen Institute for AI shannons@allenai.org 2 Brown University ruochen zhang@brown.edu 3 Harvard University {melissadell,jacob carlson}@fas.harvard.edu 4 University of Washington bcgl@cs.washington.edu 5 University of Waterloo w422li@uwaterloo.ca', metadata={'source': './example\_data/layout-parser-paper.pdf', 'coordinates': {'points': ((207.23000000000002, 202.57205439999996), (207.23000000000002, 311.8195408), (408.12676, 311.8195408), (408.12676, 202.57205439999996)), 'system': 'PixelSpace', 'layout\_width': 612, 'layout\_height': 792}, 'filename': 'layout-parser-paper.pdf', 'file\_directory': './example\_data', 'filetype': 'application/pdf', 'page\_number': 1, 'category': 'UncategorizedText'}),  
 Document(page\_content='1 2 0 2', metadata={'source': './example\_data/layout-parser-paper.pdf', 'coordinates': {'points': ((16.34, 213.36), (16.34, 253.36), (36.34, 253.36), (36.34, 213.36)), 'system': 'PixelSpace', 'layout\_width': 612, 'layout\_height': 792}, 'filename': 'layout-parser-paper.pdf', 'file\_directory': './example\_data', 'filetype': 'application/pdf', 'page\_number': 1, 'category': 'UncategorizedText'}),  
 Document(page\_content='n u J', metadata={'source': './example\_data/layout-parser-paper.pdf', 'coordinates': {'points': ((16.34, 258.36), (16.34, 286.14), (36.34, 286.14), (36.34, 258.36)), 'system': 'PixelSpace', 'layout\_width': 612, 'layout\_height': 792}, 'filename': 'layout-parser-paper.pdf', 'file\_directory': './example\_data', 'filetype': 'application/pdf', 'page\_number': 1, 'category': 'Title'})]  

```

## Unstructured API[​](#unstructured-api "Direct link to Unstructured API")

If you want to get up and running with less set up, you can simply run `pip install unstructured` and use `UnstructuredAPIFileLoader` or `UnstructuredAPIFileIOLoader`. That will process your document using the hosted Unstructured API. You can generate a free Unstructured API key [here](https://www.unstructured.io/api-key/). The [Unstructured documentation](https://unstructured-io.github.io/) page will have instructions on how to generate an API key once they’re available. Check out the instructions [here](https://github.com/Unstructured-IO/unstructured-api#dizzy-instructions-for-using-the-docker-image) if you’d like to self-host the Unstructured API or run it locally.

```python
from langchain.document\_loaders import UnstructuredAPIFileLoader  

```

```python
filenames = ["example\_data/fake.docx", "example\_data/fake-email.eml"]  

```

```python
loader = UnstructuredAPIFileLoader(  
 file\_path=filenames[0],  
 api\_key="FAKE\_API\_KEY",  
)  

```

```python
docs = loader.load()  
docs[0]  

```

```text
 Document(page\_content='Lorem ipsum dolor sit amet.', metadata={'source': 'example\_data/fake.docx'})  

```

You can also batch multiple files through the Unstructured API in a single API using `UnstructuredAPIFileLoader`.

```python
loader = UnstructuredAPIFileLoader(  
 file\_path=filenames,  
 api\_key="FAKE\_API\_KEY",  
)  

```

```python
docs = loader.load()  
docs[0]  

```

```text
 Document(page\_content='Lorem ipsum dolor sit amet.\n\nThis is a test email to use for unit tests.\n\nImportant points:\n\nRoses are red\n\nViolets are blue', metadata={'source': ['example\_data/fake.docx', 'example\_data/fake-email.eml']})  

```

- [Retain Elements](#retain-elements)
- [Define a Partitioning Strategy](#define-a-partitioning-strategy)
- [PDF Example](#pdf-example)
- [Unstructured API](#unstructured-api)

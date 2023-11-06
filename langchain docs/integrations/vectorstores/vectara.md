# Vectara

[Vectara](https://vectara.com/) is a API platform for building GenAI applications. It provides an easy-to-use API for document indexing and querying that is managed by Vectara and is optimized for performance and accuracy.
See the [Vectara API documentation](https://docs.vectara.com/docs/)  for more information on how to use the API.

This notebook shows how to use functionality related to the `Vectara`'s integration with langchain.
Note that unlike many other integrations in this category, Vectara provides an end-to-end managed service for [Grounded Generation](https://vectara.com/grounded-generation/) (aka retrieval augmented generation), which includes:

1. A way to extract text from document files and chunk them into sentences.
1. Its own embeddings model and vector store - each text segment is encoded into a vector embedding and stored in the Vectara internal vector store
1. A query service that automatically encodes the query into embedding, and retrieves the most relevant text segments (including support for [Hybrid Search](https://docs.vectara.com/docs/api-reference/search-apis/lexical-matching))

All of these are supported in this LangChain integration.

# Setup

You will need a Vectara account to use Vectara with LangChain. To get started, use the following steps (see our [quickstart](https://docs.vectara.com/docs/quickstart) guide):

1. [Sign up](https://vectara.com/integrations/langchain) for a Vectara account if you don't already have one. Once you have completed your sign up you will have a Vectara customer ID. You can find your customer ID by clicking on your name, on the top-right of the Vectara console window.
1. Within your account you can create one or more corpora. Each corpus represents an area that stores text data upon ingest from input documents. To create a corpus, use the **"Create Corpus"** button. You then provide a name to your corpus as well as a description. Optionally you can define filtering attributes and apply some advanced options. If you click on your created corpus, you can see its name and corpus ID right on the top.
1. Next you'll need to create API keys to access the corpus. Click on the **"Authorization"** tab in the corpus view and then the **"Create API Key"** button. Give your key a name, and choose whether you want query only or query+index for your key. Click "Create" and you now have an active API key. Keep this key confidential.

To use LangChain with Vectara, you'll need to have these three values: customer ID, corpus ID and api_key.
You can provide those to LangChain in two ways:

1. Include in your environment these three variables: `VECTARA_CUSTOMER_ID`, `VECTARA_CORPUS_ID` and `VECTARA_API_KEY`.

For example, you can set these variables using os.environ and getpass as follows:

```python
import os  
import getpass  
  
os.environ["VECTARA\_CUSTOMER\_ID"] = getpass.getpass("Vectara Customer ID:")  
os.environ["VECTARA\_CORPUS\_ID"] = getpass.getpass("Vectara Corpus ID:")  
os.environ["VECTARA\_API\_KEY"] = getpass.getpass("Vectara API Key:")  

```

1. Provide them as arguments when creating the Vectara vectorstore object:

```python
vectorstore = Vectara(  
 vectara\_customer\_id=vectara\_customer\_id,  
 vectara\_corpus\_id=vectara\_corpus\_id,  
 vectara\_api\_key=vectara\_api\_key  
 )  

```

## Connecting to Vectara from LangChain[​](#connecting-to-vectara-from-langchain "Direct link to Connecting to Vectara from LangChain")

In this example, we assume that you've created an account and a corpus, and added your VECTARA_CUSTOMER_ID, VECTARA_CORPUS_ID and VECTARA_API_KEY (created with permissions for both indexing and query) as environment variables.

The corpus has 3 fields defined as metadata for filtering:

- url: a string field containing the source URL of the document (where relevant)
- speech: a string field containing the name of the speech
- author: the name of the author

Let's start by ingesting 3 documents into the corpus:

1. The State of the Union speech from 2022, available in the LangChain repository as a text file
1. The "I have a dream" speech by Dr. Kind
1. The "We shall Fight on the Beaches" speech by Winston Churchil

```python
from langchain.embeddings import FakeEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import Vectara  
from langchain.document\_loaders import TextLoader  
  
from langchain.llms import OpenAI  
from langchain.chains import ConversationalRetrievalChain  
from langchain.retrievers.self\_query.base import SelfQueryRetriever  
from langchain.chains.query\_constructor.base import AttributeInfo  

```

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  

```

```python
vectara = Vectara.from\_documents(  
 docs,  
 embedding=FakeEmbeddings(size=768),  
 doc\_metadata={"speech": "state-of-the-union", "author": "Biden"},  
)  

```

Vectara's indexing API provides a file upload API where the file is handled directly by Vectara - pre-processed, chunked optimally and added to the Vectara vector store.
To use this, we added the add_files() method (as well as from_files()).

Let's see this in action. We pick two PDF documents to upload:

1. The "I have a dream" speech by Dr. King
1. Churchill's "We Shall Fight on the Beaches" speech

```python
import tempfile  
import urllib.request  
  
urls = [  
 [  
 "https://www.gilderlehrman.org/sites/default/files/inline-pdfs/king.dreamspeech.excerpts.pdf",  
 "I-have-a-dream",  
 "Dr. King"  
 ],  
 [  
 "https://www.parkwayschools.net/cms/lib/MO01931486/Centricity/Domain/1578/Churchill\_Beaches\_Speech.pdf",  
 "we shall fight on the beaches",  
 "Churchil"  
 ],  
]  
files\_list = []  
for url, \_, \_ in urls:  
 name = tempfile.NamedTemporaryFile().name  
 urllib.request.urlretrieve(url, name)  
 files\_list.append(name)  
  
docsearch: Vectara = Vectara.from\_files(  
 files=files\_list,  
 embedding=FakeEmbeddings(size=768),  
 metadatas=[{"url": url, "speech": title, "author": author} for url, title, author in urls],  
)  

```

## Similarity search[​](#similarity-search "Direct link to Similarity search")

The simplest scenario for using Vectara is to perform a similarity search.

```python
query = "What did the president say about Ketanji Brown Jackson"  
found\_docs = vectara.similarity\_search(  
 query, n\_sentence\_context=0, filter="doc.speech = 'state-of-the-union'"  
)  

```

```python
print(found\_docs[0].page\_content)  

```

```text
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson.  

```

## Similarity search with score[​](#similarity-search-with-score "Direct link to Similarity search with score")

Sometimes we might want to perform the search, but also obtain a relevancy score to know how good is a particular result.

```python
query = "What did the president say about Ketanji Brown Jackson"  
found\_docs = vectara.similarity\_search\_with\_score(  
 query, filter="doc.speech = 'state-of-the-union'", score\_threshold=0.2,  
)  

```

```python
document, score = found\_docs[0]  
print(document.page\_content)  
print(f"\nScore: {score}")  

```

```text
 Justice Breyer, thank you for your service. One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence. A former top litigator in private practice.  
   
 Score: 0.8299499  

```

Now let's do similar search for content in the files we uploaded

```python
query = "We must forever conduct our struggle"  
min\_score = 1.2  
found\_docs = vectara.similarity\_search\_with\_score(  
 query, filter="doc.speech = 'I-have-a-dream'", score\_threshold=min\_score,  
)  
print(f"With this threshold of {min\_score} we have {len(found\_docs)} documents")  

```

```text
 With this threshold of 1.2 we have 0 documents  

```

```python
query = "We must forever conduct our struggle"  
min\_score = 0.2  
found\_docs = vectara.similarity\_search\_with\_score(  
 query, filter="doc.speech = 'I-have-a-dream'", score\_threshold=min\_score,  
)  
print(f"With this threshold of {min\_score} we have {len(found\_docs)} documents")  

```

```text
 With this threshold of 0.2 we have 5 documents  

```

## Vectara as a Retriever[​](#vectara-as-a-retriever "Direct link to Vectara as a Retriever")

Vectara, as all the other LangChain vectorstores, is most often used as a LangChain Retriever:

```python
retriever = vectara.as\_retriever()  
retriever  

```

```text
 VectaraRetriever(tags=['Vectara'], metadata=None, vectorstore=<langchain.vectorstores.vectara.Vectara object at 0x13b15e9b0>, search\_type='similarity', search\_kwargs={'lambda\_val': 0.025, 'k': 5, 'filter': '', 'n\_sentence\_context': '2'})  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
retriever.get\_relevant\_documents(query)[0]  

```

```text
 Document(page\_content='Justice Breyer, thank you for your service. One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence. A former top litigator in private practice.', metadata={'source': 'langchain', 'lang': 'eng', 'offset': '596', 'len': '97', 'speech': 'state-of-the-union', 'author': 'Biden'})  

```

## Using Vectara as a SelfQuery Retriever[​](#using-vectara-as-a-selfquery-retriever "Direct link to Using Vectara as a SelfQuery Retriever")

```python
metadata\_field\_info = [  
 AttributeInfo(  
 name="speech",  
 description="what name of the speech",  
 type="string or list[string]",  
 ),  
 AttributeInfo(  
 name="author",  
 description="author of the speech",  
 type="string or list[string]",  
 ),  
]  
document\_content\_description = "the text of the speech"  
  
vectordb = Vectara()  
llm = OpenAI(temperature=0)  
retriever = SelfQueryRetriever.from\_llm(llm, vectara,   
 document\_content\_description, metadata\_field\_info,   
 verbose=True)  

```

```python
retriever.get\_relevant\_documents("what did Biden say about the freedom?")  

```

```text
 /Users/ofer/dev/langchain/libs/langchain/langchain/chains/llm.py:278: UserWarning: The predict\_and\_parse method is deprecated, instead pass an output parser directly to LLMChain.  
 warnings.warn(  
  
  
 query='freedom' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='author', value='Biden') limit=None  
  
  
  
  
  
 [Document(page\_content='Well I know this nation. We will meet the test. To protect freedom and liberty, to expand fairness and opportunity. We will save democracy. As hard as these times have been, I am more optimistic about America today than I have been my whole life.', metadata={'source': 'langchain', 'lang': 'eng', 'offset': '346', 'len': '67', 'speech': 'state-of-the-union', 'author': 'Biden'}),  
 Document(page\_content='To our fellow Ukrainian Americans who forge a deep bond that connects our two nations we stand with you. Putin may circle Kyiv with tanks, but he will never gain the hearts and souls of the Ukrainian people. He will never extinguish their love of freedom. He will never weaken the resolve of the free world. We meet tonight in an America that has lived through two of the hardest years this nation has ever faced.', metadata={'source': 'langchain', 'lang': 'eng', 'offset': '740', 'len': '47', 'speech': 'state-of-the-union', 'author': 'Biden'}),  
 Document(page\_content='But most importantly as Americans. With a duty to one another to the American people to the Constitution. And with an unwavering resolve that freedom will always triumph over tyranny. Six days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated.', metadata={'source': 'langchain', 'lang': 'eng', 'offset': '413', 'len': '77', 'speech': 'state-of-the-union', 'author': 'Biden'}),  
 Document(page\_content='We can do this. \n\nMy fellow Americans—tonight , we have gathered in a sacred space—the citadel of our democracy. In this Capitol, generation after generation, Americans have debated great questions amid great strife, and have done great things. We have fought for freedom, expanded liberty, defeated totalitarianism and terror. And built the strongest, freest, and most prosperous nation the world has ever known. Now is the hour. \n\nOur moment of responsibility.', metadata={'source': 'langchain', 'lang': 'eng', 'offset': '906', 'len': '82', 'speech': 'state-of-the-union', 'author': 'Biden'}),  
 Document(page\_content='In state after state, new laws have been passed, not only to suppress the vote, but to subvert entire elections. We cannot let this happen. Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.', metadata={'source': 'langchain', 'lang': 'eng', 'offset': '0', 'len': '63', 'speech': 'state-of-the-union', 'author': 'Biden'})]  

```

```python
retriever.get\_relevant\_documents("what did Dr. King say about the freedom?")  

```

```text
 query='freedom' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='author', value='Dr. King') limit=None  
  
  
  
  
  
 [Document(page\_content='And if America is to be a great nation, this must become true. So\nlet freedom ring from the prodigious hilltops of New Hampshire. Let freedom ring from the mighty\nmountains of New York. Let freedom ring from the heightening Alleghenies of Pennsylvania. Let\nfreedom ring from the snowcapped Rockies of Colorado.', metadata={'lang': 'eng', 'section': '3', 'offset': '1534', 'len': '55', 'CreationDate': '1424880481', 'Producer': 'Adobe PDF Library 10.0', 'Author': 'Sasha Rolon-Pereira', 'Title': 'Martin Luther King Jr.pdf', 'Creator': 'Acrobat PDFMaker 10.1 for Word', 'ModDate': '1424880524', 'url': 'https://www.gilderlehrman.org/sites/default/files/inline-pdfs/king.dreamspeech.excerpts.pdf', 'speech': 'I-have-a-dream', 'author': 'Dr. King', 'title': 'Martin Luther King Jr.pdf'}),  
 Document(page\_content='And if America is to be a great nation, this must become true. So\nlet freedom ring from the prodigious hilltops of New Hampshire. Let freedom ring from the mighty\nmountains of New York. Let freedom ring from the heightening Alleghenies of Pennsylvania. Let\nfreedom ring from the snowcapped Rockies of Colorado.', metadata={'lang': 'eng', 'section': '3', 'offset': '1534', 'len': '55', 'CreationDate': '1424880481', 'Producer': 'Adobe PDF Library 10.0', 'Author': 'Sasha Rolon-Pereira', 'Title': 'Martin Luther King Jr.pdf', 'Creator': 'Acrobat PDFMaker 10.1 for Word', 'ModDate': '1424880524', 'url': 'https://www.gilderlehrman.org/sites/default/files/inline-pdfs/king.dreamspeech.excerpts.pdf', 'speech': 'I-have-a-dream', 'author': 'Dr. King', 'title': 'Martin Luther King Jr.pdf'}),  
 Document(page\_content='Let freedom ring from the curvaceous slopes of\nCalifornia. But not only that. Let freedom ring from Stone Mountain of Georgia. Let freedom ring from Lookout\nMountain of Tennessee. Let freedom ring from every hill and molehill of Mississippi, from every\nmountain side. Let freedom ring . . .\nWhen we allow freedom to ring—when we let it ring from every city and every hamlet, from every state\nand every city, we will be able to speed up that day when all of God’s children, black men and white\nmen, Jews and Gentiles, Protestants and Catholics, will be able to join hands and sing in the words of the\nold Negro spiritual, “Free at last, Free at last, Great God a-mighty, We are free at last.”', metadata={'lang': 'eng', 'section': '3', 'offset': '1842', 'len': '52', 'CreationDate': '1424880481', 'Producer': 'Adobe PDF Library 10.0', 'Author': 'Sasha Rolon-Pereira', 'Title': 'Martin Luther King Jr.pdf', 'Creator': 'Acrobat PDFMaker 10.1 for Word', 'ModDate': '1424880524', 'url': 'https://www.gilderlehrman.org/sites/default/files/inline-pdfs/king.dreamspeech.excerpts.pdf', 'speech': 'I-have-a-dream', 'author': 'Dr. King', 'title': 'Martin Luther King Jr.pdf'}),  
 Document(page\_content='Let freedom ring from the curvaceous slopes of\nCalifornia. But not only that. Let freedom ring from Stone Mountain of Georgia. Let freedom ring from Lookout\nMountain of Tennessee. Let freedom ring from every hill and molehill of Mississippi, from every\nmountain side. Let freedom ring . . .\nWhen we allow freedom to ring—when we let it ring from every city and every hamlet, from every state\nand every city, we will be able to speed up that day when all of God’s children, black men and white\nmen, Jews and Gentiles, Protestants and Catholics, will be able to join hands and sing in the words of the\nold Negro spiritual, “Free at last, Free at last, Great God a-mighty, We are free at last.”', metadata={'lang': 'eng', 'section': '3', 'offset': '1842', 'len': '52', 'CreationDate': '1424880481', 'Producer': 'Adobe PDF Library 10.0', 'Author': 'Sasha Rolon-Pereira', 'Title': 'Martin Luther King Jr.pdf', 'Creator': 'Acrobat PDFMaker 10.1 for Word', 'ModDate': '1424880524', 'url': 'https://www.gilderlehrman.org/sites/default/files/inline-pdfs/king.dreamspeech.excerpts.pdf', 'speech': 'I-have-a-dream', 'author': 'Dr. King', 'title': 'Martin Luther King Jr.pdf'}),  
 Document(page\_content='Let freedom ring from the mighty\nmountains of New York. Let freedom ring from the heightening Alleghenies of Pennsylvania. Let\nfreedom ring from the snowcapped Rockies of Colorado. Let freedom ring from the curvaceous slopes of\nCalifornia. But not only that. Let freedom ring from Stone Mountain of Georgia.', metadata={'lang': 'eng', 'section': '3', 'offset': '1657', 'len': '57', 'CreationDate': '1424880481', 'Producer': 'Adobe PDF Library 10.0', 'Author': 'Sasha Rolon-Pereira', 'Title': 'Martin Luther King Jr.pdf', 'Creator': 'Acrobat PDFMaker 10.1 for Word', 'ModDate': '1424880524', 'url': 'https://www.gilderlehrman.org/sites/default/files/inline-pdfs/king.dreamspeech.excerpts.pdf', 'speech': 'I-have-a-dream', 'author': 'Dr. King', 'title': 'Martin Luther King Jr.pdf'})]  

```

- [Connecting to Vectara from LangChain](#connecting-to-vectara-from-langchain)
- [Similarity search](#similarity-search)
- [Similarity search with score](#similarity-search-with-score)
- [Vectara as a Retriever](#vectara-as-a-retriever)
- [Using Vectara as a SelfQuery Retriever](#using-vectara-as-a-selfquery-retriever)

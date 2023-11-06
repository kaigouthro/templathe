# Zep

Zep is an open-source long-term memory store for LLM applications. Zep makes it easy to add relevant documents,
chat history memory & rich user data to your LLM app's prompts.

**Note:** The `ZepVectorStore` works with `Documents` and is intended to be used as a `Retriever`.
It offers separate functionality to Zep's `ZepMemory` class, which is designed for persisting, enriching
and searching your user's chat history.

## Why Zep's VectorStore? 🤖🚀[​](#why-zeps-vectorstore- "Direct link to Why Zep's VectorStore? 🤖🚀")

Zep automatically embeds documents added to the Zep Vector Store using low-latency models local to the Zep server.
The Zep client also offers async interfaces for all document operations. These two together with Zep's chat memory
functionality make Zep ideal for building conversational LLM apps where latency and performance are important.

## Installation[​](#installation "Direct link to Installation")

Follow the [Zep Quickstart Guide](https://docs.getzep.com/deployment/quickstart/) to install and get started with Zep.

## Usage[​](#usage "Direct link to Usage")

You'll need your Zep API URL and optionally an API key to use the Zep VectorStore.
See the [Zep docs](https://docs.getzep.com) for more information.

In the examples below, we're using Zep's auto-embedding feature which automatically embed documents on the Zep server
using low-latency embedding models.

## Note[​](#note "Direct link to Note")

- These examples use Zep's async interfaces. Call sync interfaces by removing the `a` prefix from the method names.
- If you pass in an `Embeddings` instance Zep will use this to embed documents rather than auto-embed them.
  You must also set your document collection to `isAutoEmbedded === false`.
- If you set your collection to `isAutoEmbedded === false`, you must pass in an `Embeddings` instance.

## Load or create a Collection from documents[​](#load-or-create-a-collection-from-documents "Direct link to Load or create a Collection from documents")

```python
from uuid import uuid4  
  
from langchain.document\_loaders import WebBaseLoader  
from langchain.text\_splitter import RecursiveCharacterTextSplitter  
from langchain.vectorstores import ZepVectorStore  
from langchain.vectorstores.zep import CollectionConfig  
  
ZEP\_API\_URL = "http://localhost:8000" # this is the API url of your Zep instance  
ZEP\_API\_KEY = "<optional\_key>" # optional API Key for your Zep instance  
collection\_name = f"babbage{uuid4().hex}" # a unique collection name. alphanum only  
  
# Collection config is needed if we're creating a new Zep Collection  
config = CollectionConfig(  
 name=collection\_name,  
 description="<optional description>",  
 metadata={"optional\_metadata": "associated with the collection"},  
 is\_auto\_embedded=True, # we'll have Zep embed our documents using its low-latency embedder  
 embedding\_dimensions=1536 # this should match the model you've configured Zep to use.  
)  
  
# load the document  
article\_url = "https://www.gutenberg.org/cache/epub/71292/pg71292.txt"  
loader = WebBaseLoader(article\_url)  
documents = loader.load()  
  
# split it into chunks  
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=500, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
# Instantiate the VectorStore. Since the collection does not already exist in Zep,  
# it will be created and populated with the documents we pass in.  
vs = ZepVectorStore.from\_documents(docs,  
 collection\_name=collection\_name,  
 config=config,  
 api\_url=ZEP\_API\_URL,  
 api\_key=ZEP\_API\_KEY  
 )  

```

```python
# wait for the collection embedding to complete  
  
async def wait\_for\_ready(collection\_name: str) -> None:  
 from zep\_python import ZepClient  
 import time  
  
 client = ZepClient(ZEP\_API\_URL, ZEP\_API\_KEY)  
  
 while True:  
 c = await client.document.aget\_collection(collection\_name)  
 print(  
 "Embedding status: "  
 f"{c.document\_embedded\_count}/{c.document\_count} documents embedded"  
 )  
 time.sleep(1)  
 if c.status == "ready":  
 break  
  
  
await wait\_for\_ready(collection\_name)  

```

```text
 Embedding status: 0/402 documents embedded  
 Embedding status: 0/402 documents embedded  
 Embedding status: 402/402 documents embedded  

```

## Simarility Search Query over the Collection[​](#simarility-search-query-over-the-collection "Direct link to Simarility Search Query over the Collection")

```python
# query it  
query = "what is the structure of our solar system?"  
docs\_scores = await vs.asimilarity\_search\_with\_relevance\_scores(query, k=3)  
  
# print results  
for d, s in docs\_scores:  
 print(d.page\_content, " -> ", s, "\n====\n")  

```

```text
 Tables necessary to determine the places of the planets are not less  
 necessary than those for the sun, moon, and stars. Some notion of the  
 number and complexity of these tables may be formed, when we state that  
 the positions of the two principal planets, (and these are the most  
 necessary for the navigator,) Jupiter and Saturn, require each not less  
 than one hundred and sixteen tables. Yet it is not only necessary to  
 predict the position of these bodies, but it is likewise expedient to -> 0.8998482592744614   
 ====  
   
 tabulate the motions of the four satellites of Jupiter, to predict the  
 exact times at which they enter his shadow, and at which their shadows  
 cross his disc, as well as the times at which they are interposed  
 between him and the Earth, and he between them and the Earth.  
   
 Among the extensive classes of tables here enumerated, there are several  
 which are in their nature permanent and unalterable, and would never  
 require to be recomputed, if they could once be computed with perfect -> 0.8976143854195493   
 ====  
   
 the scheme of notation thus applied, immediately suggested the  
 advantages which must attend it as an instrument for expressing the  
 structure, operation, and circulation of the animal system; and we  
 entertain no doubt of its adequacy for that purpose. Not only the  
 mechanical connexion of the solid members of the bodies of men and  
 animals, but likewise the structure and operation of the softer parts,  
 including the muscles, integuments, membranes, &c. the nature, motion, -> 0.889982614061763   
 ====  

```

## Search over Collection Re-ranked by MMR[​](#search-over-collection-re-ranked-by-mmr "Direct link to Search over Collection Re-ranked by MMR")

```python
query = "what is the structure of our solar system?"  
docs = await vs.asearch(query, search\_type="mmr", k=3)  
  
for d in docs:  
 print(d.page\_content, "\n====\n")  

```

```text
 Tables necessary to determine the places of the planets are not less  
 necessary than those for the sun, moon, and stars. Some notion of the  
 number and complexity of these tables may be formed, when we state that  
 the positions of the two principal planets, (and these the most  
 necessary for the navigator,) Jupiter and Saturn, require each not less  
 than one hundred and sixteen tables. Yet it is not only necessary to  
 predict the position of these bodies, but it is likewise expedient to   
 ====  
   
 the scheme of notation thus applied, immediately suggested the  
 advantages which must attend it as an instrument for expressing the  
 structure, operation, and circulation of the animal system; and we  
 entertain no doubt of its adequacy for that purpose. Not only the  
 mechanical connexion of the solid members of the bodies of men and  
 animals, but likewise the structure and operation of the softer parts,  
 including the muscles, integuments, membranes, &c. the nature, motion,   
 ====  
   
 tabulate the motions of the four satellites of Jupiter, to predict the  
 exact times at which they enter his shadow, and at which their shadows  
 cross his disc, as well as the times at which they are interposed  
 between him and the Earth, and he between them and the Earth.  
   
 Among the extensive classes of tables here enumerated, there are several  
 which are in their nature permanent and unalterable, and would never  
 require to be recomputed, if they could once be computed with perfect   
 ====  

```

# Filter by Metadata

Use a metadata filter to narrow down results. First, load another book: "Adventures of Sherlock Holmes"

```python
# Let's add more content to the existing Collection  
article\_url = "https://www.gutenberg.org/files/48320/48320-0.txt"  
loader = WebBaseLoader(article\_url)  
documents = loader.load()  
  
# split it into chunks  
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=500, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
await vs.aadd\_documents(docs)  
  
await wait\_for\_ready(collection\_name)  

```

```text
 Embedding status: 402/1692 documents embedded  
 Embedding status: 402/1692 documents embedded  
 Embedding status: 552/1692 documents embedded  
 Embedding status: 702/1692 documents embedded  
 Embedding status: 1002/1692 documents embedded  
 Embedding status: 1002/1692 documents embedded  
 Embedding status: 1152/1692 documents embedded  
 Embedding status: 1302/1692 documents embedded  
 Embedding status: 1452/1692 documents embedded  
 Embedding status: 1602/1692 documents embedded  
 Embedding status: 1692/1692 documents embedded  

```

### We see results from both books. Note the `source` metadata[​](#we-see-results-from-both-books-note-the-source-metadata "Direct link to we-see-results-from-both-books-note-the-source-metadata")

```python
query = "Was he interested in astronomy?"  
docs = await vs.asearch(query, search\_type="similarity", k=3)  
  
for d in docs:  
 print(d.page\_content, " -> ", d.metadata, "\n====\n")  

```

```text
 by that body to Mr Babbage:--'In no department of science, or of the  
 arts, does this discovery promise to be so eminently useful as in that  
 of astronomy, and its kindred sciences, with the various arts dependent  
 on them. In none are computations more operose than those which  
 astronomy in particular requires;--in none are preparatory facilities  
 more needful;--in none is error more detrimental. The practical  
 astronomer is interrupted in his pursuit, and diverted from his task of -> {'source': 'https://www.gutenberg.org/cache/epub/71292/pg71292.txt'}   
 ====  
   
 possess all knowledge which is likely to be useful to him in his work,  
 and this I have endeavored in my case to do. If I remember rightly, you  
 on one occasion, in the early days of our friendship, defined my limits  
 in a very precise fashion.”  
   
 “Yes,” I answered, laughing. “It was a singular document. Philosophy,  
 astronomy, and politics were marked at zero, I remember. Botany  
 variable, geology profound as regards the mud-stains from any region -> {'source': 'https://www.gutenberg.org/files/48320/48320-0.txt'}   
 ====  
   
 in all its relations; but above all, with Astronomy and Navigation. So  
 important have they been considered, that in many instances large sums  
 have been appropriated by the most enlightened nations in the production  
 of them; and yet so numerous and insurmountable have been the  
 difficulties attending the attainment of this end, that after all, even  
 navigators, putting aside every other department of art and science,  
 have, until very recently, been scantily and imperfectly supplied with -> {'source': 'https://www.gutenberg.org/cache/epub/71292/pg71292.txt'}   
 ====  

```

### Let's try again using a filter for only the Sherlock Holmes document.[​](#lets-try-again-using-a-filter-for-only-the-sherlock-holmes-document "Direct link to Let's try again using a filter for only the Sherlock Holmes document.")

```python
filter = {  
 "where": {"jsonpath": "$[\*] ? (@.source == 'https://www.gutenberg.org/files/48320/48320-0.txt')"},  
}  
  
docs = await vs.asearch(query, search\_type="similarity", metadata=filter, k=3)  
  
for d in docs:  
 print(d.page\_content, " -> ", d.metadata, "\n====\n")  

```

```text
 possess all knowledge which is likely to be useful to him in his work,  
 and this I have endeavored in my case to do. If I remember rightly, you  
 on one occasion, in the early days of our friendship, defined my limits  
 in a very precise fashion.”  
   
 “Yes,” I answered, laughing. “It was a singular document. Philosophy,  
 astronomy, and politics were marked at zero, I remember. Botany  
 variable, geology profound as regards the mud-stains from any region -> {'source': 'https://www.gutenberg.org/files/48320/48320-0.txt'}   
 ====  
   
 the light shining upon his strong-set aquiline features. So he sat as I  
 dropped off to sleep, and so he sat when a sudden ejaculation caused me  
 to wake up, and I found the summer sun shining into the apartment. The  
 pipe was still between his lips, the smoke still curled upward, and the  
 room was full of a dense tobacco haze, but nothing remained of the heap  
 of shag which I had seen upon the previous night.  
   
 “Awake, Watson?” he asked.  
   
 “Yes.”  
   
 “Game for a morning drive?” -> {'source': 'https://www.gutenberg.org/files/48320/48320-0.txt'}   
 ====  
   
 “I glanced at the books upon the table, and in spite of my ignorance  
 of German I could see that two of them were treatises on science, the  
 others being volumes of poetry. Then I walked across to the window,  
 hoping that I might catch some glimpse of the country-side, but an oak  
 shutter, heavily barred, was folded across it. It was a wonderfully  
 silent house. There was an old clock ticking loudly somewhere in the  
 passage, but otherwise everything was deadly still. A vague feeling of -> {'source': 'https://www.gutenberg.org/files/48320/48320-0.txt'}   
 ====  

```

- [Why Zep's VectorStore? 🤖🚀](#why-zeps-vectorstore-)

- [Installation](#installation)

- [Usage](#usage)

- [Note](#note)

- [Load or create a Collection from documents](#load-or-create-a-collection-from-documents)

- [Simarility Search Query over the Collection](#simarility-search-query-over-the-collection)

- [Search over Collection Re-ranked by MMR](#search-over-collection-re-ranked-by-mmr)

  - [We see results from both books. Note the `source` metadata](#we-see-results-from-both-books-note-the-source-metadata)
  - [Let's try again using a filter for only the Sherlock Holmes document.](#lets-try-again-using-a-filter-for-only-the-sherlock-holmes-document)

- [We see results from both books. Note the `source` metadata](#we-see-results-from-both-books-note-the-source-metadata)

- [Let's try again using a filter for only the Sherlock Holmes document.](#lets-try-again-using-a-filter-for-only-the-sherlock-holmes-document)

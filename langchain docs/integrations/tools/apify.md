# Apify

This notebook shows how to use the [Apify integration](/docs/ecosystem/integrations/apify.html) for LangChain.

[Apify](https://apify.com) is a cloud platform for web scraping and data extraction,
which provides an [ecosystem](https://apify.com/store) of more than a thousand
ready-made apps called *Actors* for various web scraping, crawling, and data extraction use cases.
For example, you can use it to extract Google Search results, Instagram and Facebook profiles, products from Amazon or Shopify, Google Maps reviews, etc. etc.

In this example, we'll use the [Website Content Crawler](https://apify.com/apify/website-content-crawler) Actor,
which can deeply crawl websites such as documentation, knowledge bases, help centers, or blogs,
and extract text content from the web pages. Then we feed the documents into a vector index and answer questions from it.

```python
#!pip install apify-client openai langchain chromadb tiktoken  

```

First, import `ApifyWrapper` into your source code:

```python
from langchain.document\_loaders.base import Document  
from langchain.indexes import VectorstoreIndexCreator  
from langchain.utilities import ApifyWrapper  

```

Initialize it using your [Apify API token](https://console.apify.com/account/integrations) and for the purpose of this example, also with your OpenAI API key:

```python
import os  
  
os.environ["OPENAI\_API\_KEY"] = "Your OpenAI API key"  
os.environ["APIFY\_API\_TOKEN"] = "Your Apify API token"  
  
apify = ApifyWrapper()  

```

Then run the Actor, wait for it to finish, and fetch its results from the Apify dataset into a LangChain document loader.

Note that if you already have some results in an Apify dataset, you can load them directly using `ApifyDatasetLoader`, as shown in [this notebook](/docs/integrations/document_loaders/apify_dataset.html). In that notebook, you'll also find the explanation of the `dataset_mapping_function`, which is used to map fields from the Apify dataset records to LangChain `Document` fields.

```python
loader = apify.call\_actor(  
 actor\_id="apify/website-content-crawler",  
 run\_input={"startUrls": [{"url": "https://python.langchain.com/en/latest/"}]},  
 dataset\_mapping\_function=lambda item: Document(  
 page\_content=item["text"] or "", metadata={"source": item["url"]}  
 ),  
)  

```

Initialize the vector index from the crawled documents:

```python
index = VectorstoreIndexCreator().from\_loaders([loader])  

```

And finally, query the vector index:

```python
query = "What is LangChain?"  
result = index.query\_with\_sources(query)  

```

```python
print(result["answer"])  
print(result["sources"])  

```

```text
 LangChain is a standard interface through which you can interact with a variety of large language models (LLMs). It provides modules that can be used to build language model applications, and it also provides chains and agents with memory capabilities.  
   
 https://python.langchain.com/en/latest/modules/models/llms.html, https://python.langchain.com/en/latest/getting\_started/getting\_started.html  

```

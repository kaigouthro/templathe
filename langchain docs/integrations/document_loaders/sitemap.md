# Sitemap

Extends from the `WebBaseLoader`, `SitemapLoader` loads a sitemap from a given URL, and then scrape and load all pages in the sitemap, returning each page as a Document.

The scraping is done concurrently. There are reasonable limits to concurrent requests, defaulting to 2 per second. If you aren't concerned about being a good citizen, or you control the scrapped server, or don't care about load. Note, while this will speed up the scraping process, but it may cause the server to block you. Be careful!

```bash
pip install nest\_asyncio  

```

```text
 Requirement already satisfied: nest\_asyncio in /Users/tasp/Code/projects/langchain/.venv/lib/python3.10/site-packages (1.5.6)  
   
 [notice] A new release of pip available: 22.3.1 -> 23.0.1  
 [notice] To update, run: pip install --upgrade pip  

```

```python
# fixes a bug with asyncio and jupyter  
import nest\_asyncio  
  
nest\_asyncio.apply()  

```

```python
from langchain.document\_loaders.sitemap import SitemapLoader  

```

```python
sitemap\_loader = SitemapLoader(web\_path="https://langchain.readthedocs.io/sitemap.xml")  
  
docs = sitemap\_loader.load()  

```

You can change the `requests_per_second` parameter to increase the max concurrent requests. and use `requests_kwargs` to pass kwargs when send requests.

```python
sitemap\_loader.requests\_per\_second = 2  
# Optional: avoid `[SSL: CERTIFICATE\_VERIFY\_FAILED]` issue  
sitemap\_loader.requests\_kwargs = {"verify": False}  

```

```python
docs[0]  

```

```text
 Document(page\_content='\n\n\n\n\n\n\n\n\n\nLangChain Python API Reference Documentation.\n\n\n\n\n\n\n\n\n\nYou will be automatically redirected to the new location of this page.\n\n', metadata={'source': 'https://api.python.langchain.com/en/stable/', 'loc': 'https://api.python.langchain.com/en/stable/', 'lastmod': '2023-10-13T18:13:26.966937+00:00', 'changefreq': 'weekly', 'priority': '1'})  

```

## Filtering sitemap URLs[​](#filtering-sitemap-urls "Direct link to Filtering sitemap URLs")

Sitemaps can be massive files, with thousands of URLs. Often you don't need every single one of them. You can filter the URLs by passing a list of strings or regex patterns to the `filter_urls` parameter. Only URLs that match one of the patterns will be loaded.

```python
loader = SitemapLoader(  
 web\_path="https://langchain.readthedocs.io/sitemap.xml",  
 filter\_urls=["https://api.python.langchain.com/en/latest"],  
)  
documents = loader.load()  

```

```text
 Fetching pages: 100%|##########| 1/1 [00:00<00:00, 16.39it/s]  

```

```python
documents[0]  

```

```text
 Document(page\_content='\n\n\n\n\n\n\n\n\n\nLangChain Python API Reference Documentation.\n\n\n\n\n\n\n\n\n\nYou will be automatically redirected to the new location of this page.\n\n', metadata={'source': 'https://api.python.langchain.com/en/latest/', 'loc': 'https://api.python.langchain.com/en/latest/', 'lastmod': '2023-10-13T18:09:58.478681+00:00', 'changefreq': 'daily', 'priority': '0.9'})  

```

## Add custom scraping rules[​](#add-custom-scraping-rules "Direct link to Add custom scraping rules")

The `SitemapLoader` uses `beautifulsoup4` for the scraping process, and it scrapes every element on the page by default. The `SitemapLoader` constructor accepts a custom scraping function. This feature can be helpful to tailor the scraping process to your specific needs; for example, you might want to avoid scraping headers or navigation elements.

The following example shows how to develop and use a custom function to avoid navigation and header elements.

Import the `beautifulsoup4` library and define the custom function.

```python
pip install beautifulsoup4  

```

```python
from bs4 import BeautifulSoup  
  
  
def remove\_nav\_and\_header\_elements(content: BeautifulSoup) -> str:  
 # Find all 'nav' and 'header' elements in the BeautifulSoup object  
 nav\_elements = content.find\_all("nav")  
 header\_elements = content.find\_all("header")  
  
 # Remove each 'nav' and 'header' element from the BeautifulSoup object  
 for element in nav\_elements + header\_elements:  
 element.decompose()  
  
 return str(content.get\_text())  

```

Add your custom function to the `SitemapLoader` object.

```python
loader = SitemapLoader(  
 "https://langchain.readthedocs.io/sitemap.xml",  
 filter\_urls=["https://api.python.langchain.com/en/latest/"],  
 parsing\_function=remove\_nav\_and\_header\_elements,  
)  

```

## Local Sitemap[​](#local-sitemap "Direct link to Local Sitemap")

The sitemap loader can also be used to load local files.

```python
sitemap\_loader = SitemapLoader(web\_path="example\_data/sitemap.xml", is\_local=True)  
  
docs = sitemap\_loader.load()  

```

```text
 Fetching pages: 100%|##########| 3/3 [00:00<00:00, 12.46it/s]  

```

- [Filtering sitemap URLs](#filtering-sitemap-urls)
- [Add custom scraping rules](#add-custom-scraping-rules)
- [Local Sitemap](#local-sitemap)

# Tavily Search API

[Tavily's Search API](https://tavily.com) is a search engine built specifically for AI agents (LLMs), delivering real-time, accurate, and factual results at speed.

## Usage[​](#usage "Direct link to Usage")

For a full list of allowed arguments, see [the official documentation](https://app.tavily.com/documentation/python). You can also pass any param to the SDK via a `kwargs` dictionary.

```python
# %pip install tavily-python  

```

```python
import os  
from langchain.retrievers.tavily\_search\_api import TavilySearchAPIRetriever  
  
os.environ["TAVILY\_API\_KEY"] = "YOUR\_API\_KEY"  
  
retriever = TavilySearchAPIRetriever(k=4)  
  
retriever.invoke("what year was breath of the wild released?")  

```

```text
 [Document(page\_content='Nintendo Designer (s) Hidemaro Fujibayashi (director) Eiji Aonuma (producer/group manager) Release date (s) United States of America: • March 3, 2017 Japan: • March 3, 2017 Australia / New Zealand: • March 2, 2017 Belgium: • March 3, 2017 Hong Kong: • Feburary 1, 2018 South Korea: • February 1, 2018 The UK / Ireland: • March 3, 2017 Content ratings', metadata={'title': 'The Legend of Zelda: Breath of the Wild - Zelda Wiki', 'source': 'https://zelda.fandom.com/wiki/The\_Legend\_of\_Zelda:\_Breath\_of\_the\_Wild', 'score': 0.96994, 'images': None}),  
 Document(page\_content='02/01/23 Nintendo Switch Online member exclusive: Save on two digital games Read more 09/13/22 Out of the Shadows … the Legend of Zelda: Tears of the Kingdom Launches for Nintendo Switch on May...', metadata={'title': 'The Legend of Zelda™: Breath of the Wild - Nintendo', 'source': 'https://www.nintendo.com/store/products/the-legend-of-zelda-breath-of-the-wild-switch/', 'score': 0.94346, 'images': None}),  
 Document(page\_content='Now we finally have a concrete release date of May 12, 2023. The date was announced alongside this brief (and mysterious) new trailer that also confirmed its title: The Legend of Zelda: Tears...', metadata={'title': 'The Legend of Zelda: Tears of the Kingdom: Release Date, Gameplay ... - IGN', 'source': 'https://www.ign.com/articles/the-legend-of-zelda-breath-of-the-wild-2-release-date-gameplay-news-rumors', 'score': 0.94145, 'images': None}),  
 Document(page\_content='It was eventually released on March 3, 2017, as a launch game for the Switch and the final Nintendo game for the Wii U. It received widespread acclaim and won numerous Game of the Year accolades. Critics praised its open-ended gameplay, open-world design, and attention to detail, though some criticized its technical performance.', metadata={'title': 'The Legend of Zelda: Breath of the Wild - Wikipedia', 'source': 'https://en.wikipedia.org/wiki/The\_Legend\_of\_Zelda:\_Breath\_of\_the\_Wild', 'score': 0.92102, 'images': None})]  

```

- [Usage](#usage)

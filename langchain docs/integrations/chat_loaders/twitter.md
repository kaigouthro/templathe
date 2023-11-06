# Twitter (via Apify)

This notebook shows how to load chat messages from Twitter to fine-tune on. We do this by utilizing Apify.

First, use Apify to export tweets. An example

```python
import json  
from langchain.schema import AIMessage  
from langchain.adapters.openai import convert\_message\_to\_dict  

```

```python
with open('example\_data/dataset\_twitter-scraper\_2023-08-23\_22-13-19-740.json') as f:  
 data = json.load(f)  

```

```python
# Filter out tweets that reference other tweets, because it's a bit weird  
tweets = [d["full\_text"] for d in data if "t.co" not in d['full\_text']]  
# Create them as AI messages  
messages = [AIMessage(content=t) for t in tweets]  
# Add in a system message at the start  
# TODO: we could try to extract the subject from the tweets, and put that in the system message.  
system\_message = {"role": "system", "content": "write a tweet"}  
data = [[system\_message, convert\_message\_to\_dict(m)] for m in messages]  

```

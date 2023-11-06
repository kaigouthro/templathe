# LarkSuite (FeiShu)

[LarkSuite](https://www.larksuite.com/) is an enterprise collaboration platform developed by ByteDance.

This notebook covers how to load data from the `LarkSuite` REST API into a format that can be ingested into LangChain, along with example usage for text summarization.

The LarkSuite API requires an access token (tenant_access_token or user_access_token), checkout [LarkSuite open platform document](https://open.larksuite.com/document) for API details.

```python
from getpass import getpass  
from langchain.document\_loaders.larksuite import LarkSuiteDocLoader  
  
DOMAIN = input("larksuite domain")  
ACCESS\_TOKEN = getpass("larksuite tenant\_access\_token or user\_access\_token")  
DOCUMENT\_ID = input("larksuite document id")  

```

```python
from pprint import pprint  
  
larksuite\_loader = LarkSuiteDocLoader(DOMAIN, ACCESS\_TOKEN, DOCUMENT\_ID)  
docs = larksuite\_loader.load()  
  
pprint(docs)  

```

```text
 [Document(page\_content='Test Doc\nThis is a Test Doc\n\n1\n2\n3\n\n', metadata={'document\_id': 'V76kdbd2HoBbYJxdiNNccajunPf', 'revision\_id': 11, 'title': 'Test Doc'})]  

```

```python
# see https://python.langchain.com/docs/use\_cases/summarization for more details  
from langchain.chains.summarize import load\_summarize\_chain  
  
chain = load\_summarize\_chain(llm, chain\_type="map\_reduce")  
chain.run(docs)  

```

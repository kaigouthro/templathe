# Airbyte Question Answering

This notebook shows how to do question answering over structured data, in this case using the `AirbyteStripeLoader`.

Vectorstores often have a hard time answering questions that requires computing, grouping and filtering structured data so the high level idea is to use a `pandas` dataframe to help with these types of questions.

1. Load data from Stripe using Airbyte. user the `record_handler` paramater to return a JSON from the data loader.

```python
import os  
import pandas as pd  
  
from langchain.document\_loaders.airbyte import AirbyteStripeLoader  
from langchain.chat\_models.openai import ChatOpenAI  
from langchain.agents import AgentType, create\_pandas\_dataframe\_agent  
  
stream\_name = "customers"  
config = {  
 "client\_secret": os.getenv("STRIPE\_CLIENT\_SECRET"),  
 "account\_id": os.getenv("STRIPE\_ACCOUNT\_D"),  
 "start\_date": "2023-01-20T00:00:00Z",  
}  
  
def handle\_record(record: dict, \_id: str):  
 return record.data  
  
loader = AirbyteStripeLoader(  
 config=config,  
 record\_handler=handle\_record,  
 stream\_name=stream\_name,  
)  
data = loader.load()  

```

2. Pass the data to `pandas` dataframe.

```python
df = pd.DataFrame(data)  

```

3. Pass the dataframe `df` to the `create_pandas_dataframe_agent` and invoke

```python
agent = create\_pandas\_dataframe\_agent(  
 ChatOpenAI(temperature=0, model="gpt-4"),  
 df,  
 verbose=True,  
 agent\_type=AgentType.OPENAI\_FUNCTIONS,  
)  

```

4. Run the agent

```python
output = agent.run("How many rows are there?")  

```

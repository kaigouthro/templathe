# PowerBI Dataset

This notebook showcases an agent interacting with a `Power BI Dataset`. The agent is answering more general questions about a dataset, as well as recover from errors.

Note that, as this agent is in active development, all answers might not be correct. It runs against the [executequery endpoint](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries), which does not allow deletes.

### Notes:[​](#notes "Direct link to Notes:")

- It relies on authentication with the azure.identity package, which can be installed with `pip install azure-identity`. Alternatively you can create the powerbi dataset with a token as a string without supplying the credentials.
- You can also supply a username to impersonate for use with datasets that have RLS enabled.
- The toolkit uses a LLM to create the query from the question, the agent uses the LLM for the overall execution.
- Testing was done mostly with a `text-davinci-003` model, codex models did not seem to perform ver well.

## Initialization[​](#initialization "Direct link to Initialization")

```python
from langchain.agents.agent\_toolkits import create\_pbi\_agent  
from langchain.agents.agent\_toolkits import PowerBIToolkit  
from langchain.utilities.powerbi import PowerBIDataset  
from langchain.chat\_models import ChatOpenAI  
from langchain.agents import AgentExecutor  
from azure.identity import DefaultAzureCredential  

```

```python
fast\_llm = ChatOpenAI(  
 temperature=0.5, max\_tokens=1000, model\_name="gpt-3.5-turbo", verbose=True  
)  
smart\_llm = ChatOpenAI(temperature=0, max\_tokens=100, model\_name="gpt-4", verbose=True)  
  
toolkit = PowerBIToolkit(  
 powerbi=PowerBIDataset(  
 dataset\_id="<dataset\_id>",  
 table\_names=["table1", "table2"],  
 credential=DefaultAzureCredential(),  
 ),  
 llm=smart\_llm,  
)  
  
agent\_executor = create\_pbi\_agent(  
 llm=fast\_llm,  
 toolkit=toolkit,  
 verbose=True,  
)  

```

## Example: describing a table[​](#example-describing-a-table "Direct link to Example: describing a table")

```python
agent\_executor.run("Describe table1")  

```

## Example: simple query on a table[​](#example-simple-query-on-a-table "Direct link to Example: simple query on a table")

In this example, the agent actually figures out the correct query to get a row count of the table.

```python
agent\_executor.run("How many records are in table1?")  

```

## Example: running queries[​](#example-running-queries "Direct link to Example: running queries")

```python
agent\_executor.run("How many records are there by dimension1 in table2?")  

```

```python
agent\_executor.run("What unique values are there for dimensions2 in table2")  

```

## Example: add your own few-shot prompts[​](#example-add-your-own-few-shot-prompts "Direct link to Example: add your own few-shot prompts")

```python
# fictional example  
few\_shots = """  
Question: How many rows are in the table revenue?  
DAX: EVALUATE ROW("Number of rows", COUNTROWS(revenue\_details))  
----  
Question: How many rows are in the table revenue where year is not empty?  
DAX: EVALUATE ROW("Number of rows", COUNTROWS(FILTER(revenue\_details, revenue\_details[year] <> "")))  
----  
Question: What was the average of value in revenue in dollars?  
DAX: EVALUATE ROW("Average", AVERAGE(revenue\_details[dollar\_value]))  
----  
"""  
toolkit = PowerBIToolkit(  
 powerbi=PowerBIDataset(  
 dataset\_id="<dataset\_id>",  
 table\_names=["table1", "table2"],  
 credential=DefaultAzureCredential(),  
 ),  
 llm=smart\_llm,  
 examples=few\_shots,  
)  
agent\_executor = create\_pbi\_agent(  
 llm=fast\_llm,  
 toolkit=toolkit,  
 verbose=True,  
)  

```

```python
agent\_executor.run("What was the maximum of value in revenue in dollars in 2022?")  

```

- [Notes:](#notes)
- [Initialization](#initialization)
- [Example: describing a table](#example-describing-a-table)
- [Example: simple query on a table](#example-simple-query-on-a-table)
- [Example: running queries](#example-running-queries)
- [Example: add your own few-shot prompts](#example-add-your-own-few-shot-prompts)

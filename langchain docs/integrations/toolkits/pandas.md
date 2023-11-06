# Pandas Dataframe

This notebook shows how to use agents to interact with a `Pandas DataFrame`. It is mostly optimized for question answering.

**NOTE: this agent calls the `Python` agent under the hood, which executes LLM generated Python code - this can be bad if the LLM generated Python code is harmful. Use cautiously.**

```python
from langchain.agents import create\_pandas\_dataframe\_agent  
from langchain.chat\_models import ChatOpenAI  
from langchain.agents.agent\_types import AgentType  

```

```python
from langchain.llms import OpenAI  
import pandas as pd  
  
df = pd.read\_csv("titanic.csv")  

```

## Using `ZERO_SHOT_REACT_DESCRIPTION`[​](#using-zero_shot_react_description "Direct link to using-zero_shot_react_description")

This shows how to initialize the agent using the `ZERO_SHOT_REACT_DESCRIPTION` agent type. Note that this is an alternative to the above.

```python
agent = create\_pandas\_dataframe\_agent(OpenAI(temperature=0), df, verbose=True)  

```

## Using OpenAI Functions[​](#using-openai-functions "Direct link to Using OpenAI Functions")

This shows how to initialize the agent using the OPENAI_FUNCTIONS agent type. Note that this is an alternative to the above.

```python
agent = create\_pandas\_dataframe\_agent(  
 ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),  
 df,  
 verbose=True,  
 agent\_type=AgentType.OPENAI\_FUNCTIONS,  
)  

```

```python
agent.run("how many rows are there?")  

```

```text
   
   
 > Entering new chain...  
   
 Invoking: `python\_repl\_ast` with `df.shape[0]`  
   
   
 891There are 891 rows in the dataframe.  
   
 > Finished chain.  
  
  
  
  
  
 'There are 891 rows in the dataframe.'  

```

```python
agent.run("how many people have more than 3 siblings")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Thought: I need to count the number of people with more than 3 siblings  
 Action: python\_repl\_ast  
 Action Input: df[df['SibSp'] > 3].shape[0]  
 Observation: 30  
 Thought: I now know the final answer  
 Final Answer: 30 people have more than 3 siblings.  
   
 > Finished chain.  
  
  
  
  
  
 '30 people have more than 3 siblings.'  

```

```python
agent.run("whats the square root of the average age?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Thought: I need to calculate the average age first  
 Action: python\_repl\_ast  
 Action Input: df['Age'].mean()  
 Observation: 29.69911764705882  
 Thought: I now need to calculate the square root of the average age  
 Action: python\_repl\_ast  
 Action Input: math.sqrt(df['Age'].mean())  
 Observation: NameError("name 'math' is not defined")  
 Thought: I need to import the math library  
 Action: python\_repl\_ast  
 Action Input: import math  
 Observation:   
 Thought: I now need to calculate the square root of the average age  
 Action: python\_repl\_ast  
 Action Input: math.sqrt(df['Age'].mean())  
 Observation: 5.449689683556195  
 Thought: I now know the final answer  
 Final Answer: The square root of the average age is 5.449689683556195.  
   
 > Finished chain.  
  
  
  
  
  
 'The square root of the average age is 5.449689683556195.'  

```

## Multi DataFrame Example[​](#multi-dataframe-example "Direct link to Multi DataFrame Example")

This next part shows how the agent can interact with multiple dataframes passed in as a list.

```python
df1 = df.copy()  
df1["Age"] = df1["Age"].fillna(df1["Age"].mean())  

```

```python
agent = create\_pandas\_dataframe\_agent(OpenAI(temperature=0), [df, df1], verbose=True)  
agent.run("how many rows in the age column are different?")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Thought: I need to compare the age columns in both dataframes  
 Action: python\_repl\_ast  
 Action Input: len(df1[df1['Age'] != df2['Age']])  
 Observation: 177  
 Thought: I now know the final answer  
 Final Answer: 177 rows in the age column are different.  
   
 > Finished chain.  
  
  
  
  
  
 '177 rows in the age column are different.'  

```

- [Using `ZERO_SHOT_REACT_DESCRIPTION`](#using-zero_shot_react_description)
- [Using OpenAI Functions](#using-openai-functions)
- [Multi DataFrame Example](#multi-dataframe-example)

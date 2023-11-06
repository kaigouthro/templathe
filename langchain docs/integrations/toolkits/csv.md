# CSV

This notebook shows how to use agents to interact with data in `CSV` format. It is mostly optimized for question answering.

**NOTE: this agent calls the Pandas DataFrame agent under the hood, which in turn calls the Python agent, which executes LLM generated Python code - this can be bad if the LLM generated Python code is harmful. Use cautiously.**

```python
from langchain.llms import OpenAI  
from langchain.chat\_models import ChatOpenAI  
from langchain.agents.agent\_types import AgentType  
  
from langchain.agents import create\_csv\_agent  

```

## Using `ZERO_SHOT_REACT_DESCRIPTION`[​](#using-zero_shot_react_description "Direct link to using-zero_shot_react_description")

This shows how to initialize the agent using the `ZERO_SHOT_REACT_DESCRIPTION` agent type. Note that this is an alternative to the above.

```python
agent = create\_csv\_agent(  
 OpenAI(temperature=0),  
 "titanic.csv",  
 verbose=True,  
 agent\_type=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,  
)  

```

## Using OpenAI Functions[​](#using-openai-functions "Direct link to Using OpenAI Functions")

This shows how to initialize the agent using the OPENAI_FUNCTIONS agent type. Note that this is an alternative to the above.

```python
agent = create\_csv\_agent(  
 ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),  
 "titanic.csv",  
 verbose=True,  
 agent\_type=AgentType.OPENAI\_FUNCTIONS,  
)  

```

```python
agent.run("how many rows are there?")  

```

```text
 Error in on\_chain\_start callback: 'name'  
  
  
   
 Invoking: `python\_repl\_ast` with `df.shape[0]`  
   
   
 891There are 891 rows in the dataframe.  
   
 > Finished chain.  
  
  
  
  
  
 'There are 891 rows in the dataframe.'  

```

```python
agent.run("how many people have more than 3 siblings")  

```

```text
 Error in on\_chain\_start callback: 'name'  
  
  
   
 Invoking: `python\_repl\_ast` with `df[df['SibSp'] > 3]['PassengerId'].count()`  
   
   
 30There are 30 people in the dataframe who have more than 3 siblings.  
   
 > Finished chain.  
  
  
  
  
  
 'There are 30 people in the dataframe who have more than 3 siblings.'  

```

```python
agent.run("whats the square root of the average age?")  

```

```text
 Error in on\_chain\_start callback: 'name'  
  
  
   
 Invoking: `python\_repl\_ast` with `import pandas as pd  
 import math  
   
 # Create a dataframe  
 data = {'Age': [22, 38, 26, 35, 35]}  
 df = pd.DataFrame(data)  
   
 # Calculate the average age  
 average\_age = df['Age'].mean()  
   
 # Calculate the square root of the average age  
 square\_root = math.sqrt(average\_age)  
   
 square\_root`  
   
   
 5.585696017507576The square root of the average age is approximately 5.59.  
   
 > Finished chain.  
  
  
  
  
  
 'The square root of the average age is approximately 5.59.'  

```

### Multi CSV Example[​](#multi-csv-example "Direct link to Multi CSV Example")

This next part shows how the agent can interact with multiple csv files passed in as a list.

```python
agent = create\_csv\_agent(  
 ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),  
 ["titanic.csv", "titanic\_age\_fillna.csv"],  
 verbose=True,  
 agent\_type=AgentType.OPENAI\_FUNCTIONS,  
)  
agent.run("how many rows in the age column are different between the two dfs?")  

```

```text
 Error in on\_chain\_start callback: 'name'  
  
  
   
 Invoking: `python\_repl\_ast` with `df1['Age'].nunique() - df2['Age'].nunique()`  
   
   
 -1There is 1 row in the age column that is different between the two dataframes.  
   
 > Finished chain.  
  
  
  
  
  
 'There is 1 row in the age column that is different between the two dataframes.'  

```

- [Using `ZERO_SHOT_REACT_DESCRIPTION`](#using-zero_shot_react_description)

- [Using OpenAI Functions](#using-openai-functions)

  - [Multi CSV Example](#multi-csv-example)

- [Multi CSV Example](#multi-csv-example)

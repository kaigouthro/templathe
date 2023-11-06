# MLflow

[MLflow](https://www.mlflow.org/docs/latest/what-is-mlflow.html) is a versatile, expandable, open-source platform for managing workflows and artifacts across the machine learning lifecycle. It has built-in integrations with many popular ML libraries, but can be used with any library, algorithm, or deployment tool. It is designed to be extensible, so you can write plugins to support new workflows, libraries, and tools.

This notebook goes over how to track your LangChain experiments into your `MLflow Server`

## External examples[​](#external-examples "Direct link to External examples")

`MLflow` provides [several examples](https://github.com/mlflow/mlflow/tree/master/examples/langchain) for the `LangChain` integration:

- [simple_chain](https://github.com/mlflow/mlflow/blob/master/examples/langchain/simple_chain.py)
- [simple_agent](https://github.com/mlflow/mlflow/blob/master/examples/langchain/simple_agent.py)
- [retriever_chain](https://github.com/mlflow/mlflow/blob/master/examples/langchain/retriever_chain.py)
- [retrieval_qa_chain](https://github.com/mlflow/mlflow/blob/master/examples/langchain/retrieval_qa_chain.py)

## Example[​](#example "Direct link to Example")

```bash
pip install azureml-mlflow  
pip install pandas  
pip install textstat  
pip install spacy  
pip install openai  
pip install google-search-results  
python -m spacy download en\_core\_web\_sm  

```

```python
import os  
  
os.environ["MLFLOW\_TRACKING\_URI"] = ""  
os.environ["OPENAI\_API\_KEY"] = ""  
os.environ["SERPAPI\_API\_KEY"] = ""  

```

```python
from langchain.callbacks import MlflowCallbackHandler  
from langchain.llms import OpenAI  

```

```python
"""Main function.  
  
This function is used to try the callback handler.  
Scenarios:  
1. OpenAI LLM  
2. Chain with multiple SubChains on multiple generations  
3. Agent with Tools  
"""  
mlflow\_callback = MlflowCallbackHandler()  
llm = OpenAI(  
 model\_name="gpt-3.5-turbo", temperature=0, callbacks=[mlflow\_callback], verbose=True  
)  

```

```python
# SCENARIO 1 - LLM  
llm\_result = llm.generate(["Tell me a joke"])  
  
mlflow\_callback.flush\_tracker(llm)  

```

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
# SCENARIO 2 - Chain  
template = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.  
Title: {title}  
Playwright: This is a synopsis for the above play:"""  
prompt\_template = PromptTemplate(input\_variables=["title"], template=template)  
synopsis\_chain = LLMChain(llm=llm, prompt=prompt\_template, callbacks=[mlflow\_callback])  
  
test\_prompts = [  
 {  
 "title": "documentary about good video games that push the boundary of game design"  
 },  
]  
synopsis\_chain.apply(test\_prompts)  
mlflow\_callback.flush\_tracker(synopsis\_chain)  

```

```python
from langchain.agents import initialize\_agent, load\_tools  
from langchain.agents import AgentType  

```

```python
# SCENARIO 3 - Agent with Tools  
tools = load\_tools(["serpapi", "llm-math"], llm=llm, callbacks=[mlflow\_callback])  
agent = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,  
 callbacks=[mlflow\_callback],  
 verbose=True,  
)  
agent.run(  
 "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"  
)  
mlflow\_callback.flush\_tracker(agent, finish=True)  

```

- [External examples](#external-examples)
- [Example](#example)

# Jira

This notebook goes over how to use the `Jira` toolkit.

The `Jira` toolkit allows agents to interact with a given Jira instance, performing actions such as searching for issues and creating issues, the tool wraps the atlassian-python-api library, for more see: <https://atlassian-python-api.readthedocs.io/jira.html>

To use this tool, you must first set as environment variables:
JIRA_API_TOKEN
JIRA_USERNAME
JIRA_INSTANCE_URL

```python
%pip install atlassian-python-api  

```

```python
import os  
from langchain.agents import AgentType  
from langchain.agents import initialize\_agent  
from langchain.agents.agent\_toolkits.jira.toolkit import JiraToolkit  
from langchain.llms import OpenAI  
from langchain.utilities.jira import JiraAPIWrapper  

```

```python
os.environ["JIRA\_API\_TOKEN"] = "abc"  
os.environ["JIRA\_USERNAME"] = "123"  
os.environ["JIRA\_INSTANCE\_URL"] = "https://jira.atlassian.com"  
os.environ["OPENAI\_API\_KEY"] = "xyz"  

```

```python
llm = OpenAI(temperature=0)  
jira = JiraAPIWrapper()  
toolkit = JiraToolkit.from\_jira\_api\_wrapper(jira)  
agent = initialize\_agent(  
 toolkit.get\_tools(), llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run("make a new issue in project PW to remind me to make more fried rice")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to create an issue in project PW  
 Action: Create Issue  
 Action Input: {"summary": "Make more fried rice", "description": "Reminder to make more fried rice", "issuetype": {"name": "Task"}, "priority": {"name": "Low"}, "project": {"key": "PW"}}  
 Observation: None  
 Thought: I now know the final answer  
 Final Answer: A new issue has been created in project PW with the summary "Make more fried rice" and description "Reminder to make more fried rice".  
   
 > Finished chain.  
  
  
  
  
  
 'A new issue has been created in project PW with the summary "Make more fried rice" and description "Reminder to make more fried rice".'  

```

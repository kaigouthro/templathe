# MultiOn

This notebook walks you through connecting LangChain to the `MultiOn` Client in your browser

To use this toolkit, you will need to add `MultiOn Extension` to your browser as explained in the [MultiOn for Chrome](https://multion.notion.site/Download-MultiOn-ddddcfe719f94ab182107ca2612c07a5).

```bash
pip install --upgrade multion langchain -q  

```

```python
from langchain.agents.agent\_toolkits import MultionToolkit  
import os  
  
  
toolkit = MultionToolkit()  
  
toolkit  

```

```python
tools = toolkit.get\_tools()  
tools  

```

## MultiOn Setup[​](#multion-setup "Direct link to MultiOn Setup")

Login to establish connection with your extension.

```python
# Authorize connection to your Browser extention  
import multion  
multion.login()  

```

## Use Multion Toolkit within an Agent[​](#use-multion-toolkit-within-an-agent "Direct link to Use Multion Toolkit within an Agent")

```python
from langchain.llms import OpenAI  
from langchain.agents import initialize\_agent, AgentType  
llm = OpenAI(temperature=0)  
from langchain.agents.agent\_toolkits import MultionToolkit  
toolkit = MultionToolkit()  
tools=toolkit.get\_tools()  
agent = initialize\_agent(  
 tools=toolkit.get\_tools(),  
 llm=llm,  
 agent=AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose = True  
)  

```

```python
agent.run(  
 "Tweet 'Hi from MultiOn'"  
)  

```

- [MultiOn Setup](#multion-setup)
- [Use Multion Toolkit within an Agent](#use-multion-toolkit-within-an-agent)

# Structured tool chat

The structured tool chat agent is capable of using multi-input tools.

Older agents are configured to specify an action input as a single string, but this agent can use the provided tools' `args_schema` to populate the action input.

```python
from langchain.agents import AgentType  
from langchain.chat\_models import ChatOpenAI  
from langchain.agents import initialize\_agent  

```

## Initialize Tools[​](#initialize-tools "Direct link to Initialize Tools")

We will test the agent using a web browser

```python
from langchain.agents.agent\_toolkits import PlayWrightBrowserToolkit  
from langchain.tools.playwright.utils import (  
 create\_async\_playwright\_browser,  
 create\_sync\_playwright\_browser, # A synchronous browser is available, though it isn't compatible with jupyter.  
)  
  
# This import is required only for jupyter notebooks, since they have their own eventloop  
import nest\_asyncio  
nest\_asyncio.apply()  

```

```bash
pip install playwright  
playwright install  

```

```python
async\_browser = create\_async\_playwright\_browser()  
browser\_toolkit = PlayWrightBrowserToolkit.from\_browser(async\_browser=async\_browser)  
tools = browser\_toolkit.get\_tools()  

```

## Use LCEL[​](#use-lcel "Direct link to Use LCEL")

We can first construct this agent using LangChain Expression Language

```python
from langchain import hub  

```

```python
prompt = hub.pull("hwchase17/react-multi-input-json")  

```

```python
from langchain.tools.render import render\_text\_description\_and\_args  

```

```python
prompt = prompt.partial(  
 tools=render\_text\_description\_and\_args(tools),  
 tool\_names=", ".join([t.name for t in tools]),  
)  

```

```python
llm = ChatOpenAI(temperature=0)  
llm\_with\_stop = llm.bind(stop=["Observation"])  

```

```python
from langchain.agents.output\_parsers import JSONAgentOutputParser  
from langchain.agents.format\_scratchpad import format\_log\_to\_str  

```

```python
agent = {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_log\_to\_str(x['intermediate\_steps']),  
} | prompt | llm\_with\_stop | JSONAgentOutputParser()  

```

```python
from langchain.agents import AgentExecutor  

```

```python
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

```python
response = await agent\_executor.ainvoke({"input": "Browse to blog.langchain.dev and summarize the text, please."})  
print(response['output'])  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Action:  
```

{\
"action": "navigate_browser",\
"action_input": {\
"url": "https://blog.langchain.dev"\
}\
}

```
Navigating to https://blog.langchain.dev returned status code 200Action:  
```

{\
"action": "extract_text",\
"action_input": {}\
}

```
  
LangChain LangChain Home GitHub Docs By LangChain Release Notes Write with Us Sign in Subscribe The official LangChain blog. Subscribe now Login Featured Posts Announcing LangChain Hub Using LangSmith to Support Fine-tuning Announcing LangSmith, a unified platform for debugging, testing, evaluating, and monitoring your LLM applications Sep 20 Peering Into the Soul of AI Decision-Making with LangSmith 10 min read Sep 20 LangChain + Docugami Webinar: Lessons from Deploying LLMs with LangSmith 3 min read Sep 18 TED AI Hackathon Kickoff (and projects we’d love to see) 2 min read Sep 12 How to Safely Query Enterprise Data with LangChain Agents + SQL + OpenAI + Gretel 6 min read Sep 12 OpaquePrompts x LangChain: Enhance the privacy of your LangChain application with just one code change 4 min read Load more LangChain © 2023 Sign up Powered by GhostAction:  
```

{\
"action": "Final Answer",\
"action_input": "The LangChain blog features posts on topics such as using LangSmith for fine-tuning, AI decision-making with LangSmith, deploying LLMs with LangSmith, and more. It also includes information on LangChain Hub and upcoming webinars. LangChain is a platform for debugging, testing, evaluating, and monitoring LLM applications."\
}

```
  
> Finished chain.  
The LangChain blog features posts on topics such as using LangSmith for fine-tuning, AI decision-making with LangSmith, deploying LLMs with LangSmith, and more. It also includes information on LangChain Hub and upcoming webinars. LangChain is a platform for debugging, testing, evaluating, and monitoring LLM applications.  

```

## Use off the shelf agent[​](#use-off-the-shelf-agent "Direct link to Use off the shelf agent")

```python
llm = ChatOpenAI(temperature=0) # Also works well with Anthropic models  
agent\_chain = initialize\_agent(tools, llm, agent=AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True)  

```

```python
response = await agent\_chain.ainvoke({"input": "Browse to blog.langchain.dev and summarize the text, please."})  
print(response['output'])  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Action:  
```

{\
"action": "navigate_browser",\
"action_input": {\
"url": "https://blog.langchain.dev"\
}\
}

```
Observation: Navigating to https://blog.langchain.dev returned status code 200  
Thought:I have successfully navigated to the blog.langchain.dev website. Now I need to extract the text from the webpage to summarize it.  
Action:  
```

{\
"action": "extract_text",\
"action_input": {}\
}

```
Observation: LangChain LangChain Home GitHub Docs By LangChain Release Notes Write with Us Sign in Subscribe The official LangChain blog. Subscribe now Login Featured Posts Announcing LangChain Hub Using LangSmith to Support Fine-tuning Announcing LangSmith, a unified platform for debugging, testing, evaluating, and monitoring your LLM applications Sep 20 Peering Into the Soul of AI Decision-Making with LangSmith 10 min read Sep 20 LangChain + Docugami Webinar: Lessons from Deploying LLMs with LangSmith 3 min read Sep 18 TED AI Hackathon Kickoff (and projects we’d love to see) 2 min read Sep 12 How to Safely Query Enterprise Data with LangChain Agents + SQL + OpenAI + Gretel 6 min read Sep 12 OpaquePrompts x LangChain: Enhance the privacy of your LangChain application with just one code change 4 min read Load more LangChain © 2023 Sign up Powered by Ghost  
Thought:I have successfully navigated to the blog.langchain.dev website. The text on the webpage includes featured posts such as "Announcing LangChain Hub," "Using LangSmith to Support Fine-tuning," "Peering Into the Soul of AI Decision-Making with LangSmith," "LangChain + Docugami Webinar: Lessons from Deploying LLMs with LangSmith," "TED AI Hackathon Kickoff (and projects we’d love to see)," "How to Safely Query Enterprise Data with LangChain Agents + SQL + OpenAI + Gretel," and "OpaquePrompts x LangChain: Enhance the privacy of your LangChain application with just one code change." There are also links to other pages on the website.  
  
> Finished chain.  
I have successfully navigated to the blog.langchain.dev website. The text on the webpage includes featured posts such as "Announcing LangChain Hub," "Using LangSmith to Support Fine-tuning," "Peering Into the Soul of AI Decision-Making with LangSmith," "LangChain + Docugami Webinar: Lessons from Deploying LLMs with LangSmith," "TED AI Hackathon Kickoff (and projects we’d love to see)," "How to Safely Query Enterprise Data with LangChain Agents + SQL + OpenAI + Gretel," and "OpaquePrompts x LangChain: Enhance the privacy of your LangChain application with just one code change." There are also links to other pages on the website.  

```

- [Initialize Tools](#initialize-tools)
- [Use LCEL](#use-lcel)
- [Use off the shelf agent](#use-off-the-shelf-agent)

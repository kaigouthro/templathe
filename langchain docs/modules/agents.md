# Agents

The core idea of agents is to use an LLM to choose a sequence of actions to take.
In chains, a sequence of actions is hardcoded (in code).
In agents, a language model is used as a reasoning engine to determine which actions to take and in which order.

Some important terminology (and schema) to know:

1. `AgentAction`: This is a dataclass that represents the action an agent should take. It has a `tool` property (which is the name of the tool that should be invoked) and a `tool_input` property (the input to that tool)
1. `AgentFinish`: This is a dataclass that signifies that the agent has finished and should return to the user. It has a `return_values` parameter, which is a dictionary to return. It often only has one key - `output` - that is a string, and so often it is just this key that is returned.
1. `intermediate_steps`: These represent previous agent actions and corresponding outputs that are passed around. These are important to pass to future iteration so the agent knows what work it has already done. This is typed as a `List[Tuple[AgentAction, Any]]`. Note that observation is currently left as type `Any` to be maximally flexible. In practice, this is often a string.

There are several key components here:

## Agent[​](#agent "Direct link to Agent")

This is the chain responsible for deciding what step to take next.
This is powered by a language model and a prompt.
The inputs to this chain are:

1. List of available tools
1. User input
1. Any previously executed steps (`intermediate_steps`)

This chain then returns either the next action to take or the final response to send to the user (`AgentAction` or `AgentFinish`).

Different agents have different prompting styles for reasoning, different ways of encoding input, and different ways of parsing the output.
For a full list of agent types see [agent types](/docs/modules/agents/agent_types/)

## Tools[​](#tools "Direct link to Tools")

Tools are functions that an agent calls.
There are two important considerations here:

1. Giving the agent access to the right tools
1. Describing the tools in a way that is most helpful to the agent

Without both, the agent you are trying to build will not work.
If you don't give the agent access to a correct set of tools, it will never be able to accomplish the objective.
If you don't describe the tools properly, the agent won't know how to properly use them.

LangChain provides a wide set of tools to get started, but also makes it easy to define your own (including custom descriptions).
For a full list of tools, see [here](/docs/modules/agents/tools/)

## Toolkits[​](#toolkits "Direct link to Toolkits")

Often the set of tools an agent has access to is more important than a single tool.
For this LangChain provides the concept of toolkits - groups of tools needed to accomplish specific objectives.
There are generally around 3-5 tools in a toolkit.

LangChain provides a wide set of toolkits to get started.
For a full list of toolkits, see [here](/docs/modules/agents/toolkits/)

## AgentExecutor[​](#agentexecutor "Direct link to AgentExecutor")

The agent executor is the runtime for an agent.
This is what actually calls the agent and executes the actions it chooses.
Pseudocode for this runtime is below:

```python
next\_action = agent.get\_action(...)  
while next\_action != AgentFinish:  
 observation = run(next\_action)  
 next\_action = agent.get\_action(..., next\_action, observation)  
return next\_action  

```

While this may seem simple, there are several complexities this runtime handles for you, including:

1. Handling cases where the agent selects a non-existent tool
1. Handling cases where the tool errors
1. Handling cases where the agent produces output that cannot be parsed into a tool invocation
1. Logging and observability at all levels (agent decisions, tool calls) either to stdout or [LangSmith](https://smith.langchain.com).

## Other types of agent runtimes[​](#other-types-of-agent-runtimes "Direct link to Other types of agent runtimes")

The `AgentExecutor` class is the main agent runtime supported by LangChain.
However, there are other, more experimental runtimes we also support.
These include:

- [Plan-and-execute Agent](/docs/use_cases/more/agents/autonomous_agents/plan_and_execute)
- [Baby AGI](/docs/use_cases/more/agents/autonomous_agents/baby_agi)
- [Auto GPT](/docs/use_cases/more/agents/autonomous_agents/autogpt)

## Get started[​](#get-started "Direct link to Get started")

This will go over how to get started building an agent.
We will create this agent from scratch, using LangChain Expression Language.
We will then define custom tools, and then run it in a custom loop (we will also show how to use the standard LangChain `AgentExecutor`).

### Set up the agent[​](#set-up-the-agent "Direct link to Set up the agent")

We first need to create our agent.
This is the chain responsible for determining what action to take next.

In this example, we will use OpenAI Function Calling to create this agent.
This is generally the most reliable way create agents.
In this example we will show what it is like to construct this agent from scratch, using LangChain Expression Language.

For this guide, we will construct a custom agent that has access to a custom tool.
We are choosing this example because we think for most use cases you will NEED to customize either the agent or the tools.
The tool we will give the agent is a tool to calculate the length of a word.
This is useful because this is actually something LLMs can mess up due to tokenization.
We will first create it WITHOUT memory, but we will then show how to add memory in.
Memory is needed to enable conversation.

First, let's load the language model we're going to use to control the agent.

```python
from langchain.chat\_models import ChatOpenAI  
llm = ChatOpenAI(temperature=0)  

```

Next, let's define some tools to use.
Let's write a really simple Python function to calculate the length of a word that is passed in.

```python
from langchain.agents import tool  
  
@tool  
def get\_word\_length(word: str) -> int:  
 """Returns the length of a word."""  
 return len(word)  
  
tools = [get\_word\_length]  

```

Now let us create the prompt.
Because OpenAI Function Calling is finetuned for tool usage, we hardly need any instructions on how to reason, or how to output format.
We will just have two input variables: `input` (for the user question) and `agent_scratchpad` (for any previous steps taken)

```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder  
prompt = ChatPromptTemplate.from\_messages([  
 ("system", "You are very powerful assistant, but bad at calculating lengths of words."),  
 ("user", "{input}"),  
 MessagesPlaceholder(variable\_name="agent\_scratchpad"),  
])  

```

How does the agent know what tools it can use?
Those are passed in as a separate argument, so we can bind those as keyword arguments to the LLM.

```python
from langchain.tools.render import format\_tool\_to\_openai\_function  
llm\_with\_tools = llm.bind(  
 functions=[format\_tool\_to\_openai\_function(t) for t in tools]  
)  

```

Putting those pieces together, we can now create the agent.
We will import two last utility functions: a component for formatting intermediate steps to messages, and a component for converting the output message into an agent action/agent finish.

```python
from langchain.agents.format\_scratchpad import format\_to\_openai\_functions  
from langchain.agents.output\_parsers import OpenAIFunctionsAgentOutputParser  
agent = {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_to\_openai\_functions(x['intermediate\_steps'])  
} | prompt | llm\_with\_tools | OpenAIFunctionsAgentOutputParser()  

```

Now that we have our agent, let's play around with it!
Let's pass in a simple question and empty intermediate steps and see what it returns:

```python
agent.invoke({  
 "input": "how many letters in the word educa?",  
 "intermediate\_steps": []  
})  

```

We can see that it responds with an `AgentAction` to take (it's actually an `AgentActionMessageLog` - a subclass of `AgentAction` which also tracks the full message log).

So this is just the first step - now we need to write a runtime for this.
The simplest one is just one that continuously loops, calling the agent, then taking the action, and repeating until an `AgentFinish` is returned.
Let's code that up below:

```python
from langchain.schema.agent import AgentFinish  
intermediate\_steps = []  
while True:  
 output = agent.invoke({  
 "input": "how many letters in the word educa?",  
 "intermediate\_steps": intermediate\_steps  
 })  
 if isinstance(output, AgentFinish):  
 final\_result = output.return\_values["output"]  
 break  
 else:  
 print(output.tool, output.tool\_input)  
 tool = {  
 "get\_word\_length": get\_word\_length  
 }[output.tool]  
 observation = tool.run(output.tool\_input)  
 intermediate\_steps.append((output, observation))  
print(final\_result)  

```

We can see this prints out the following:

```text
get\_word\_length {'word': 'educa'}  
There are 5 letters in the word "educa".  

```

Woo! It's working.

To simplify this a bit, we can import and use the `AgentExecutor` class.
This bundles up all of the above and adds in error handling, early stopping, tracing, and other quality-of-life improvements that reduce safeguards you need to write.

```python
from langchain.agents import AgentExecutor  
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

Now let's test it out!

```python
agent\_executor.invoke({"input": "how many letters in the word educa?"})  

```

```text
  
  
 > Entering new AgentExecutor chain...  
  
 Invoking: `get\_word\_length` with `{'word': 'educa'}`  
  
 5  
  
 There are 5 letters in the word "educa".  
  
 > Finished chain.  
  
 'There are 5 letters in the word "educa".'  

```

This is great - we have an agent!
However, this agent is stateless - it doesn't remember anything about previous interactions.
This means you can't ask follow up questions easily.
Let's fix that by adding in memory.

In order to do this, we need to do two things:

1. Add a place for memory variables to go in the prompt
1. Keep track of the chat history

First, let's add a place for memory in the prompt.
We do this by adding a placeholder for messages with the key `"chat_history"`.
Notice that we put this ABOVE the new user input (to follow the conversation flow).

```python
from langchain.prompts import MessagesPlaceholder  
  
MEMORY\_KEY = "chat\_history"  
prompt = ChatPromptTemplate.from\_messages([  
 ("system", "You are very powerful assistant, but bad at calculating lengths of words."),  
 MessagesPlaceholder(variable\_name=MEMORY\_KEY),  
 ("user", "{input}"),  
 MessagesPlaceholder(variable\_name="agent\_scratchpad"),  
])  

```

We can then set up a list to track the chat history

```text
from langchain.schema.messages import HumanMessage, AIMessage  
chat\_history = []  

```

We can then put it all together!

```python
agent = {  
 "input": lambda x: x["input"],  
 "agent\_scratchpad": lambda x: format\_to\_openai\_functions(x['intermediate\_steps']),  
 "chat\_history": lambda x: x["chat\_history"]  
} | prompt | llm\_with\_tools | OpenAIFunctionsAgentOutputParser()  
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

When running, we now need to track the inputs and outputs as chat history

```text
input1 = "how many letters in the word educa?"  
result = agent\_executor.invoke({"input": input1, "chat\_history": chat\_history})  
chat\_history.append(HumanMessage(content=input1))  
chat\_history.append(AIMessage(content=result['output']))  
agent\_executor.invoke({"input": "is that a real word?", "chat\_history": chat\_history})  

```

## Next Steps[​](#next-steps "Direct link to Next Steps")

Awesome! You've now run your first end-to-end agent.
To dive deeper, you can:

- Check out all the different [agent types](/docs/modules/agents/agent_types/) supported

- Learn all the controls for [AgentExecutor](/docs/modules/agents/how_to/)

- See a full list of all the off-the-shelf [toolkits](/docs/modules/agents/toolkits/) we provide

- Explore all the individual [tools](/docs/modules/agents/tools/) supported

- [Agent](#agent)

- [Tools](#tools)

- [Toolkits](#toolkits)

- [AgentExecutor](#agentexecutor)

- [Other types of agent runtimes](#other-types-of-agent-runtimes)

- [Get started](#get-started)

  - [Set up the agent](#set-up-the-agent)

- [Next Steps](#next-steps)

- [Set up the agent](#set-up-the-agent)

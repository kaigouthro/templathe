# Conversation Summary

Now let's take a look at using a slightly more complex type of memory - `ConversationSummaryMemory`. This type of memory creates a summary of the conversation over time. This can be useful for condensing information from the conversation over time.
Conversation summary memory summarizes the conversation as it happens and stores the current summary in memory. This memory can then be used to inject the summary of the conversation so far into a prompt/chain. This memory is most useful for longer conversations, where keeping the past message history in the prompt verbatim would take up too many tokens.

Let's first explore the basic functionality of this type of memory.

```python
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory  
from langchain.llms import OpenAI  

```

```python
memory = ConversationSummaryMemory(llm=OpenAI(temperature=0))  
memory.save\_context({"input": "hi"}, {"output": "whats up"})  

```

```python
memory.load\_memory\_variables({})  

```

```text
 {'history': '\nThe human greets the AI, to which the AI responds.'}  

```

We can also get the history as a list of messages (this is useful if you are using this with a chat model).

```python
memory = ConversationSummaryMemory(llm=OpenAI(temperature=0), return\_messages=True)  
memory.save\_context({"input": "hi"}, {"output": "whats up"})  

```

```python
memory.load\_memory\_variables({})  

```

```text
 {'history': [SystemMessage(content='\nThe human greets the AI, to which the AI responds.', additional\_kwargs={})]}  

```

We can also utilize the `predict_new_summary` method directly.

```python
messages = memory.chat\_memory.messages  
previous\_summary = ""  
memory.predict\_new\_summary(messages, previous\_summary)  

```

```text
 '\nThe human greets the AI, to which the AI responds.'  

```

## Initializing with messages/existing summary[​](#initializing-with-messagesexisting-summary "Direct link to Initializing with messages/existing summary")

If you have messages outside this class, you can easily initialize the class with `ChatMessageHistory`. During loading, a summary will be calculated.

```python
history = ChatMessageHistory()  
history.add\_user\_message("hi")  
history.add\_ai\_message("hi there!")  

```

```python
memory = ConversationSummaryMemory.from\_messages(  
 llm=OpenAI(temperature=0),  
 chat\_memory=history,  
 return\_messages=True  
)  

```

```python
memory.buffer  

```

```text
 '\nThe human greets the AI, to which the AI responds with a friendly greeting.'  

```

Optionally you can speed up initialization using a previously generated summary, and avoid regenerating the summary by just initializing directly.

```python
memory = ConversationSummaryMemory(  
 llm=OpenAI(temperature=0),  
 buffer="The human asks what the AI thinks of artificial intelligence. The AI thinks artificial intelligence is a force for good because it will help humans reach their full potential.",  
 chat\_memory=history,  
 return\_messages=True  
)  

```

## Using in a chain[​](#using-in-a-chain "Direct link to Using in a chain")

Let's walk through an example of using this in a chain, again setting `verbose=True` so we can see the prompt.

```python
from langchain.llms import OpenAI  
from langchain.chains import ConversationChain  
llm = OpenAI(temperature=0)  
conversation\_with\_summary = ConversationChain(  
 llm=llm,  
 memory=ConversationSummaryMemory(llm=OpenAI()),  
 verbose=True  
)  
conversation\_with\_summary.predict(input="Hi, what's up?")  

```

```text
  
  
 > Entering new ConversationChain chain...  
 Prompt after formatting:  
 The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.  
  
 Current conversation:  
  
 Human: Hi, what's up?  
 AI:  
  
 > Finished chain.  
  
  
  
  
  
 " Hi there! I'm doing great. I'm currently helping a customer with a technical issue. How about you?"  

```

```python
conversation\_with\_summary.predict(input="Tell me more about it!")  

```

```text
  
  
 > Entering new ConversationChain chain...  
 Prompt after formatting:  
 The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.  
  
 Current conversation:  
  
 The human greeted the AI and asked how it was doing. The AI replied that it was doing great and was currently helping a customer with a technical issue.  
 Human: Tell me more about it!  
 AI:  
  
 > Finished chain.  
  
  
  
  
  
 " Sure! The customer is having trouble with their computer not connecting to the internet. I'm helping them troubleshoot the issue and figure out what the problem is. So far, we've tried resetting the router and checking the network settings, but the issue still persists. We're currently looking into other possible solutions."  

```

```python
conversation\_with\_summary.predict(input="Very cool -- what is the scope of the project?")  

```

```text
  
  
 > Entering new ConversationChain chain...  
 Prompt after formatting:  
 The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.  
  
 Current conversation:  
  
 The human greeted the AI and asked how it was doing. The AI replied that it was doing great and was currently helping a customer with a technical issue where their computer was not connecting to the internet. The AI was troubleshooting the issue and had already tried resetting the router and checking the network settings, but the issue still persisted and they were looking into other possible solutions.  
 Human: Very cool -- what is the scope of the project?  
 AI:  
  
 > Finished chain.  
  
  
  
  
  
 " The scope of the project is to troubleshoot the customer's computer issue and find a solution that will allow them to connect to the internet. We are currently exploring different possibilities and have already tried resetting the router and checking the network settings, but the issue still persists."  

```

- [Initializing with messages/existing summary](#initializing-with-messagesexisting-summary)
- [Using in a chain](#using-in-a-chain)

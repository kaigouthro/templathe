# Conversation Knowledge Graph

This type of memory uses a knowledge graph to recreate memory.

## Using memory with LLM[​](#using-memory-with-llm "Direct link to Using memory with LLM")

```python
from langchain.memory import ConversationKGMemory  
from langchain.llms import OpenAI  

```

```python
llm = OpenAI(temperature=0)  
memory = ConversationKGMemory(llm=llm)  
memory.save\_context({"input": "say hi to sam"}, {"output": "who is sam"})  
memory.save\_context({"input": "sam is a friend"}, {"output": "okay"})  

```

```python
memory.load\_memory\_variables({"input": "who is sam"})  

```

```text
 {'history': 'On Sam: Sam is friend.'}  

```

We can also get the history as a list of messages (this is useful if you are using this with a chat model).

```python
memory = ConversationKGMemory(llm=llm, return\_messages=True)  
memory.save\_context({"input": "say hi to sam"}, {"output": "who is sam"})  
memory.save\_context({"input": "sam is a friend"}, {"output": "okay"})  

```

```python
memory.load\_memory\_variables({"input": "who is sam"})  

```

```text
 {'history': [SystemMessage(content='On Sam: Sam is friend.', additional\_kwargs={})]}  

```

We can also more modularly get current entities from a new message (will use previous messages as context).

```python
memory.get\_current\_entities("what's Sams favorite color?")  

```

```text
 ['Sam']  

```

We can also more modularly get knowledge triplets from a new message (will use previous messages as context).

```python
memory.get\_knowledge\_triplets("her favorite color is red")  

```

```text
 [KnowledgeTriple(subject='Sam', predicate='favorite color', object\_='red')]  

```

## Using in a chain[​](#using-in-a-chain "Direct link to Using in a chain")

Let's now use this in a chain!

```python
llm = OpenAI(temperature=0)  
from langchain.prompts.prompt import PromptTemplate  
from langchain.chains import ConversationChain  
  
template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context.   
If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.  
  
Relevant Information:  
  
{history}  
  
Conversation:  
Human: {input}  
AI:"""  
prompt = PromptTemplate(input\_variables=["history", "input"], template=template)  
conversation\_with\_kg = ConversationChain(  
 llm=llm, verbose=True, prompt=prompt, memory=ConversationKGMemory(llm=llm)  
)  

```

```python
conversation\_with\_kg.predict(input="Hi, what's up?")  

```

```text
   
   
 > Entering new ConversationChain chain...  
 Prompt after formatting:  
 The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context.   
 If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.  
   
 Relevant Information:  
   
   
   
 Conversation:  
 Human: Hi, what's up?  
 AI:  
   
 > Finished chain.  
  
  
  
  
  
 " Hi there! I'm doing great. I'm currently in the process of learning about the world around me. I'm learning about different cultures, languages, and customs. It's really fascinating! How about you?"  

```

```python
conversation\_with\_kg.predict(  
 input="My name is James and I'm helping Will. He's an engineer."  
)  

```

```text
   
   
 > Entering new ConversationChain chain...  
 Prompt after formatting:  
 The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context.   
 If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.  
   
 Relevant Information:  
   
   
   
 Conversation:  
 Human: My name is James and I'm helping Will. He's an engineer.  
 AI:  
   
 > Finished chain.  
  
  
  
  
  
 " Hi James, it's nice to meet you. I'm an AI and I understand you're helping Will, the engineer. What kind of engineering does he do?"  

```

```python
conversation\_with\_kg.predict(input="What do you know about Will?")  

```

```text
   
   
 > Entering new ConversationChain chain...  
 Prompt after formatting:  
 The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context.   
 If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.  
   
 Relevant Information:  
   
 On Will: Will is an engineer.  
   
 Conversation:  
 Human: What do you know about Will?  
 AI:  
   
 > Finished chain.  
  
  
  
  
  
 ' Will is an engineer.'  

```

- [Using memory with LLM](#using-memory-with-llm)
- [Using in a chain](#using-in-a-chain)

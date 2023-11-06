# Streamlit

[Streamlit](https://docs.streamlit.io/) is an open-source Python library that makes it easy to create and share beautiful,
custom web apps for machine learning and data science.

This notebook goes over how to store and use chat message history in a `Streamlit` app. `StreamlitChatMessageHistory` will store messages in
[Streamlit session state](https://docs.streamlit.io/library/api-reference/session-state)
at the specified `key=`. The default key is `"langchain_messages"`.

- Note, `StreamlitChatMessageHistory` only works when run in a Streamlit app.
- You may also be interested in [StreamlitCallbackHandler](/docs/integrations/callbacks/streamlit) for LangChain.
- For more on Streamlit check out their
  [getting started documentation](https://docs.streamlit.io/library/get-started).

You can see the [full app example running here](https://langchain-st-memory.streamlit.app/), and more examples in
[github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).

```python
from langchain.memory import StreamlitChatMessageHistory  
  
history = StreamlitChatMessageHistory(key="chat\_messages")  
  
history.add\_user\_message("hi!")  
history.add\_ai\_message("whats up?")  

```

```python
history.messages  

```

You can integrate `StreamlitChatMessageHistory` into `ConversationBufferMemory` and chains or agents as usual. The history will be persisted across re-runs of the Streamlit app within a given user session. A given `StreamlitChatMessageHistory` will NOT be persisted or shared across user sessions.

```python
from langchain.memory import ConversationBufferMemory  
from langchain.memory.chat\_message\_histories import StreamlitChatMessageHistory  
  
# Optionally, specify your own session\_state key for storing messages  
msgs = StreamlitChatMessageHistory(key="special\_app\_key")  
  
memory = ConversationBufferMemory(memory\_key="history", chat\_memory=msgs)  
if len(msgs.messages) == 0:  
 msgs.add\_ai\_message("How can I help you?")  

```

```python
from langchain.chains import LLMChain  
from langchain.llms import OpenAI  
from langchain.prompts import PromptTemplate  
template = """You are an AI chatbot having a conversation with a human.  
  
{history}  
Human: {human\_input}  
AI: """  
prompt = PromptTemplate(input\_variables=["history", "human\_input"], template=template)  
  
# Add the memory to an LLMChain as usual  
llm\_chain = LLMChain(llm=OpenAI(), prompt=prompt, memory=memory)  

```

Conversational Streamlit apps will often re-draw each previous chat message on every re-run. This is easy to do by iterating through `StreamlitChatMessageHistory.messages`:

```python
import streamlit as st  
  
for msg in msgs.messages:  
 st.chat\_message(msg.type).write(msg.content)  
  
if prompt := st.chat\_input():  
 st.chat\_message("human").write(prompt)  
  
 # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.  
 response = llm\_chain.run(prompt)  
 st.chat\_message("ai").write(response)  

```

**[View the final app](https://langchain-st-memory.streamlit.app/).**

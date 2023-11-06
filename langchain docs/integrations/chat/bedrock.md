# Bedrock Chat

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is a fully managed service that makes FMs from leading AI startups and Amazon available via an API, so you can choose from a wide range of FMs to find the model that is best suited for your use case

```python
%pip install boto3  

```

```python
from langchain.chat\_models import BedrockChat  
from langchain.schema import HumanMessage  

```

```python
chat = BedrockChat(model\_id="anthropic.claude-v2", model\_kwargs={"temperature":0.1})  

```

```python
messages = [  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 )  
]  
chat(messages)  

```

```text
 AIMessage(content=" Voici la traduction en français : J'adore programmer.", additional\_kwargs={}, example=False)  

```

### For BedrockChat with Streaming[​](#for-bedrockchat-with-streaming "Direct link to For BedrockChat with Streaming")

```python
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
  
chat = BedrockChat(  
 model\_id="anthropic.claude-v2",  
 streaming=True,  
 callbacks=[StreamingStdOutCallbackHandler()],  
 model\_kwargs={"temperature": 0.1},  
)  

```

```python
messages = [  
 HumanMessage(  
 content="Translate this sentence from English to French. I love programming."  
 )  
]  
chat(messages)  

```

- [For BedrockChat with Streaming](#for-bedrockchat-with-streaming)

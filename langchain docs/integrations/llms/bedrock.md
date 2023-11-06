# Bedrock

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is a fully managed service that makes FMs from leading AI startups and Amazon available via an API, so you can choose from a wide range of FMs to find the model that is best suited for your use case

```python
%pip install boto3  

```

```python
from langchain.llms import Bedrock  
  
llm = Bedrock(  
 credentials\_profile\_name="bedrock-admin",  
 model\_id="amazon.titan-text-express-v1"  
)  

```

### Using in a conversation chain[​](#using-in-a-conversation-chain "Direct link to Using in a conversation chain")

```python
from langchain.chains import ConversationChain  
from langchain.memory import ConversationBufferMemory  
  
conversation = ConversationChain(  
 llm=llm, verbose=True, memory=ConversationBufferMemory()  
)  
  
conversation.predict(input="Hi there!")  

```

### Conversation Chain With Streaming[​](#conversation-chain-with-streaming "Direct link to Conversation Chain With Streaming")

```python
from langchain.llms import Bedrock  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
  
  
llm = Bedrock(  
 credentials\_profile\_name="bedrock-admin",  
 model\_id="amazon.titan-text-express-v1",  
 streaming=True,  
 callbacks=[StreamingStdOutCallbackHandler()],  
)  

```

```python
conversation = ConversationChain(  
 llm=llm, verbose=True, memory=ConversationBufferMemory()  
)  
  
conversation.predict(input="Hi there!")  

```

- [Using in a conversation chain](#using-in-a-conversation-chain)
- [Conversation Chain With Streaming](#conversation-chain-with-streaming)

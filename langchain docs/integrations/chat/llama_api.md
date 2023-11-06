# Llama API

This notebook shows how to use LangChain with [LlamaAPI](https://llama-api.com/) - a hosted version of Llama2 that adds in support for function calling.

!pip install -U llamaapi

```python
from llamaapi import LlamaAPI  
  
# Replace 'Your\_API\_Token' with your actual API token  
llama = LlamaAPI('Your\_API\_Token')  

```

```python
from langchain\_experimental.llms import ChatLlamaAPI  

```

```text
 /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check\_latest\_version.py:32: UserWarning: A newer version of deeplake (3.6.12) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.  
 warnings.warn(  

```

```python
model = ChatLlamaAPI(client=llama)  

```

```python
from langchain.chains import create\_tagging\_chain  
  
schema = {  
 "properties": {  
 "sentiment": {"type": "string", 'description': 'the sentiment encountered in the passage'},  
 "aggressiveness": {"type": "integer", 'description': 'a 0-10 score of how aggressive the passage is'},  
 "language": {"type": "string", 'description': 'the language of the passage'},  
 }  
}  
  
chain = create\_tagging\_chain(schema, model)  

```

```python
chain.run("give me your money")  

```

```text
 {'sentiment': 'aggressive', 'aggressiveness': 8, 'language': 'english'}  

```

# Anthropic Functions

This notebook shows how to use an experimental wrapper around Anthropic that gives it the same API as OpenAI Functions.

```python
from langchain\_experimental.llms.anthropic\_functions import AnthropicFunctions  

```

```text
 /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check\_latest\_version.py:32: UserWarning: A newer version of deeplake (3.6.14) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.  
 warnings.warn(  

```

## Initialize Model[​](#initialize-model "Direct link to Initialize Model")

You can initialize this wrapper the same way you'd initialize ChatAnthropic

```python
model = AnthropicFunctions(model='claude-2')  

```

## Passing in functions[​](#passing-in-functions "Direct link to Passing in functions")

You can now pass in functions in a similar way

```python
functions=[  
 {  
 "name": "get\_current\_weather",  
 "description": "Get the current weather in a given location",  
 "parameters": {  
 "type": "object",  
 "properties": {  
 "location": {  
 "type": "string",  
 "description": "The city and state, e.g. San Francisco, CA"  
 },  
 "unit": {  
 "type": "string",  
 "enum": ["celsius", "fahrenheit"]  
 }  
 },  
 "required": ["location"]  
 }  
 }  
 ]  

```

```python
from langchain.schema import HumanMessage  

```

```python
response = model.predict\_messages(  
 [HumanMessage(content="whats the weater in boston?")],   
 functions=functions  
)  

```

```python
response  

```

```text
 AIMessage(content=' ', additional\_kwargs={'function\_call': {'name': 'get\_current\_weather', 'arguments': '{"location": "Boston, MA", "unit": "fahrenheit"}'}}, example=False)  

```

## Using for extraction[​](#using-for-extraction "Direct link to Using for extraction")

You can now use this for extraction.

```python
from langchain.chains import create\_extraction\_chain  
schema = {  
 "properties": {  
 "name": {"type": "string"},  
 "height": {"type": "integer"},  
 "hair\_color": {"type": "string"},  
 },  
 "required": ["name", "height"],  
}  
inp = """  
Alex is 5 feet tall. Claudia is 1 feet taller Alex and jumps higher than him. Claudia is a brunette and Alex is blonde.  
 """  

```

```python
chain = create\_extraction\_chain(schema, model)  

```

```python
chain.run(inp)  

```

```text
 [{'name': 'Alex', 'height': '5', 'hair\_color': 'blonde'},  
 {'name': 'Claudia', 'height': '6', 'hair\_color': 'brunette'}]  

```

## Using for tagging[​](#using-for-tagging "Direct link to Using for tagging")

You can now use this for tagging

```python
from langchain.chains import create\_tagging\_chain  

```

```python
schema = {  
 "properties": {  
 "sentiment": {"type": "string"},  
 "aggressiveness": {"type": "integer"},  
 "language": {"type": "string"},  
 }  
}  

```

```python
chain = create\_tagging\_chain(schema, model)  

```

```python
chain.run("this is really cool")  

```

```text
 {'sentiment': 'positive', 'aggressiveness': '0', 'language': 'english'}  

```

- [Initialize Model](#initialize-model)
- [Passing in functions](#passing-in-functions)
- [Using for extraction](#using-for-extraction)
- [Using for tagging](#using-for-tagging)

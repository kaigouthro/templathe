# Different call methods

All classes inherited from `Chain` offer a few ways of running chain logic. The most direct one is by using `__call__`:

```python
chat = ChatOpenAI(temperature=0)  
prompt\_template = "Tell me a {adjective} joke"  
llm\_chain = LLMChain(llm=chat, prompt=PromptTemplate.from\_template(prompt\_template))  
  
llm\_chain(inputs={"adjective": "corny"})  

```

```text
 {'adjective': 'corny',  
 'text': 'Why did the tomato turn red? Because it saw the salad dressing!'}  

```

By default, `__call__` returns both the input and output key values. You can configure it to only return output key values by setting `return_only_outputs` to `True`.

```python
llm\_chain("corny", return\_only\_outputs=True)  

```

```text
 {'text': 'Why did the tomato turn red? Because it saw the salad dressing!'}  

```

If the `Chain` only outputs one output key (i.e. only has one element in its `output_keys`), you can use `run` method. Note that `run` outputs a string instead of a dictionary.

```python
# llm\_chain only has one output key, so we can use run  
llm\_chain.output\_keys  

```

```text
 ['text']  

```

```python
llm\_chain.run({"adjective": "corny"})  

```

```text
 'Why did the tomato turn red? Because it saw the salad dressing!'  

```

In the case of one input key, you can input the string directly without specifying the input mapping.

```python
# These two are equivalent  
llm\_chain.run({"adjective": "corny"})  
llm\_chain.run("corny")  
  
# These two are also equivalent  
llm\_chain("corny")  
llm\_chain({"adjective": "corny"})  

```

```text
 {'adjective': 'corny',  
 'text': 'Why did the tomato turn red? Because it saw the salad dressing!'}  

```

Tips: You can easily integrate a `Chain` object as a `Tool` in your `Agent` via its `run` method. See an example [here](/docs/modules/agents/tools/how_to/custom_tools).

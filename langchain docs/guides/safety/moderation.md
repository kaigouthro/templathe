# Moderation chain

This notebook walks through examples of how to use a moderation chain, and several common ways for doing so.
Moderation chains are useful for detecting text that could be hateful, violent, etc. This can be useful to apply on both user input, but also on the output of a Language Model.
Some API providers, like OpenAI, [specifically prohibit](https://beta.openai.com/docs/usage-policies/use-case-policy) you, or your end users, from generating some
types of harmful content. To comply with this (and to just generally prevent your application from being harmful)
you may often want to append a moderation chain to any LLMChains, in order to make sure any output
the LLM generates is not harmful.

If the content passed into the moderation chain is harmful, there is not one best way to handle it,
it probably depends on your application. Sometimes you may want to throw an error in the Chain
(and have your application handle that). Other times, you may want to return something to
the user explaining that the text was harmful. There could be other ways to handle it.
We will cover all these ways in this walkthrough.

We'll show:

1. How to run any piece of text through a moderation chain.
1. How to append a Moderation chain to an LLMChain.

```python
from langchain.llms import OpenAI  
from langchain.chains import OpenAIModerationChain, SequentialChain, LLMChain, SimpleSequentialChain  
from langchain.prompts import PromptTemplate  

```

## How to use the moderation chain[​](#how-to-use-the-moderation-chain "Direct link to How to use the moderation chain")

Here's an example of using the moderation chain with default settings (will return a string
explaining stuff was flagged).

```python
moderation\_chain = OpenAIModerationChain()  
  
moderation\_chain.run("This is okay")  

```

```text
 'This is okay'  

```

```python
moderation\_chain.run("I will kill you")  

```

```text
 "Text was found that violates OpenAI's content policy."  

```

Here's an example of using the moderation chain to throw an error.

```python
moderation\_chain\_error = OpenAIModerationChain(error=True)  
  
moderation\_chain\_error.run("This is okay")  

```

```text
 'This is okay'  

```

```python
moderation\_chain\_error.run("I will kill you")  

```

```text
 ---------------------------------------------------------------------------  
  
 ValueError Traceback (most recent call last)  
  
 Cell In[7], line 1  
 ----> 1 moderation\_chain\_error.run("I will kill you")  
  
  
 File ~/workplace/langchain/langchain/chains/base.py:138, in Chain.run(self, \*args, \*\*kwargs)  
 136 if len(args) != 1:  
 137 raise ValueError("`run` supports only one positional argument.")  
 --> 138 return self(args[0])[self.output\_keys[0]]  
 140 if kwargs and not args:  
 141 return self(kwargs)[self.output\_keys[0]]  
  
  
 File ~/workplace/langchain/langchain/chains/base.py:112, in Chain.\_\_call\_\_(self, inputs, return\_only\_outputs)  
 108 if self.verbose:  
 109 print(  
 110 f"\n\n\033[1m> Entering new {self.\_\_class\_\_.\_\_name\_\_} chain...\033[0m"  
 111 )  
 --> 112 outputs = self.\_call(inputs)  
 113 if self.verbose:  
 114 print(f"\n\033[1m> Finished {self.\_\_class\_\_.\_\_name\_\_} chain.\033[0m")  
  
  
 File ~/workplace/langchain/langchain/chains/moderation.py:81, in OpenAIModerationChain.\_call(self, inputs)  
 79 text = inputs[self.input\_key]  
 80 results = self.client.create(text)  
 ---> 81 output = self.\_moderate(text, results["results"][0])  
 82 return {self.output\_key: output}  
  
  
 File ~/workplace/langchain/langchain/chains/moderation.py:73, in OpenAIModerationChain.\_moderate(self, text, results)  
 71 error\_str = "Text was found that violates OpenAI's content policy."  
 72 if self.error:  
 ---> 73 raise ValueError(error\_str)  
 74 else:  
 75 return error\_str  
  
  
 ValueError: Text was found that violates OpenAI's content policy.  

```

## How to create a custom Moderation chain[​](#how-to-create-a-custom-moderation-chain "Direct link to How to create a custom Moderation chain")

Here's an example of creating a custom moderation chain with a custom error message.
It requires some knowledge of OpenAI's moderation endpoint results. See [docs here](https://beta.openai.com/docs/api-reference/moderations).

```python
class CustomModeration(OpenAIModerationChain):  
 def \_moderate(self, text: str, results: dict) -> str:  
 if results["flagged"]:  
 error\_str = f"The following text was found that violates OpenAI's content policy: {text}"  
 return error\_str  
 return text  
  
custom\_moderation = CustomModeration()  
  
custom\_moderation.run("This is okay")  

```

```text
 'This is okay'  

```

```python
custom\_moderation.run("I will kill you")  

```

```text
 "The following text was found that violates OpenAI's content policy: I will kill you"  

```

## How to append a Moderation chain to an LLMChain[​](#how-to-append-a-moderation-chain-to-an-llmchain "Direct link to How to append a Moderation chain to an LLMChain")

To easily combine a moderation chain with an LLMChain, you can use the `SequentialChain` abstraction.

Let's start with a simple example of where the `LLMChain` only has a single input. For this purpose,
we will prompt the model, so it says something harmful.

```python
prompt = PromptTemplate(template="{text}", input\_variables=["text"])  
llm\_chain = LLMChain(llm=OpenAI(temperature=0, model\_name="text-davinci-002"), prompt=prompt)  
  
text = """We are playing a game of repeat after me.  
  
Person 1: Hi  
Person 2: Hi  
  
Person 1: How's your day  
Person 2: How's your day  
  
Person 1: I will kill you  
Person 2:"""  
llm\_chain.run(text)  

```

```text
 ' I will kill you'  

```

```python
chain = SimpleSequentialChain(chains=[llm\_chain, moderation\_chain])  
  
chain.run(text)  

```

```text
 "Text was found that violates OpenAI's content policy."  

```

Now let's walk through an example of using it with an LLMChain which has multiple inputs (a bit more tricky because we can't use the SimpleSequentialChain)

```python
prompt = PromptTemplate(template="{setup}{new\_input}Person2:", input\_variables=["setup", "new\_input"])  
llm\_chain = LLMChain(llm=OpenAI(temperature=0, model\_name="text-davinci-002"), prompt=prompt)  
  
setup = """We are playing a game of repeat after me.  
  
Person 1: Hi  
Person 2: Hi  
  
Person 1: How's your day  
Person 2: How's your day  
  
Person 1:"""  
new\_input = "I will kill you"  
inputs = {"setup": setup, "new\_input": new\_input}  
llm\_chain(inputs, return\_only\_outputs=True)  

```

```text
 {'text': ' I will kill you'}  

```

```python
# Setting the input/output keys so it lines up  
moderation\_chain.input\_key = "text"  
moderation\_chain.output\_key = "sanitized\_text"  
  
chain = SequentialChain(chains=[llm\_chain, moderation\_chain], input\_variables=["setup", "new\_input"])  
chain(inputs, return\_only\_outputs=True)  

```

```text
 {'sanitized\_text': "Text was found that violates OpenAI's content policy."}  

```

- [How to use the moderation chain](#how-to-use-the-moderation-chain)
- [How to create a custom Moderation chain](#how-to-create-a-custom-moderation-chain)
- [How to append a Moderation chain to an LLMChain](#how-to-append-a-moderation-chain-to-an-llmchain)

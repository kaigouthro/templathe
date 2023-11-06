# LLM

The most common type of chaining in any LLM application is combining a prompt template with an LLM and optionally an output parser.

The recommended way to do this is using LangChain Expression Language. We also continue to support the legacy `LLMChain`, which is a single class for composing these three components.

## Using LCEL[​](#using-lcel "Direct link to Using LCEL")

`BasePromptTemplate`, `BaseLanguageModel` and `BaseOutputParser` all implement the `Runnable` interface and are designed to be piped into one another, making LCEL composition very easy:

```python
from langchain.prompts import PromptTemplate  
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import StrOutputParser  
  
prompt = PromptTemplate.from\_template("What is a good name for a company that makes {product}?")  
runnable = prompt | ChatOpenAI() | StrOutputParser()  
runnable.invoke({"product": "colorful socks"})  

```

```text
 'VibrantSocks'  

```

Head to the [LCEL](/docs/expression_language) section for more on the interface, built-in features, and cookbook examples.

## \[Legacy\] LLMChain[​](#legacy-llmchain "Direct link to legacy-llmchain")

An `LLMChain` is a simple chain that adds some functionality around language models. It is used widely throughout LangChain, including in other chains and agents.

An `LLMChain` consists of a `PromptTemplate` and a language model (either an LLM or chat model). It formats the prompt template using the input key values provided (and also memory key values, if available), passes the formatted string to LLM and returns the LLM output.

### Get started[​](#get-started "Direct link to Get started")

```python
from langchain.prompts import PromptTemplate  
from langchain.llms import OpenAI  
from langchain.chains import LLMChain  
  
prompt\_template = "What is a good name for a company that makes {product}?"  
  
llm = OpenAI(temperature=0)  
llm\_chain = LLMChain(  
 llm=llm,  
 prompt=PromptTemplate.from\_template(prompt\_template)  
)  
llm\_chain("colorful socks")  

```

```text
 {'product': 'colorful socks', 'text': '\n\nSocktastic!'}  

```

### Additional ways of running `LLMChain`[​](#additional-ways-of-running-llmchain "Direct link to additional-ways-of-running-llmchain")

Aside from `__call__` and `run` methods shared by all `Chain` object, `LLMChain` offers a few more ways of calling the chain logic:

- `apply` allows you run the chain against a list of inputs:

```python
input\_list = [  
 {"product": "socks"},  
 {"product": "computer"},  
 {"product": "shoes"}  
]  
llm\_chain.apply(input\_list)  

```

```text
 [{'text': '\n\nSocktastic!'},  
 {'text': '\n\nTechCore Solutions.'},  
 {'text': '\n\nFootwear Factory.'}]  

```

- `generate` is similar to `apply`, except it return an `LLMResult` instead of string. `LLMResult` often contains useful generation such as token usages and finish reason.

```python
llm\_chain.generate(input\_list)  

```

```text
 LLMResult(generations=[[Generation(text='\n\nSocktastic!', generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text='\n\nTechCore Solutions.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})], [Generation(text='\n\nFootwear Factory.', generation\_info={'finish\_reason': 'stop', 'logprobs': None})]], llm\_output={'token\_usage': {'completion\_tokens': 19, 'prompt\_tokens': 36, 'total\_tokens': 55}, 'model\_name': 'text-davinci-003'}, run=[RunInfo(run\_id=UUID('9a423a43-6d35-4e8f-9aca-cacfc8e0dc49')), RunInfo(run\_id=UUID('a879c077-b521-461c-8f29-ba63adfc327c')), RunInfo(run\_id=UUID('40b892fa-e8c2-47d0-a309-4f7a4ed5b64a'))])  

```

- `predict` is similar to `run` method except that the input keys are specified as keyword arguments instead of a Python dict.

```python
# Single input example  
llm\_chain.predict(product="colorful socks")  

```

```text
 '\n\nSocktastic!'  

```

```python
# Multiple inputs example  
template = """Tell me a {adjective} joke about {subject}."""  
prompt = PromptTemplate(template=template, input\_variables=["adjective", "subject"])  
llm\_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0))  
  
llm\_chain.predict(adjective="sad", subject="ducks")  

```

```text
 '\n\nQ: What did the duck say when his friend died?\nA: Quack, quack, goodbye.'  

```

### Parsing the outputs[​](#parsing-the-outputs "Direct link to Parsing the outputs")

By default, `LLMChain` does not parse the output even if the underlying `prompt` object has an output parser. If you would like to apply that output parser on the LLM output, use `predict_and_parse` instead of `predict` and `apply_and_parse` instead of `apply`.

With `predict`:

```python
from langchain.output\_parsers import CommaSeparatedListOutputParser  
  
output\_parser = CommaSeparatedListOutputParser()  
template = """List all the colors in a rainbow"""  
prompt = PromptTemplate(template=template, input\_variables=[], output\_parser=output\_parser)  
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
llm\_chain.predict()  

```

```text
 '\n\nRed, orange, yellow, green, blue, indigo, violet'  

```

With `predict_and_parse`:

```python
llm\_chain.predict\_and\_parse()  

```

```text
 /Users/bagatur/langchain/libs/langchain/langchain/chains/llm.py:280: UserWarning: The predict\_and\_parse method is deprecated, instead pass an output parser directly to LLMChain.  
 warnings.warn(  
  
  
  
  
  
 ['Red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']  

```

### Initialize from string[​](#initialize-from-string "Direct link to Initialize from string")

You can also construct an `LLMChain` from a string template directly.

```python
template = """Tell me a {adjective} joke about {subject}."""  
llm\_chain = LLMChain.from\_string(llm=llm, template=template)  

```

```python
llm\_chain.predict(adjective="sad", subject="ducks")  

```

```text
 '\n\nQ: What did the duck say when his friend died?\nA: Quack, quack, goodbye.'  

```

- [Using LCEL](#using-lcel)
- [Legacy LLMChain](#legacy-llmchain)

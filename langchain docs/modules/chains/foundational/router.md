# Router

Routing allows you to create non-deterministic chains where the output of a previous step defines the next step. Routing helps provide structure and consistency around interactions with LLMs.

As a very simple example, let's suppose we have two templates optimized for different types of questions, and we want to choose the template based on the user input.

```python
from langchain.prompts import PromptTemplate  
  
  
physics\_template = """You are a very smart physics professor. \  
You are great at answering questions about physics in a concise and easy to understand manner. \  
When you don't know the answer to a question you admit that you don't know.  
  
Here is a question:  
{input}"""  
physics\_prompt = PromptTemplate.from\_template(physics\_template)  
  
math\_template = """You are a very good mathematician. You are great at answering math questions. \  
You are so good because you are able to break down hard problems into their component parts, \  
answer the component parts, and then put them together to answer the broader question.  
  
Here is a question:  
{input}"""  
math\_prompt = PromptTemplate.from\_template(math\_template)  

```

## Using LCEL[​](#using-lcel "Direct link to Using LCEL")

We can easily do this using a `RunnableBranch`. A `RunnableBranch` is initialized with a list of (condition, runnable) pairs and a default runnable. It selects which branch by passing each condition the input it's invoked with. It selects the first condition to evaluate to True, and runs the corresponding runnable to that condition with the input.

If no provided conditions match, it runs the default runnable.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.schema.output\_parser import StrOutputParser  
from langchain.schema.runnable import RunnableBranch  

```

```python
general\_prompt = PromptTemplate.from\_template(  
 "You are a helpful assistant. Answer the question as accurately as you can.\n\n{input}"  
)  
prompt\_branch = RunnableBranch(  
 (lambda x: x["topic"] == "math", math\_prompt),  
 (lambda x: x["topic"] == "physics", physics\_prompt),  
 general\_prompt  
)  

```

```python
from typing import Literal  
  
from langchain.pydantic\_v1 import BaseModel  
from langchain.output\_parsers.openai\_functions import PydanticAttrOutputFunctionsParser  
from langchain.utils.openai\_functions import convert\_pydantic\_to\_openai\_function  
  
  
class TopicClassifier(BaseModel):  
 "Classify the topic of the user question"  
   
 topic: Literal["math", "physics", "general"]  
 "The topic of the user question. One of 'math', 'phsyics' or 'general'."  
  
  
classifier\_function = convert\_pydantic\_to\_openai\_function(TopicClassifier)  
llm = ChatOpenAI().bind(functions=[classifier\_function], function\_call={"name": "TopicClassifier"})   
parser = PydanticAttrOutputFunctionsParser(pydantic\_schema=TopicClassifier, attr\_name="topic")  
classifier\_chain = llm | parser  

```

```python
from operator import itemgetter  
  
from langchain.schema.output\_parser import StrOutputParser  
from langchain.schema.runnable import RunnablePassthrough  
  
  
final\_chain = (  
 RunnablePassthrough.assign(topic=itemgetter("input") | classifier\_chain)   
 | prompt\_branch   
 | ChatOpenAI()  
 | StrOutputParser()  
)  

```

```python
final\_chain.invoke(  
 {"input": "What is the first prime number greater than 40 such that one plus the prime number is divisible by 3?"}  
)  

```

```text
 "Thank you for your kind words! I'll be happy to help you with this math question.\n\nTo find the first prime number greater than 40 that satisfies the given condition, we need to follow a step-by-step approach. \n\nFirstly, let's list the prime numbers greater than 40:\n41, 43, 47, 53, 59, 61, 67, 71, ...\n\nNow, we need to check if one plus each of these prime numbers is divisible by 3. We can do this by calculating the remainder when dividing each number by 3.\n\nFor 41, (41 + 1) % 3 = 42 % 3 = 0. It is divisible by 3.\n\nFor 43, (43 + 1) % 3 = 44 % 3 = 2. It is not divisible by 3.\n\nFor 47, (47 + 1) % 3 = 48 % 3 = 0. It is divisible by 3.\n\nSince 41 and 47 are both greater than 40 and satisfy the condition, the first prime number greater than 40 such that one plus the prime number is divisible by 3 is 41.\n\nTherefore, the answer to the question is 41."  

```

For more on routing with LCEL [head here](/docs/expression_language/how_to/routing).

## \[Legacy\] RouterChain[​](#legacy-routerchain "Direct link to legacy-routerchain")

Here we show how to use the `RouterChain` paradigm to create a chain that dynamically selects the next chain to use for a given input.

Router chains are made up of two components:

- The `RouterChain` itself (responsible for selecting the next chain to call)
- `destination_chains`: chains that the router chain can route to

In this example, we will focus on the different types of routing chains. We will show these routing chains used in a `MultiPromptChain` to create a question-answering chain that selects the prompt which is most relevant for a given question, and then answers the question using that prompt.

```python
from langchain.chains.router import MultiPromptChain  
from langchain.llms import OpenAI  
from langchain.chains import ConversationChain  
from langchain.chains.llm import LLMChain  

```

### \[Legacy\] LLMRouterChain[​](#legacy-llmrouterchain "Direct link to legacy-llmrouterchain")

This chain uses an LLM to determine how to route things.

```python
prompt\_infos = [  
 {  
 "name": "physics",  
 "description": "Good for answering questions about physics",  
 "prompt\_template": physics\_template,  
 },  
 {  
 "name": "math",  
 "description": "Good for answering math questions",  
 "prompt\_template": math\_template,  
 },  
]  

```

```python
llm = OpenAI()  

```

```python
destination\_chains = {}  
for p\_info in prompt\_infos:  
 name = p\_info["name"]  
 prompt\_template = p\_info["prompt\_template"]  
 prompt = PromptTemplate(template=prompt\_template, input\_variables=["input"])  
 chain = LLMChain(llm=llm, prompt=prompt)  
 destination\_chains[name] = chain  
default\_chain = ConversationChain(llm=llm, output\_key="text")  

```

```python
from langchain.chains.router.llm\_router import LLMRouterChain, RouterOutputParser  
from langchain.chains.router.multi\_prompt\_prompt import MULTI\_PROMPT\_ROUTER\_TEMPLATE  

```

```python
destinations = [f"{p['name']}: {p['description']}" for p in prompt\_infos]  
destinations\_str = "\n".join(destinations)  
router\_template = MULTI\_PROMPT\_ROUTER\_TEMPLATE.format(destinations=destinations\_str)  
router\_prompt = PromptTemplate(  
 template=router\_template,  
 input\_variables=["input"],  
 output\_parser=RouterOutputParser(),  
)  
router\_chain = LLMRouterChain.from\_llm(llm, router\_prompt)  

```

```python
chain = MultiPromptChain(  
 router\_chain=router\_chain,  
 destination\_chains=destination\_chains,  
 default\_chain=default\_chain,  
 verbose=True,  
)  

```

```python
print(chain.run("What is black body radiation?"))  

```

```text
   
   
 > Entering new MultiPromptChain chain...  
  
  
 /Users/bagatur/langchain/libs/langchain/langchain/chains/llm.py:280: UserWarning: The predict\_and\_parse method is deprecated, instead pass an output parser directly to LLMChain.  
 warnings.warn(  
  
  
 physics: {'input': 'What is black body radiation?'}  
 > Finished chain.  
   
   
 Black body radiation is the thermal electromagnetic radiation within or surrounding a body in thermodynamic equilibrium with its environment, or emitted by a black body (an idealized physical body which absorbs all incident electromagnetic radiation). It is a characteristic of the temperature of the body; if the body has a uniform temperature, the radiation is also uniform across the spectrum of frequencies. The spectral characteristics of the radiation are determined by the temperature of the body, which implies that a black body at a given temperature will emit the same amount of radiation at every frequency.  

```

```python
print(  
 chain.run(  
 "What is the first prime number greater than 40 such that one plus the prime number is divisible by 3?"  
 )  
)  

```

```text
   
   
 > Entering new MultiPromptChain chain...  
  
  
 /Users/bagatur/langchain/libs/langchain/langchain/chains/llm.py:280: UserWarning: The predict\_and\_parse method is deprecated, instead pass an output parser directly to LLMChain.  
 warnings.warn(  
  
  
 math: {'input': 'What is the first prime number greater than 40 such that one plus the prime number is divisible by 3?'}  
 > Finished chain.  
   
   
 The first prime number greater than 40 such that one plus the prime number is divisible by 3 is 43. This can be seen by breaking down the problem:  
   
 1) We know that a prime number is a number that is only divisible by itself and one.   
 2) We also know that if a number is divisible by 3, the sum of its digits must be divisible by 3.   
   
 So, if we want to find the first prime number greater than 40 such that one plus the prime number is divisible by 3, we can start counting up from 40, testing each number to see if it is prime and if the sum of the number and one is divisible by three.   
   
 The first number we come to that satisfies these conditions is 43.  

```

```python
print(chain.run("What is the name of the type of cloud that rains?"))  

```

```text
   
   
 > Entering new MultiPromptChain chain...  
  
  
 /Users/bagatur/langchain/libs/langchain/langchain/chains/llm.py:280: UserWarning: The predict\_and\_parse method is deprecated, instead pass an output parser directly to LLMChain.  
 warnings.warn(  
  
  
 physics: {'input': 'What is the name of the type of cloud that rains?'}  
 > Finished chain.  
   
   
 The type of cloud that rains is called a cumulonimbus cloud.  

```

## \[Legacy\] EmbeddingRouterChain[​](#legacy-embeddingrouterchain "Direct link to legacy-embeddingrouterchain")

The `EmbeddingRouterChain` uses embeddings and similarity to route between destination chains.

```python
from langchain.chains.router.embedding\_router import EmbeddingRouterChain  
from langchain.embeddings import CohereEmbeddings  
from langchain.vectorstores import Chroma  

```

```python
names\_and\_descriptions = [  
 ("physics", ["for questions about physics"]),  
 ("math", ["for questions about math"]),  
]  

```

```python
router\_chain = EmbeddingRouterChain.from\_names\_and\_descriptions(  
 names\_and\_descriptions, Chroma, CohereEmbeddings(), routing\_keys=["input"]  
)  

```

```python
chain = MultiPromptChain(  
 router\_chain=router\_chain,  
 destination\_chains=destination\_chains,  
 default\_chain=default\_chain,  
 verbose=True,  
)  

```

```python
print(chain.run("What is black body radiation?"))  

```

```text
   
   
 > Entering new MultiPromptChain chain...  
 physics: {'input': 'What is black body radiation?'}  
 > Finished chain.  
   
   
 Black body radiation is the electromagnetic radiation emitted by a black body, which is an idealized physical body that absorbs all incident electromagnetic radiation. This radiation is related to the temperature of the body, with higher temperatures leading to higher radiation levels. The spectrum of the radiation is continuous, and is described by the Planck's law of black body radiation.  

```

```python
print(  
 chain.run(  
 "What is the first prime number greater than 40 such that one plus the prime number is divisible by 3?"  
 )  
)  

```

```text
   
   
 > Entering new MultiPromptChain chain...  
 math: {'input': 'What is the first prime number greater than 40 such that one plus the prime number is divisible by 3?'}  
 > Finished chain.  
   
   
 The first prime number greater than 40 such that one plus the prime number is divisible by 3 is 43. This is because 43 is a prime number, and 1 + 43 = 44, which is divisible by 3.  

```

- [Using LCEL](#using-lcel)
- [Legacy RouterChain](#legacy-routerchain)

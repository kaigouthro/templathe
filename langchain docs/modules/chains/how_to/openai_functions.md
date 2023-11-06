# Using OpenAI functions

This walkthrough demonstrates how to incorporate OpenAI function-calling API's in a chain. We'll go over:

1. How to use functions to get structured outputs from ChatOpenAI
1. How to create a generic chain that uses (multiple) functions
1. How to create a chain that actually executes the chosen function

```python
from typing import Optional  
  
from langchain.chains.openai\_functions import (  
 create\_openai\_fn\_chain,  
 create\_structured\_output\_chain,  
)  
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate  

```

## Getting structured outputs[​](#getting-structured-outputs "Direct link to Getting structured outputs")

We can take advantage of OpenAI functions to try and force the model to return a particular kind of structured output. We'll use `create_structured_output_chain` to create our chain, which takes the desired structured output either as a Pydantic class or as JsonSchema.

See here for relevant [reference docs](https://api.python.langchain.com/en/latest/chains/langchain.chains.openai_functions.base.create_structured_output_chain.html).

### Using Pydantic classes[​](#using-pydantic-classes "Direct link to Using Pydantic classes")

When passing in Pydantic classes to structure our text, we need to make sure to have a docstring description for the class. It also helps to have descriptions for each of the classes attributes.

```python
from langchain.pydantic\_v1 import BaseModel, Field  
  
  
class Person(BaseModel):  
 """Identifying information about a person."""  
  
 name: str = Field(..., description="The person's name")  
 age: int = Field(..., description="The person's age")  
 fav\_food: Optional[str] = Field(None, description="The person's favorite food")  

```

```python
# If we pass in a model explicitly, we need to make sure it supports the OpenAI function-calling API.  
llm = ChatOpenAI(model="gpt-4", temperature=0)  
prompt = ChatPromptTemplate.from\_messages(  
 [  
 ("system", "You are a world class algorithm for extracting information in structured formats."),  
 ("human", "Use the given format to extract information from the following input: {input}"),  
 ("human", "Tip: Make sure to answer in the correct format"),  
 ]  
)  
  
chain = create\_structured\_output\_chain(Person, llm, prompt, verbose=True)  
chain.run("Sally is 13")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 System: You are a world class algorithm for extracting information in structured formats.  
 Human: Use the given format to extract information from the following input: Sally is 13  
 Human: Tip: Make sure to answer in the correct format  
   
 > Finished chain.  
  
  
  
  
  
 Person(name='Sally', age=13, fav\_food='Unknown')  

```

To extract arbitrarily many structured outputs of a given format, we can just create a wrapper Pydantic class that takes a sequence of the original class.

```python
from typing import Sequence  
  
  
class People(BaseModel):  
 """Identifying information about all people in a text."""  
  
 people: Sequence[Person] = Field(..., description="The people in the text")  
  
  
chain = create\_structured\_output\_chain(People, llm, prompt, verbose=True)  
chain.run(  
 "Sally is 13, Joey just turned 12 and loves spinach. Caroline is 10 years older than Sally."  
)  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 System: You are a world class algorithm for extracting information in structured formats.  
 Human: Use the given format to extract information from the following input: Sally is 13, Joey just turned 12 and loves spinach. Caroline is 10 years older than Sally.  
 Human: Tip: Make sure to answer in the correct format  
   
 > Finished chain.  
  
  
  
  
  
 People(people=[Person(name='Sally', age=13, fav\_food=''), Person(name='Joey', age=12, fav\_food='spinach'), Person(name='Caroline', age=23, fav\_food='')])  

```

### Using JsonSchema[​](#using-jsonschema "Direct link to Using JsonSchema")

We can also pass in JsonSchema instead of Pydantic classes to specify the desired structure. When we do this, our chain will output JSON corresponding to the properties described in the JsonSchema, instead of a Pydantic class.

```python
json\_schema = {  
 "title": "Person",  
 "description": "Identifying information about a person.",  
 "type": "object",  
 "properties": {  
 "name": {"title": "Name", "description": "The person's name", "type": "string"},  
 "age": {"title": "Age", "description": "The person's age", "type": "integer"},  
 "fav\_food": {  
 "title": "Fav Food",  
 "description": "The person's favorite food",  
 "type": "string",  
 },  
 },  
 "required": ["name", "age"],  
}  

```

```python
chain = create\_structured\_output\_chain(json\_schema, llm, prompt, verbose=True)  
chain.run("Sally is 13")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 System: You are a world class algorithm for extracting information in structured formats.  
 Human: Use the given format to extract information from the following input: Sally is 13  
 Human: Tip: Make sure to answer in the correct format  
   
 > Finished chain.  
  
  
  
  
  
 {'name': 'Sally', 'age': 13}  

```

## Creating a generic OpenAI functions chain[​](#creating-a-generic-openai-functions-chain "Direct link to Creating a generic OpenAI functions chain")

To create a generic OpenAI functions chain, we can use the `create_openai_fn_chain` method. This is the same as `create_structured_output_chain` except that instead of taking a single output schema, it takes a sequence of function definitions.

Functions can be passed in as:

- dicts conforming to OpenAI functions spec,
- Pydantic classes, in which case they should have docstring descriptions of the function they represent and descriptions for each of the parameters,
- Python functions, in which case they should have docstring descriptions of the function and args, along with type hints.

See here for relevant [reference docs](https://api.python.langchain.com/en/latest/chains/langchain.chains.openai_functions.base.create_openai_fn_chain.html).

### Using Pydantic classes[​](#using-pydantic-classes-1 "Direct link to Using Pydantic classes")

```python
class RecordPerson(BaseModel):  
 """Record some identifying information about a pe."""  
  
 name: str = Field(..., description="The person's name")  
 age: int = Field(..., description="The person's age")  
 fav\_food: Optional[str] = Field(None, description="The person's favorite food")  
  
  
class RecordDog(BaseModel):  
 """Record some identifying information about a dog."""  
  
 name: str = Field(..., description="The dog's name")  
 color: str = Field(..., description="The dog's color")  
 fav\_food: Optional[str] = Field(None, description="The dog's favorite food")  

```

```python
prompt = ChatPromptTemplate.from\_messages(  
 [  
 ("system", "You are a world class algorithm for recording entities."),  
 ("human", "Make calls to the relevant function to record the entities in the following input: {input}"),  
 ("human", "Tip: Make sure to answer in the correct format"),  
 ]  
)  
  
chain = create\_openai\_fn\_chain([RecordPerson, RecordDog], llm, prompt, verbose=True)  
chain.run("Harry was a chubby brown beagle who loved chicken")  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 System: You are a world class algorithm for recording entities.  
 Human: Make calls to the relevant function to record the entities in the following input: Harry was a chubby brown beagle who loved chicken  
 Human: Tip: Make sure to answer in the correct format  
   
 > Finished chain.  
  
  
  
  
  
 RecordDog(name='Harry', color='brown', fav\_food='chicken')  

```

### Using Python functions[​](#using-python-functions "Direct link to Using Python functions")

We can pass in functions as Pydantic classes, directly as OpenAI function dicts, or Python functions. To pass Python function in directly, we'll want to make sure our parameters have type hints, we have a docstring, and we use [Google Python style docstrings](https://google.github.io/styleguide/pyguide.html#doc-function-args) to describe the parameters.

**NOTE**: To use Python functions, make sure the function arguments are of primitive types (str, float, int, bool) or that they are Pydantic objects.

```python
class OptionalFavFood(BaseModel):  
 """Either a food or null."""  
  
 food: Optional[str] = Field(  
 None,  
 description="Either the name of a food or null. Should be null if the food isn't known.",  
 )  
  
  
def record\_person(name: str, age: int, fav\_food: OptionalFavFood) -> str:  
 """Record some basic identifying information about a person.  
  
 Args:  
 name: The person's name.  
 age: The person's age in years.  
 fav\_food: An OptionalFavFood object that either contains the person's favorite food or a null value. Food should be null if it's not known.  
 """  
 return f"Recording person {name} of age {age} with favorite food {fav\_food.food}!"  
  
  
chain = create\_openai\_fn\_chain([record\_person], llm, prompt, verbose=True)  
chain.run(  
 "The most important thing to remember about Tommy, my 12 year old, is that he'll do anything for apple pie."  
)  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 System: You are a world class algorithm for recording entities.  
 Human: Make calls to the relevant function to record the entities in the following input: The most important thing to remember about Tommy, my 12 year old, is that he'll do anything for apple pie.  
 Human: Tip: Make sure to answer in the correct format  
   
 > Finished chain.  
  
  
  
  
  
 {'name': 'Tommy', 'age': 12, 'fav\_food': {'food': 'apple pie'}}  

```

If we pass in multiple Python functions or OpenAI functions, then the returned output will be of the form:

```python
{"name": "<<function\_name>>", "arguments": {<<function\_arguments>>}}  

```

```python
def record\_dog(name: str, color: str, fav\_food: OptionalFavFood) -> str:  
 """Record some basic identifying information about a dog.  
  
 Args:  
 name: The dog's name.  
 color: The dog's color.  
 fav\_food: An OptionalFavFood object that either contains the dog's favorite food or a null value. Food should be null if it's not known.  
 """  
 return f"Recording dog {name} of color {color} with favorite food {fav\_food}!"  
  
  
chain = create\_openai\_fn\_chain([record\_person, record\_dog], llm, prompt, verbose=True)  
chain.run(  
 "I can't find my dog Henry anywhere, he's a small brown beagle. Could you send a message about him?"  
)  

```

```text
   
   
 > Entering new LLMChain chain...  
 Prompt after formatting:  
 System: You are a world class algorithm for recording entities.  
 Human: Make calls to the relevant function to record the entities in the following input: I can't find my dog Henry anywhere, he's a small brown beagle. Could you send a message about him?  
 Human: Tip: Make sure to answer in the correct format  
   
 > Finished chain.  
  
  
  
  
  
 {'name': 'record\_dog',  
 'arguments': {'name': 'Henry', 'color': 'brown', 'fav\_food': {'food': None}}}  

```

## Other Chains using OpenAI functions[​](#other-chains-using-openai-functions "Direct link to Other Chains using OpenAI functions")

There are a number of more specific chains that use OpenAI functions.

- [Extraction](/docs/modules/chains/additional/extraction): very similar to structured output chain, intended for information/entity extraction specifically.

- [Tagging](/docs/use_cases/tagging): tag inputs.

- [OpenAPI](/docs/use_cases/apis/openapi_openai): take an OpenAPI spec and create + execute valid requests against the API, using OpenAI functions under the hood.

- [QA with citations](/docs/use_cases/question_answering/qa_citations): use OpenAI functions ability to extract citations from text.

- [Getting structured outputs](#getting-structured-outputs)

  - [Using Pydantic classes](#using-pydantic-classes)
  - [Using JsonSchema](#using-jsonschema)

- [Creating a generic OpenAI functions chain](#creating-a-generic-openai-functions-chain)

  - [Using Pydantic classes](#using-pydantic-classes-1)
  - [Using Python functions](#using-python-functions)

- [Other Chains using OpenAI functions](#other-chains-using-openai-functions)

- [Using Pydantic classes](#using-pydantic-classes)

- [Using JsonSchema](#using-jsonschema)

- [Using Pydantic classes](#using-pydantic-classes-1)

- [Using Python functions](#using-python-functions)

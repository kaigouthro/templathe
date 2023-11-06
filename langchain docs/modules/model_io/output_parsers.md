# Output parsers

Language models output text. But many times you may want to get more structured information than just text back. This is where output parsers come in.

Output parsers are classes that help structure language model responses. There are two main methods an output parser must implement:

- "Get format instructions": A method which returns a string containing instructions for how the output of a language model should be formatted.
- "Parse": A method which takes in a string (assumed to be the response from a language model) and parses it into some structure.

And then one optional one:

- "Parse with prompt": A method which takes in a string (assumed to be the response from a language model) and a prompt (assumed to be the prompt that generated such a response) and parses it into some structure. The prompt is largely provided in the event the OutputParser wants to retry or fix the output in some way, and needs information from the prompt to do so.

## Get started[​](#get-started "Direct link to Get started")

Below we go over the main type of output parser, the `PydanticOutputParser`.

```python
from typing import List  
  
from langchain.llms import OpenAI  
from langchain.output\_parsers import PydanticOutputParser  
from langchain.prompts import PromptTemplate  
from langchain.pydantic\_v1 import BaseModel, Field, validator  
  
  
model = OpenAI(model\_name='text-davinci-003', temperature=0.0)  
  
# Define your desired data structure.  
class Joke(BaseModel):  
 setup: str = Field(description="question to set up a joke")  
 punchline: str = Field(description="answer to resolve the joke")  
  
 # You can add custom validation logic easily with Pydantic.  
 @validator('setup')  
 def question\_ends\_with\_question\_mark(cls, field):  
 if field[-1] != '?':  
 raise ValueError("Badly formed question!")  
 return field  
  
# Set up a parser + inject instructions into the prompt template.  
parser = PydanticOutputParser(pydantic\_object=Joke)  
  
prompt = PromptTemplate(  
 template="Answer the user query.\n{format\_instructions}\n{query}\n",  
 input\_variables=["query"],  
 partial\_variables={"format\_instructions": parser.get\_format\_instructions()}  
)  
  
# And a query intended to prompt a language model to populate the data structure.  
prompt\_and\_model = prompt | model  
output = prompt\_and\_model.invoke({"query": "Tell me a joke."})  
parser.invoke(output)  

```

```text
 Joke(setup='Why did the chicken cross the road?', punchline='To get to the other side!')  

```

## LCEL[​](#lcel "Direct link to LCEL")

Output parsers implement the [Runnable interface](/docs/expression_language/interface), the basic building block of the [LangChain Expression Language (LCEL)](/docs/expression_language/). This means they support `invoke`, `ainvoke`, `stream`, `astream`, `batch`, `abatch`, `astream_log` calls.

Output parsers accept a string or `BaseMessage` as input and can return an arbitrary type.

```python
parser.invoke(output)  

```

```text
 Joke(setup='Why did the chicken cross the road?', punchline='To get to the other side!')  

```

Instead of manually invoking the parser, we also could've just added it to our `Runnable` sequence:

```python
chain = prompt | model | parser  
chain.invoke({"query": "Tell me a joke."})  

```

```text
 Joke(setup='Why did the chicken cross the road?', punchline='To get to the other side!')  

```

While all parsers support the streaming interface, only certain parsers can stream through partially parsed objects, since this is highly dependent on the output type. Parsers which cannot construct partial objects will simply yield the fully parsed output.

The `SimpleJsonOutputParser` for example can stream through partial outputs:

```python
from langchain.output\_parsers.json import SimpleJsonOutputParser  
  
json\_prompt = PromptTemplate.from\_template("Return a JSON object with an `answer` key that answers the following question: {question}")  
json\_parser = SimpleJsonOutputParser()  
json\_chain = json\_prompt | model | json\_parser  

```

```python
list(json\_chain.stream({"question": "Who invented the microscope?"}))  

```

```text
 [{},  
 {'answer': ''},  
 {'answer': 'Ant'},  
 {'answer': 'Anton'},  
 {'answer': 'Antonie'},  
 {'answer': 'Antonie van'},  
 {'answer': 'Antonie van Lee'},  
 {'answer': 'Antonie van Leeu'},  
 {'answer': 'Antonie van Leeuwen'},  
 {'answer': 'Antonie van Leeuwenho'},  
 {'answer': 'Antonie van Leeuwenhoek'}]  

```

While the PydanticOutputParser cannot:

```python
list(chain.stream({"query": "Tell me a joke."}))  

```

```text
 [Joke(setup='Why did the chicken cross the road?', punchline='To get to the other side!')]  

```

- [Get started](#get-started)
- [LCEL](#lcel)

# LangChain Decorators ✨

lanchchain decorators is a layer on the top of LangChain that provides syntactic sugar 🍭 for writing custom langchain prompts and chains

For Feedback, Issues, Contributions - please raise an issue here:
[ju-bezdek/langchain-decorators](https://github.com/ju-bezdek/langchain-decorators)

Main principles and benefits:

- more `pythonic` way of writing code
- write multiline prompts that won't break your code flow with indentation
- making use of IDE in-built support for **hinting**, **type checking** and **popup with docs** to quickly peek in the function to see the prompt, parameters it consumes etc.
- leverage all the power of 🦜🔗 LangChain ecosystem
- adding support for **optional parameters**
- easily share parameters between the prompts by binding them to one class

Here is a simple example of a code written with **LangChain Decorators ✨**

```python
  
@llm\_prompt  
def write\_me\_short\_post(topic:str, platform:str="twitter", audience:str = "developers")->str:  
 """  
 Write me a short header for my post about {topic} for {platform} platform.   
 It should be for {audience} audience.  
 (Max 15 words)  
 """  
 return  
  
# run it naturally  
write\_me\_short\_post(topic="starwars")  
# or  
write\_me\_short\_post(topic="starwars", platform="redit")  

```

# Quick start

## Installation[​](#installation "Direct link to Installation")

```bash
pip install langchain\_decorators  

```

## Examples[​](#examples "Direct link to Examples")

Good idea on how to start is to review the examples here:

- [jupyter notebook](https://github.com/ju-bezdek/langchain-decorators/blob/main/example_notebook.ipynb)
- [colab notebook](https://colab.research.google.com/drive/1no-8WfeP6JaLD9yUtkPgym6x0G9ZYZOG#scrollTo=N4cf__D0E2Yk)

# Defining other parameters

Here we are just marking a function as a prompt with `llm_prompt` decorator, turning it effectively into a LLMChain. Instead of running it

Standard LLMchain takes much more init parameter than just inputs_variables and prompt... here is this implementation detail hidden in the decorator.
Here is how it works:

1. Using **Global settings**:

```python
# define global settings for all prompty (if not set - chatGPT is the current default)  
from langchain\_decorators import GlobalSettings  
  
GlobalSettings.define\_settings(  
 default\_llm=ChatOpenAI(temperature=0.0), this is default... can change it here globally  
 default\_streaming\_llm=ChatOpenAI(temperature=0.0,streaming=True), this is default... can change it here for all ... will be used for streaming  
)  

```

2. Using predefined **prompt types**

```python
#You can change the default prompt types  
from langchain\_decorators import PromptTypes, PromptTypeSettings  
  
PromptTypes.AGENT\_REASONING.llm = ChatOpenAI()  
  
# Or you can just define your own ones:  
class MyCustomPromptTypes(PromptTypes):  
 GPT4=PromptTypeSettings(llm=ChatOpenAI(model="gpt-4"))  
  
@llm\_prompt(prompt\_type=MyCustomPromptTypes.GPT4)   
def write\_a\_complicated\_code(app\_idea:str)->str:  
 ...  
  

```

3. Define the settings **directly in the decorator**

```python
from langchain.llms import OpenAI  
  
@llm\_prompt(  
 llm=OpenAI(temperature=0.7),  
 stop\_tokens=["\nObservation"],  
 ...  
 )  
def creative\_writer(book\_title:str)->str:  
 ...  

```

## Passing a memory and/or callbacks:[​](#passing-a-memory-andor-callbacks "Direct link to Passing a memory and/or callbacks:")

To pass any of these, just declare them in the function (or use kwargs to pass anything)

```python
  
@llm\_prompt()  
async def write\_me\_short\_post(topic:str, platform:str="twitter", memory:SimpleMemory = None):  
 """  
 {history\_key}  
 Write me a short header for my post about {topic} for {platform} platform.   
 It should be for {audience} audience.  
 (Max 15 words)  
 """  
 pass  
  
await write\_me\_short\_post(topic="old movies")  
  

```

# Simplified streaming

If we want to leverage streaming:

- we need to define prompt as async function
- turn on the streaming on the decorator, or we can define PromptType with streaming on
- capture the stream using StreamingContext

This way we just mark which prompt should be streamed, not needing to tinker with what LLM should we use, passing around the creating and distribute streaming handler into particular part of our chain... just turn the streaming on/off on prompt/prompt type...

The streaming will happen only if we call it in streaming context ... there we can define a simple function to handle the stream

```python
# this code example is complete and should run as it is  
  
from langchain\_decorators import StreamingContext, llm\_prompt  
  
# this will mark the prompt for streaming (useful if we want stream just some prompts in our app... but don't want to pass distribute the callback handlers)  
# note that only async functions can be streamed (will get an error if it's not)  
@llm\_prompt(capture\_stream=True)   
async def write\_me\_short\_post(topic:str, platform:str="twitter", audience:str = "developers"):  
 """  
 Write me a short header for my post about {topic} for {platform} platform.   
 It should be for {audience} audience.  
 (Max 15 words)  
 """  
 pass  
  
  
  
# just an arbitrary function to demonstrate the streaming... will be some websockets code in the real world  
tokens=[]  
def capture\_stream\_func(new\_token:str):  
 tokens.append(new\_token)  
  
# if we want to capture the stream, we need to wrap the execution into StreamingContext...   
# this will allow us to capture the stream even if the prompt call is hidden inside higher level method  
# only the prompts marked with capture\_stream will be captured here  
with StreamingContext(stream\_to\_stdout=True, callback=capture\_stream\_func):  
 result = await run\_prompt()  
 print("Stream finished ... we can distinguish tokens thanks to alternating colors")  
  
  
print("\nWe've captured",len(tokens),"tokens🎉\n")  
print("Here is the result:")  
print(result)  

```

# Prompt declarations

By default the prompt is is the whole function docs, unless you mark your prompt

## Documenting your prompt[​](#documenting-your-prompt "Direct link to Documenting your prompt")

We can specify what part of our docs is the prompt definition, by specifying a code block with `<prompt>` language tag

````python
@llm\_prompt  
def write\_me\_short\_post(topic:str, platform:str="twitter", audience:str = "developers"):  
 """  
 Here is a good way to write a prompt as part of a function docstring, with additional documentation for devs.  
  
 It needs to be a code block, marked as a `<prompt>` language  
 ```<prompt>  
 Write me a short header for my post about {topic} for {platform} platform.   
 It should be for {audience} audience.  
 (Max 15 words)  
````

Now only to code block above will be used as a prompt, and the rest of the docstring will be used as a description for developers.\
(It has also a nice benefit that IDE (like VS code) will display the prompt properly (not trying to parse it as markdown, and thus not showing new lines properly))\
"""\
return

````


Chat messages prompt[​](#chat-messages-prompt "Direct link to Chat messages prompt")
------------------------------------------------------------------------------------



For chat models is very useful to define prompt as a set of message templates... here is how to do it:




```python
@llm\_prompt  
def simulate\_conversation(human\_input:str, agent\_role:str="a pirate"):  
 """  
 ## System message  
 - note the `:system` sufix inside the <prompt:\_role\_> tag  
   
  
 ```<prompt:system>  
 You are a {agent\_role} hacker. You mus act like one.  
 You reply always in code, using python or javascript code block...  
 for example:  
   
 ... do not reply with anything else.. just with code - respecting your role.  
````

# human message

(we are using the real role that are enforced by the LLM - GPT supports system, assistant, user)

```<prompt:user>
Helo, who are you  
```

a reply:

````<prompt:assistant>
\``` python <<- escaping inner code block with \ that should be part of the prompt  
def hello():  
print("Argh... hello you pesky pirate")  
\```  
````

we can also add some history using placeholder

```<prompt:placeholder>
{history}  
```

```<prompt:user>
{human\_input}  
```

Now only to code block above will be used as a prompt, and the rest of the docstring will be used as a description for developers.\
(It has also a nice benefit that IDE (like VS code) will display the prompt properly (not trying to parse it as markdown, and thus not showing new lines properly))\
"""\
pass

````


the roles here are model native roles (assistant, user, system for chatGPT)



Optional sections
=================



* you can define a whole sections of your prompt that should be optional
* if any input in the section is missing, the whole section won't be rendered


the syntax for this is as follows:




```python
@llm\_prompt  
def prompt\_with\_optional\_partials():  
 """  
 this text will be rendered always, but  
  
 {? anything inside this block will be rendered only if all the {value}s parameters are not empty (None | "") ?}  
  
 you can also place it in between the words  
 this too will be rendered{? , but  
 this block will be rendered only if {this\_value} and {this\_value}  
 is not empty?} !  
 """  

````

# Output parsers

- llm_prompt decorator natively tries to detect the best output parser based on the output type. (if not set, it returns the raw string)
- list, dict and pydantic outputs are also supported natively (automatically)

```python
# this code example is complete and should run as it is  
  
from langchain\_decorators import llm\_prompt  
  
@llm\_prompt  
def write\_name\_suggestions(company\_business:str, count:int)->list:  
 """ Write me {count} good name suggestions for company that {company\_business}  
 """  
 pass  
  
write\_name\_suggestions(company\_business="sells cookies", count=5)  

```

## More complex structures[​](#more-complex-structures "Direct link to More complex structures")

for dict / pydantic you need to specify the formatting instructions...
this can be tedious, that's why you can let the output parser gegnerate you the instructions based on the model (pydantic)

```python
from langchain\_decorators import llm\_prompt  
from pydantic import BaseModel, Field  
  
  
class TheOutputStructureWeExpect(BaseModel):  
 name:str = Field (description="The name of the company")  
 headline:str = Field( description="The description of the company (for landing page)")  
 employees:list[str] = Field(description="5-8 fake employee names with their positions")  
  
@llm\_prompt()  
def fake\_company\_generator(company\_business:str)->TheOutputStructureWeExpect:  
 """ Generate a fake company that {company\_business}  
 {FORMAT\_INSTRUCTIONS}  
 """  
 return  
  
company = fake\_company\_generator(company\_business="sells cookies")  
  
# print the result nicely formatted  
print("Company name: ",company.name)  
print("company headline: ",company.headline)  
print("company employees: ",company.employees)  
  

```

# Binding the prompt to an object

````python
from pydantic import BaseModel  
from langchain\_decorators import llm\_prompt  
  
class AssistantPersonality(BaseModel):  
 assistant\_name:str  
 assistant\_role:str  
 field:str  
  
 @property  
 def a\_property(self):  
 return "whatever"  
  
 def hello\_world(self, function\_kwarg:str=None):  
 """  
 We can reference any {field} or {a\_property} inside our prompt... and combine it with {function\_kwarg} in the method  
 """  
  
   
 @llm\_prompt  
 def introduce\_your\_self(self)->str:  
 """  
 ``` <prompt:system>  
 You are an assistant named {assistant\_name}.   
 Your role is to act as {assistant\_role}  
````

```<prompt:user>
Introduce your self (in less than 20 words)  
```

"""

personality = AssistantPersonality(assistant_name="John", assistant_role="a pirate")

print(personality.introduce_your_self(personality))

```


More examples:
==============



* these and few more examples are also available in the [colab notebook here](https://colab.research.google.com/drive/1no-8WfeP6JaLD9yUtkPgym6x0G9ZYZOG#scrollTo=N4cf__D0E2Yk)
* including the [ReAct Agent re-implementation](https://colab.research.google.com/drive/1no-8WfeP6JaLD9yUtkPgym6x0G9ZYZOG#scrollTo=3bID5fryE2Yp) using purely langchain decorators


* [Installation](#installation)
* [Examples](#examples)
* [Passing a memory and/or callbacks:](#passing-a-memory-andor-callbacks)
* [Documenting your prompt](#documenting-your-prompt)
* [Chat messages prompt](#chat-messages-prompt)
* [More complex structures](#more-complex-structures)

```

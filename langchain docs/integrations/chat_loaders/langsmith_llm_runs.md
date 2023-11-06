# Fine-Tuning on LangSmith LLM Runs

This notebook demonstrates how to directly load data from LangSmith's LLM runs and fine-tune a model on that data.
The process is simple and comprises 3 steps.

1. Select the LLM runs to train on.
1. Use the LangSmithRunChatLoader to load runs as chat sessions.
1. Fine-tune your model.

Then you can use the fine-tuned model in your LangChain app.

Before diving in, let's install our prerequisites.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Ensure you've installed langchain >= 0.0.311 and have configured your environment with your LangSmith API key.

```python
%pip install -U langchain openai  

```

```python
import os  
import uuid  
uid = uuid.uuid4().hex[:6]  
project\_name = f"Run Fine-tuning Walkthrough {uid}"  
os.environ["LANGCHAIN\_TRACING\_V2"] = "true"  
os.environ["LANGCHAIN\_API\_KEY"] = "YOUR API KEY"  
os.environ["LANGCHAIN\_PROJECT"] = project\_name  

```

1. Select Runs[​](#1-select-runs "Direct link to 1. Select Runs")

______________________________________________________________________

The first step is selecting which runs to fine-tune on. A common case would be to select LLM runs within
traces that have received positive user feedback. You can find examples of this in the[LangSmith Cookbook](https://github.com/langchain-ai/langsmith-cookbook/blob/main/exploratory-data-analysis/exporting-llm-runs-and-feedback/llm_run_etl.ipynb) and in the [docs](https://docs.smith.langchain.com/tracing/use-cases/export-runs/local).

For the sake of this tutorial, we will generate some runs for you to use here. Let's try fine-tuning a
simple function-calling chain.

```python
from langchain.pydantic\_v1 import BaseModel, Field  
from enum import Enum  
  
  
class Operation(Enum):  
 add = "+"  
 subtract = "-"  
 multiply = "\*"  
 divide = "/"  
  
class Calculator(BaseModel):  
 """A calculator function"""  
 num1: float  
 num2: float  
 operation: Operation = Field(..., description="+,-,\*,/")  
  
 def calculate(self):  
 if self.operation == Operation.add:  
 return self.num1 + self.num2  
 elif self.operation == Operation.subtract:  
 return self.num1 - self.num2  
 elif self.operation == Operation.multiply:  
 return self.num1 \* self.num2  
 elif self.operation == Operation.divide:  
 if self.num2 != 0:  
 return self.num1 / self.num2  
 else:  
 return "Cannot divide by zero"  

```

```python
from langchain.utils.openai\_functions import convert\_pydantic\_to\_openai\_function  
from langchain.pydantic\_v1 import BaseModel  
from pprint import pprint  
  
openai\_function\_def = convert\_pydantic\_to\_openai\_function(Calculator)  
pprint(openai\_function\_def)  

```

```text
 {'description': 'A calculator function',  
 'name': 'Calculator',  
 'parameters': {'description': 'A calculator function',  
 'properties': {'num1': {'title': 'Num1', 'type': 'number'},  
 'num2': {'title': 'Num2', 'type': 'number'},  
 'operation': {'allOf': [{'description': 'An '  
 'enumeration.',  
 'enum': ['+',  
 '-',  
 '\*',  
 '/'],  
 'title': 'Operation'}],  
 'description': '+,-,\*,/'}},  
 'required': ['num1', 'num2', 'operation'],  
 'title': 'Calculator',  
 'type': 'object'}}  

```

```python
from langchain.prompts import ChatPromptTemplate  
from langchain.chat\_models import ChatOpenAI  
from langchain.output\_parsers.openai\_functions import PydanticOutputFunctionsParser  
  
prompt = ChatPromptTemplate.from\_messages(  
 [  
 ("system", "You are an accounting assistant."),  
 ("user", "{input}"),  
 ]  
)  
chain = (  
 prompt  
 | ChatOpenAI().bind(functions=[openai\_function\_def])  
 | PydanticOutputFunctionsParser(pydantic\_schema=Calculator)  
 | (lambda x: x.calculate())  
)  

```

```python
math\_questions = [  
 "What's 45/9?",  
 "What's 81/9?",  
 "What's 72/8?",  
 "What's 56/7?",  
 "What's 36/6?",  
 "What's 64/8?",  
 "What's 12\*6?",  
 "What's 8\*8?",  
 "What's 10\*10?",  
 "What's 11\*11?",  
 "What's 13\*13?",  
 "What's 45+30?",  
 "What's 72+28?",  
 "What's 56+44?",  
 "What's 63+37?",  
 "What's 70-35?",  
 "What's 60-30?",  
 "What's 50-25?",  
 "What's 40-20?",  
 "What's 30-15?"  
]  
results = chain.batch([{"input": q} for q in math\_questions], return\_exceptions=True)  

```

```text
 Retrying langchain.chat\_models.openai.ChatOpenAI.completion\_with\_retry.<locals>.\_completion\_with\_retry in 4.0 seconds as it raised ServiceUnavailableError: The server is overloaded or not ready yet..  

```

#### Load runs that did not error[​](#load-runs-that-did-not-error "Direct link to Load runs that did not error")

Now we can select the successful runs to fine-tune on.

```python
from langsmith.client import Client  
  
client = Client()  

```

```python
successful\_traces = {  
 run.trace\_id  
 for run in client.list\_runs(  
 project\_name=project\_name,  
 execution\_order=1,  
 error=False,  
 )  
}  
   
llm\_runs = [  
 run for run in client.list\_runs(  
 project\_name=project\_name,  
 run\_type="llm",  
 )   
 if run.trace\_id in successful\_traces  
]  

```

2. Prepare data[​](#2-prepare-data "Direct link to 2. Prepare data")

______________________________________________________________________

Now we can create an instance of LangSmithRunChatLoader and load the chat sessions using its lazy_load() method.

```python
from langchain.chat\_loaders.langsmith import LangSmithRunChatLoader  
  
loader = LangSmithRunChatLoader(runs=llm\_runs)  
  
chat\_sessions = loader.lazy\_load()  

```

#### With the chat sessions loaded, convert them into a format suitable for fine-tuning.[​](#with-the-chat-sessions-loaded-convert-them-into-a-format-suitable-for-fine-tuning "Direct link to With the chat sessions loaded, convert them into a format suitable for fine-tuning.")

```python
from langchain.adapters.openai import convert\_messages\_for\_finetuning  
  
training\_data = convert\_messages\_for\_finetuning(chat\_sessions)  

```

3. Fine-tune the model[​](#3-fine-tune-the-model "Direct link to 3. Fine-tune the model")

______________________________________________________________________

Now, initiate the fine-tuning process using the OpenAI library.

```python
import openai  
import time  
import json  
from io import BytesIO  
  
my\_file = BytesIO()  
for dialog in training\_data:  
 my\_file.write((json.dumps({"messages": dialog}) + "\n").encode('utf-8'))  
  
my\_file.seek(0)  
training\_file = openai.File.create(  
 file=my\_file,  
 purpose='fine-tune'  
)  
  
job = openai.FineTuningJob.create(  
 training\_file=training\_file.id,  
 model="gpt-3.5-turbo",  
)  
  
# Wait for the fine-tuning to complete (this may take some time)  
status = openai.FineTuningJob.retrieve(job.id).status  
start\_time = time.time()  
while status != "succeeded":  
 print(f"Status=[{status}]... {time.time() - start\_time:.2f}s", end="\r", flush=True)  
 time.sleep(5)  
 status = openai.FineTuningJob.retrieve(job.id).status  
  
# Now your model is fine-tuned!  

```

```text
 Status=[running]... 346.26s. 31.70s  

```

4. Use in LangChain[​](#4-use-in-langchain "Direct link to 4. Use in LangChain")

______________________________________________________________________

After fine-tuning, use the resulting model ID with the ChatOpenAI model class in your LangChain app.

```python
# Get the fine-tuned model ID  
job = openai.FineTuningJob.retrieve(job.id)  
model\_id = job.fine\_tuned\_model  
  
# Use the fine-tuned model in LangChain  
model = ChatOpenAI(  
 model=model\_id,  
 temperature=1,  
)  

```

```python
(prompt | model).invoke({"input": "What's 56/7?"})  

```

```text
 AIMessage(content='{\n "num1": 56,\n "num2": 7,\n "operation": "/"\n}')  

```

Now you have successfully fine-tuned a model using data from LangSmith LLM runs!

- [Prerequisites](#prerequisites)
- [1. Select Runs](#1-select-runs)
- [2. Prepare data](#2-prepare-data)
- [3. Fine-tune the model](#3-fine-tune-the-model)
- [4. Use in LangChain](#4-use-in-langchain)

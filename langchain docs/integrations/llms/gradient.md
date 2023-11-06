# Gradient

`Gradient` allows to fine tune and get completions on LLMs with a simple web API.

This notebook goes over how to use Langchain with [Gradient](https://gradient.ai/).

## Imports[​](#imports "Direct link to Imports")

```python
from langchain.llms import GradientLLM  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

## Set the Environment API Key[​](#set-the-environment-api-key "Direct link to Set the Environment API Key")

Make sure to get your API key from Gradient AI. You are given $10 in free credits to test and fine-tune different models.

```python
from getpass import getpass  
import os  
  
if not os.environ.get("GRADIENT\_ACCESS\_TOKEN",None):  
 # Access token under https://auth.gradient.ai/select-workspace  
 os.environ["GRADIENT\_ACCESS\_TOKEN"] = getpass("gradient.ai access token:")  
if not os.environ.get("GRADIENT\_WORKSPACE\_ID",None):  
 # `ID` listed in `$ gradient workspace list`  
 # also displayed after login at at https://auth.gradient.ai/select-workspace  
 os.environ["GRADIENT\_WORKSPACE\_ID"] = getpass("gradient.ai workspace id:")  

```

Optional: Validate your Enviroment variables `GRADIENT_ACCESS_TOKEN` and `GRADIENT_WORKSPACE_ID` to get currently deployed models. Using the `gradientai` Python package.

```bash
pip install gradientai  

```

```text
 Requirement already satisfied: gradientai in /home/michi/.venv/lib/python3.10/site-packages (1.0.0)  
 Requirement already satisfied: aenum>=3.1.11 in /home/michi/.venv/lib/python3.10/site-packages (from gradientai) (3.1.15)  
 Requirement already satisfied: pydantic<2.0.0,>=1.10.5 in /home/michi/.venv/lib/python3.10/site-packages (from gradientai) (1.10.12)  
 Requirement already satisfied: python-dateutil>=2.8.2 in /home/michi/.venv/lib/python3.10/site-packages (from gradientai) (2.8.2)  
 Requirement already satisfied: urllib3>=1.25.3 in /home/michi/.venv/lib/python3.10/site-packages (from gradientai) (1.26.16)  
 Requirement already satisfied: typing-extensions>=4.2.0 in /home/michi/.venv/lib/python3.10/site-packages (from pydantic<2.0.0,>=1.10.5->gradientai) (4.5.0)  
 Requirement already satisfied: six>=1.5 in /home/michi/.venv/lib/python3.10/site-packages (from python-dateutil>=2.8.2->gradientai) (1.16.0)  

```

```python
import gradientai  
  
client = gradientai.Gradient()  
  
models = client.list\_models(only\_base=True)  
for model in models:  
 print(model.id)  

```

```text
 99148c6d-c2a0-4fbe-a4a7-e7c05bdb8a09\_base\_ml\_model  
 f0b97d96-51a8-4040-8b22-7940ee1fa24e\_base\_ml\_model  
 cc2dafce-9e6e-4a23-a918-cad6ba89e42e\_base\_ml\_model  

```

```python
new\_model = models[-1].create\_model\_adapter(name="my\_model\_adapter")  
new\_model.id, new\_model.name  

```

```text
 ('674119b5-f19e-4856-add2-767ae7f7d7ef\_model\_adapter', 'my\_model\_adapter')  

```

## Create the Gradient instance[​](#create-the-gradient-instance "Direct link to Create the Gradient instance")

You can specify different parameters such as the model, max_tokens generated, temperature, etc.

As we later want to fine-tune out model, we select the model_adapter with the id `674119b5-f19e-4856-add2-767ae7f7d7ef_model_adapter`, but you can use any base or fine-tunable model.

```python
llm = GradientLLM(  
 # `ID` listed in `$ gradient model list`  
 model="674119b5-f19e-4856-add2-767ae7f7d7ef\_model\_adapter",  
 # # optional: set new credentials, they default to environment variables  
 # gradient\_workspace\_id=os.environ["GRADIENT\_WORKSPACE\_ID"],  
 # gradient\_access\_token=os.environ["GRADIENT\_ACCESS\_TOKEN"],  
 model\_kwargs=dict(max\_generated\_token\_count=128)  
)  

```

## Create a Prompt Template[​](#create-a-prompt-template "Direct link to Create a Prompt Template")

We will create a prompt template for Question and Answer.

```python
template = """Question: {question}  
  
Answer: """  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

## Initiate the LLMChain[​](#initiate-the-llmchain "Direct link to Initiate the LLMChain")

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

## Run the LLMChain[​](#run-the-llmchain "Direct link to Run the LLMChain")

Provide a question and run the LLMChain.

```python
question = "What NFL team won the Super Bowl in 1994?"  
  
llm\_chain.run(  
 question=question  
)  

```

```text
 '\nThe San Francisco 49ers won the Super Bowl in 1994.'  

```

# Improve the results by fine-tuning (optional)

Well - that is wrong - the San Francisco 49ers did not win.
The correct answer to the question would be `The Dallas Cowboys!`.

Let's increase the odds for the correct answer, by fine-tuning on the correct answer using the PromptTemplate.

```python
dataset = [{"inputs": template.format(question="What NFL team won the Super Bowl in 1994?") + " The Dallas Cowboys!"}]  
dataset  

```

```text
 [{'inputs': 'Question: What NFL team won the Super Bowl in 1994?\n\nAnswer: The Dallas Cowboys!'}]  

```

```python
new\_model.fine\_tune(  
 samples=dataset  
)  

```

```text
 FineTuneResponse(number\_of\_trainable\_tokens=27, sum\_loss=78.17996)  

```

```python
# we can keep the llm\_chain, as the registered model just got refreshed on the gradient.ai servers.  
llm\_chain.run(  
 question=question  
)  

```

```text
 'The Dallas Cowboys'  

```

- [Imports](#imports)
- [Set the Environment API Key](#set-the-environment-api-key)
- [Create the Gradient instance](#create-the-gradient-instance)
- [Create a Prompt Template](#create-a-prompt-template)
- [Initiate the LLMChain](#initiate-the-llmchain)
- [Run the LLMChain](#run-the-llmchain)

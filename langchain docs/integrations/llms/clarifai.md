# Clarifai

[Clarifai](https://www.clarifai.com/) is an AI Platform that provides the full AI lifecycle ranging from data exploration, data labeling, model training, evaluation, and inference.

This example goes over how to use LangChain to interact with `Clarifai` [models](https://clarifai.com/explore/models).

To use Clarifai, you must have an account and a Personal Access Token (PAT) key.
[Check here](https://clarifai.com/settings/security) to get or create a PAT.

# Dependencies

```bash
# Install required dependencies  
pip install clarifai  

```

# Imports

Here we will be setting the personal access token. You can find your PAT under [settings/security](https://clarifai.com/settings/security) in your Clarifai account.

```python
# Please login and get your API key from https://clarifai.com/settings/security  
from getpass import getpass  
  
CLARIFAI\_PAT = getpass()  

```

```text
 ········  

```

```python
# Import the required modules  
from langchain.llms import Clarifai  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

# Input

Create a prompt template to be used with the LLM Chain:

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

# Setup

Setup the user id and app id where the model resides. You can find a list of public models on <https://clarifai.com/explore/models>

You will have to also initialize the model id and if needed, the model version id. Some models have many versions, you can choose the one appropriate for your task.

```python
USER\_ID = "openai"  
APP\_ID = "chat-completion"  
MODEL\_ID = "GPT-3\_5-turbo"  
  
# You can provide a specific model version as the model\_version\_id arg.  
# MODEL\_VERSION\_ID = "MODEL\_VERSION\_ID"  

```

```python
# Initialize a Clarifai LLM  
clarifai\_llm = Clarifai(  
 pat=CLARIFAI\_PAT, user\_id=USER\_ID, app\_id=APP\_ID, model\_id=MODEL\_ID  
)  

```

```python
# Create LLM chain  
llm\_chain = LLMChain(prompt=prompt, llm=clarifai\_llm)  

```

# Run Chain

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

```text
 'Justin Bieber was born on March 1, 1994. So, we need to figure out the Super Bowl winner for the 1994 season. The NFL season spans two calendar years, so the Super Bowl for the 1994 season would have taken place in early 1995. \n\nThe Super Bowl in question is Super Bowl XXIX, which was played on January 29, 1995. The game was won by the San Francisco 49ers, who defeated the San Diego Chargers by a score of 49-26. Therefore, the San Francisco 49ers won the Super Bowl in the year Justin Bieber was born.'  

```

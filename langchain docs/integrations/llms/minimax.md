# Minimax

[Minimax](https://api.minimax.chat) is a Chinese startup that provides natural language processing models for companies and individuals.

This example demonstrates using Langchain to interact with Minimax.

# Setup

To run this notebook, you'll need a [Minimax account](https://api.minimax.chat), an [API key](https://api.minimax.chat/user-center/basic-information/interface-key), and a [Group ID](https://api.minimax.chat/user-center/basic-information)

# Single model call

```python
from langchain.llms import Minimax  

```

```python
# Load the model  
minimax = Minimax(minimax\_api\_key="YOUR\_API\_KEY", minimax\_group\_id="YOUR\_GROUP\_ID")  

```

```python
# Prompt the model  
minimax("What is the difference between panda and bear?")  

```

# Chained model calls

```python
# get api\_key and group\_id: https://api.minimax.chat/user-center/basic-information  
# We need `MINIMAX\_API\_KEY` and `MINIMAX\_GROUP\_ID`  
  
import os  
  
os.environ["MINIMAX\_API\_KEY"] = "YOUR\_API\_KEY"  
os.environ["MINIMAX\_GROUP\_ID"] = "YOUR\_GROUP\_ID"  

```

```python
from langchain.llms import Minimax  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = Minimax()  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NBA team won the Championship in the year Jay Zhou was born?"  
  
llm\_chain.run(question)  

```

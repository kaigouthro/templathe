# Tongyi Qwen

Tongyi Qwen is a large-scale language model developed by Alibaba's Damo Academy. It is capable of understanding user intent through natural language understanding and semantic analysis, based on user input in natural language. It provides services and assistance to users in different domains and tasks. By providing clear and detailed instructions, you can obtain results that better align with your expectations.

```bash
# Install the package  
pip install dashscope  

```

```python
# Get a new token: https://help.aliyun.com/document\_detail/611472.html?spm=a2c4g.2399481.0.0  
from getpass import getpass  
  
DASHSCOPE\_API\_KEY = getpass()  

```

```text
 ········  

```

```python
import os  
  
os.environ["DASHSCOPE\_API\_KEY"] = DASHSCOPE\_API\_KEY  

```

```python
from langchain.llms import Tongyi  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = Tongyi()  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

```text
 "The year Justin Bieber was born was 1994. The Denver Broncos won the Super Bowl in 1997, which means they would have been the team that won the Super Bowl during Justin Bieber's birth year. So the answer is the Denver Broncos."  

```

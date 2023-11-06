# AliCloud PAI EAS

Machine Learning Platform for AI of Alibaba Cloud is a machine learning or deep learning engineering platform intended for enterprises and developers. It provides easy-to-use, cost-effective, high-performance, and easy-to-scale plug-ins that can be applied to various industry scenarios. With over 140 built-in optimization algorithms, Machine Learning Platform for AI provides whole-process AI engineering capabilities including data labeling (PAI-iTAG), model building (PAI-Designer and PAI-DSW), model training (PAI-DLC), compilation optimization, and inference deployment (PAI-EAS). PAI-EAS supports different types of hardware resources, including CPUs and GPUs, and features high throughput and low latency. It allows you to deploy large-scale complex models with a few clicks and perform elastic scale-ins and scale-outs in real time. It also provides a comprehensive O&M and monitoring system.

```python
from langchain.llms.pai\_eas\_endpoint import PaiEasEndpoint  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

One who want to use eas llms must set up eas service first. When the eas service is launched, eas_service_rul and eas_service token can be got. Users can refer to <https://www.alibabacloud.com/help/en/pai/user-guide/service-deployment/> for more information,

```python
import os  
os.environ["EAS\_SERVICE\_URL"] = "Your\_EAS\_Service\_URL"  
os.environ["EAS\_SERVICE\_TOKEN"] = "Your\_EAS\_Service\_Token"  
llm = PaiEasEndpoint(eas\_service\_url=os.environ["EAS\_SERVICE\_URL"], eas\_service\_token=os.environ["EAS\_SERVICE\_TOKEN"])  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  
  
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
llm\_chain.run(question)  

```

```text
 ' Thank you for asking! However, I must respectfully point out that the question contains an error. Justin Bieber was born in 1994, and the Super Bowl was first played in 1967. Therefore, it is not possible for any NFL team to have won the Super Bowl in the year Justin Bieber was born.\n\nI hope this clarifies things! If you have any other questions, please feel free to ask.'  

```

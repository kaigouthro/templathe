# AliCloud PAI EAS

Machine Learning Platform for AI of Alibaba Cloud is a machine learning or deep learning engineering platform intended for enterprises and developers. It provides easy-to-use, cost-effective, high-performance, and easy-to-scale plug-ins that can be applied to various industry scenarios. With over 140 built-in optimization algorithms, Machine Learning Platform for AI provides whole-process AI engineering capabilities including data labeling (PAI-iTAG), model building (PAI-Designer and PAI-DSW), model training (PAI-DLC), compilation optimization, and inference deployment (PAI-EAS). PAI-EAS supports different types of hardware resources, including CPUs and GPUs, and features high throughput and low latency. It allows you to deploy large-scale complex models with a few clicks and perform elastic scale-ins and scale-outs in real time. It also provides a comprehensive O&M and monitoring system.

## Setup Eas Service[​](#setup-eas-service "Direct link to Setup Eas Service")

One who want to use eas llms must set up eas service first. When the eas service is launched, eas_service_rul and eas_service token can be got. Users can refer to <https://www.alibabacloud.com/help/en/pai/user-guide/service-deployment/> for more information. Try to set environment variables to init eas service url and token:

```base
export EAS\_SERVICE\_URL=XXX  
export EAS\_SERVICE\_TOKEN=XXX  

```

or run as follow codes:

```python
import os  
from langchain.chat\_models.base import HumanMessage  
from langchain.chat\_models import PaiEasChatEndpoint  
os.environ["EAS\_SERVICE\_URL"] = "Your\_EAS\_Service\_URL"  
os.environ["EAS\_SERVICE\_TOKEN"] = "Your\_EAS\_Service\_Token"  
chat = PaiEasChatEndpoint(  
 eas\_service\_url=os.environ["EAS\_SERVICE\_URL"],   
 eas\_service\_token=os.environ["EAS\_SERVICE\_TOKEN"]  
)  

```

## Run Chat Model[​](#run-chat-model "Direct link to Run Chat Model")

You can use the default settings to call eas service as follows:

```python
output = chat([HumanMessage(content="write a funny joke")])  
print("output:", output)  

```

Or, call eas service with new inference params:

```python
kwargs = {"temperature": 0.8, "top\_p": 0.8, "top\_k": 5}  
output = chat([HumanMessage(content="write a funny joke")], \*\*kwargs)  
print("output:", output)  

```

Or, run a stream call to get a stream response:

```python
outputs = chat.stream([HumanMessage(content="hi")], streaming=True)  
for output in outputs:  
 print("stream output:", output)  

```

- [Setup Eas Service](#setup-eas-service)
- [Run Chat Model](#run-chat-model)

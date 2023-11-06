# ChatGLM

[ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) is an open bilingual language model based on General Language Model (GLM) framework, with 6.2 billion parameters. With the quantization technique, users can deploy locally on consumer-grade graphics cards (only 6GB of GPU memory is required at the INT4 quantization level).

[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) is the second-generation version of the open-source bilingual (Chinese-English) chat model ChatGLM-6B. It retains the smooth conversation flow and low deployment threshold of the first-generation model, while introducing the new features like better performance, longer context and more efficient inference.

This example goes over how to use LangChain to interact with ChatGLM2-6B Inference for text completion.
ChatGLM-6B and ChatGLM2-6B has the same api specs, so this example should work with both.

```python
from langchain.llms import ChatGLM  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
# import os  

```

```python
template = """{question}"""  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
# default endpoint\_url for a local deployed ChatGLM api server  
endpoint\_url = "http://127.0.0.1:8000"  
  
# direct access endpoint in a proxied environment  
# os.environ['NO\_PROXY'] = '127.0.0.1'  
  
llm = ChatGLM(  
 endpoint\_url=endpoint\_url,  
 max\_token=80000,  
 history=[["我将从美国到中国来旅游，出行前希望了解中国的城市", "欢迎问我任何问题。"]],  
 top\_p=0.9,  
 model\_kwargs={"sample\_model\_args": False},  
)  
  
# turn on with\_history only when you want the LLM object to keep track of the conversation history  
# and send the accumulated context to the backend model api, which make it stateful. By default it is stateless.  
# llm.with\_history = True  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "北京和上海两座城市有什么不同？"  
  
llm\_chain.run(question)  

```

```text
 ChatGLM payload: {'prompt': '北京和上海两座城市有什么不同？', 'temperature': 0.1, 'history': [['我将从美国到中国来旅游，出行前希望了解中国的城市', '欢迎问我任何问题。']], 'max\_length': 80000, 'top\_p': 0.9, 'sample\_model\_args': False}  
  
  
  
  
  
 '北京和上海是中国的两个首都，它们在许多方面都有所不同。\n\n北京是中国的政治和文化中心，拥有悠久的历史和灿烂的文化。它是中国最重要的古都之一，也是中国历史上最后一个封建王朝的都城。北京有许多著名的古迹和景点，例如紫禁城、天安门广场和长城等。\n\n上海是中国最现代化的城市之一，也是中国商业和金融中心。上海拥有许多国际知名的企业和金融机构，同时也有许多著名的景点和美食。上海的外滩是一个历史悠久的商业区，拥有许多欧式建筑和餐馆。\n\n除此之外，北京和上海在交通和人口方面也有很大差异。北京是中国的首都，人口众多，交通拥堵问题较为严重。而上海是中国的商业和金融中心，人口密度较低，交通相对较为便利。\n\n总的来说，北京和上海是两个拥有独特魅力和特点的城市，可以根据自己的兴趣和时间来选择前往其中一座城市旅游。'  

```

# Custom chain

To implement your own custom chain you can subclass `Chain` and implement the following methods:

```python
from \_\_future\_\_ import annotations  
  
from typing import Any, Dict, List, Optional  
  
from pydantic import Extra  
  
from langchain.schema.language\_model import BaseLanguageModel  
from langchain.callbacks.manager import (  
 AsyncCallbackManagerForChainRun,  
 CallbackManagerForChainRun,  
)  
from langchain.chains.base import Chain  
from langchain.prompts.base import BasePromptTemplate  
  
  
class MyCustomChain(Chain):  
 """  
 An example of a custom chain.  
 """  
  
 prompt: BasePromptTemplate  
 """Prompt object to use."""  
 llm: BaseLanguageModel  
 output\_key: str = "text" #: :meta private:  
  
 class Config:  
 """Configuration for this pydantic object."""  
  
 extra = Extra.forbid  
 arbitrary\_types\_allowed = True  
  
 @property  
 def input\_keys(self) -> List[str]:  
 """Will be whatever keys the prompt expects.  
  
 :meta private:  
 """  
 return self.prompt.input\_variables  
  
 @property  
 def output\_keys(self) -> List[str]:  
 """Will always return text key.  
  
 :meta private:  
 """  
 return [self.output\_key]  
  
 def \_call(  
 self,  
 inputs: Dict[str, Any],  
 run\_manager: Optional[CallbackManagerForChainRun] = None,  
 ) -> Dict[str, str]:  
 # Your custom chain logic goes here  
 # This is just an example that mimics LLMChain  
 prompt\_value = self.prompt.format\_prompt(\*\*inputs)  
  
 # Whenever you call a language model, or another chain, you should pass  
 # a callback manager to it. This allows the inner run to be tracked by  
 # any callbacks that are registered on the outer run.  
 # You can always obtain a callback manager for this by calling  
 # `run\_manager.get\_child()` as shown below.  
 response = self.llm.generate\_prompt(  
 [prompt\_value], callbacks=run\_manager.get\_child() if run\_manager else None  
 )  
  
 # If you want to log something about this run, you can do so by calling  
 # methods on the `run\_manager`, as shown below. This will trigger any  
 # callbacks that are registered for that event.  
 if run\_manager:  
 run\_manager.on\_text("Log something about this run")  
  
 return {self.output\_key: response.generations[0][0].text}  
  
 async def \_acall(  
 self,  
 inputs: Dict[str, Any],  
 run\_manager: Optional[AsyncCallbackManagerForChainRun] = None,  
 ) -> Dict[str, str]:  
 # Your custom chain logic goes here  
 # This is just an example that mimics LLMChain  
 prompt\_value = self.prompt.format\_prompt(\*\*inputs)  
  
 # Whenever you call a language model, or another chain, you should pass  
 # a callback manager to it. This allows the inner run to be tracked by  
 # any callbacks that are registered on the outer run.  
 # You can always obtain a callback manager for this by calling  
 # `run\_manager.get\_child()` as shown below.  
 response = await self.llm.agenerate\_prompt(  
 [prompt\_value], callbacks=run\_manager.get\_child() if run\_manager else None  
 )  
  
 # If you want to log something about this run, you can do so by calling  
 # methods on the `run\_manager`, as shown below. This will trigger any  
 # callbacks that are registered for that event.  
 if run\_manager:  
 await run\_manager.on\_text("Log something about this run")  
  
 return {self.output\_key: response.generations[0][0].text}  
  
 @property  
 def \_chain\_type(self) -> str:  
 return "my\_custom\_chain"  

```

```python
from langchain.callbacks.stdout import StdOutCallbackHandler  
from langchain.chat\_models.openai import ChatOpenAI  
from langchain.prompts.prompt import PromptTemplate  
  
  
chain = MyCustomChain(  
 prompt=PromptTemplate.from\_template("tell us a joke about {topic}"),  
 llm=ChatOpenAI(),  
)  
  
chain.run({"topic": "callbacks"}, callbacks=[StdOutCallbackHandler()])  

```

```text
   
   
 > Entering new MyCustomChain chain...  
 Log something about this run  
 > Finished chain.  
  
  
  
  
  
 'Why did the callback function feel lonely? Because it was always waiting for someone to call it back!'  

```

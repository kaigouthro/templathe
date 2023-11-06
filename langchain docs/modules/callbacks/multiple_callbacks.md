# Multiple callback handlers

In the previous examples, we passed in callback handlers upon creation of an object by using `callbacks=`. In this case, the callbacks will be scoped to that particular object.

However, in many cases, it is advantageous to pass in handlers instead when running the object. When we pass through `CallbackHandlers` using the `callbacks` keyword arg when executing an run, those callbacks will be issued by all nested objects involved in the execution. For example, when a handler is passed through to an `Agent`, it will be used for all callbacks related to the agent and all the objects involved in the agent's execution, in this case, the `Tools`, `LLMChain`, and `LLM`.

This prevents us from having to manually attach the handlers to each individual nested object.

```python
from typing import Dict, Union, Any, List  
  
from langchain.callbacks.base import BaseCallbackHandler  
from langchain.schema import AgentAction  
from langchain.agents import AgentType, initialize\_agent, load\_tools  
from langchain.callbacks import tracing\_enabled  
from langchain.llms import OpenAI  
  
  
# First, define custom callback handler implementations  
class MyCustomHandlerOne(BaseCallbackHandler):  
 def on\_llm\_start(  
 self, serialized: Dict[str, Any], prompts: List[str], \*\*kwargs: Any  
 ) -> Any:  
 print(f"on\_llm\_start {serialized['name']}")  
  
 def on\_llm\_new\_token(self, token: str, \*\*kwargs: Any) -> Any:  
 print(f"on\_new\_token {token}")  
  
 def on\_llm\_error(  
 self, error: Union[Exception, KeyboardInterrupt], \*\*kwargs: Any  
 ) -> Any:  
 """Run when LLM errors."""  
  
 def on\_chain\_start(  
 self, serialized: Dict[str, Any], inputs: Dict[str, Any], \*\*kwargs: Any  
 ) -> Any:  
 print(f"on\_chain\_start {serialized['name']}")  
  
 def on\_tool\_start(  
 self, serialized: Dict[str, Any], input\_str: str, \*\*kwargs: Any  
 ) -> Any:  
 print(f"on\_tool\_start {serialized['name']}")  
  
 def on\_agent\_action(self, action: AgentAction, \*\*kwargs: Any) -> Any:  
 print(f"on\_agent\_action {action}")  
  
  
class MyCustomHandlerTwo(BaseCallbackHandler):  
 def on\_llm\_start(  
 self, serialized: Dict[str, Any], prompts: List[str], \*\*kwargs: Any  
 ) -> Any:  
 print(f"on\_llm\_start (I'm the second handler!!) {serialized['name']}")  
  
  
# Instantiate the handlers  
handler1 = MyCustomHandlerOne()  
handler2 = MyCustomHandlerTwo()  
  
# Setup the agent. Only the `llm` will issue callbacks for handler2  
llm = OpenAI(temperature=0, streaming=True, callbacks=[handler2])  
tools = load\_tools(["llm-math"], llm=llm)  
agent = initialize\_agent(tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION)  
  
# Callbacks for handler1 will be issued by every object involved in the  
# Agent execution (llm, llmchain, tool, agent executor)  
agent.run("What is 2 raised to the 0.235 power?", callbacks=[handler1])  

```

````text
 on\_chain\_start AgentExecutor  
 on\_chain\_start LLMChain  
 on\_llm\_start OpenAI  
 on\_llm\_start (I'm the second handler!!) OpenAI  
 on\_new\_token I  
 on\_new\_token need  
 on\_new\_token to  
 on\_new\_token use  
 on\_new\_token a  
 on\_new\_token calculator  
 on\_new\_token to  
 on\_new\_token solve  
 on\_new\_token this  
 on\_new\_token .  
 on\_new\_token   
 Action  
 on\_new\_token :  
 on\_new\_token Calculator  
 on\_new\_token   
 Action  
 on\_new\_token Input  
 on\_new\_token :  
 on\_new\_token 2  
 on\_new\_token ^  
 on\_new\_token 0  
 on\_new\_token .  
 on\_new\_token 235  
 on\_new\_token   
 on\_agent\_action AgentAction(tool='Calculator', tool\_input='2^0.235', log=' I need to use a calculator to solve this.\nAction: Calculator\nAction Input: 2^0.235')  
 on\_tool\_start Calculator  
 on\_chain\_start LLMMathChain  
 on\_chain\_start LLMChain  
 on\_llm\_start OpenAI  
 on\_llm\_start (I'm the second handler!!) OpenAI  
 on\_new\_token   
 on\_new\_token ```text  
 on\_new\_token   
   
 on\_new\_token 2  
 on\_new\_token \*\*  
 on\_new\_token 0  
 on\_new\_token .  
 on\_new\_token 235  
 on\_new\_token   
   
 on\_new\_token ```  
   
 on\_new\_token ...  
 on\_new\_token num  
 on\_new\_token expr  
 on\_new\_token .  
 on\_new\_token evaluate  
 on\_new\_token ("  
 on\_new\_token 2  
 on\_new\_token \*\*  
 on\_new\_token 0  
 on\_new\_token .  
 on\_new\_token 235  
 on\_new\_token ")  
 on\_new\_token ...  
 on\_new\_token   
   
 on\_new\_token   
 on\_chain\_start LLMChain  
 on\_llm\_start OpenAI  
 on\_llm\_start (I'm the second handler!!) OpenAI  
 on\_new\_token I  
 on\_new\_token now  
 on\_new\_token know  
 on\_new\_token the  
 on\_new\_token final  
 on\_new\_token answer  
 on\_new\_token .  
 on\_new\_token   
 Final  
 on\_new\_token Answer  
 on\_new\_token :  
 on\_new\_token 1  
 on\_new\_token .  
 on\_new\_token 17  
 on\_new\_token 690  
 on\_new\_token 67  
 on\_new\_token 372  
 on\_new\_token 187  
 on\_new\_token 674  
 on\_new\_token   
  
  
  
  
  
 '1.1769067372187674'  

````

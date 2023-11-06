# Tool Input Schema

By default, tools infer the argument schema by inspecting the function signature. For more strict requirements, custom input schema can be specified, along with custom validation logic.

```python
from typing import Any, Dict  
  
from langchain.agents import AgentType, initialize\_agent  
from langchain.llms import OpenAI  
from langchain.tools.requests.tool import RequestsGetTool, TextRequestsWrapper  
from pydantic import BaseModel, Field, root\_validator  

```

```python
llm = OpenAI(temperature=0)  

```

```bash
pip install tldextract > /dev/null  

```

```text
   
 [notice] A new release of pip is available: 23.0.1 -> 23.1  
 [notice] To update, run: pip install --upgrade pip  

```

```python
import tldextract  
  
\_APPROVED\_DOMAINS = {  
 "langchain",  
 "wikipedia",  
}  
  
  
class ToolInputSchema(BaseModel):  
 url: str = Field(...)  
  
 @root\_validator  
 def validate\_query(cls, values: Dict[str, Any]) -> Dict:  
 url = values["url"]  
 domain = tldextract.extract(url).domain  
 if domain not in \_APPROVED\_DOMAINS:  
 raise ValueError(  
 f"Domain {domain} is not on the approved list:"  
 f" {sorted(\_APPROVED\_DOMAINS)}"  
 )  
 return values  
  
  
tool = RequestsGetTool(  
 args\_schema=ToolInputSchema, requests\_wrapper=TextRequestsWrapper()  
)  

```

```python
agent = initialize\_agent(  
 [tool], llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=False  
)  

```

```python
# This will succeed, since there aren't any arguments that will be triggered during validation  
answer = agent.run("What's the main title on langchain.com?")  
print(answer)  

```

```text
 The main title of langchain.com is "LANG CHAIN 🦜️🔗 Official Home Page"  

```

```python
agent.run("What's the main title on google.com?")  

```

```text
 ---------------------------------------------------------------------------  
  
 ValidationError Traceback (most recent call last)  
  
 Cell In[7], line 1  
 ----> 1 agent.run("What's the main title on google.com?")  
  
  
 File ~/code/lc/lckg/langchain/chains/base.py:213, in Chain.run(self, \*args, \*\*kwargs)  
 211 if len(args) != 1:  
 212 raise ValueError("`run` supports only one positional argument.")  
 --> 213 return self(args[0])[self.output\_keys[0]]  
 215 if kwargs and not args:  
 216 return self(kwargs)[self.output\_keys[0]]  
  
  
 File ~/code/lc/lckg/langchain/chains/base.py:116, in Chain.\_\_call\_\_(self, inputs, return\_only\_outputs)  
 114 except (KeyboardInterrupt, Exception) as e:  
 115 self.callback\_manager.on\_chain\_error(e, verbose=self.verbose)  
 --> 116 raise e  
 117 self.callback\_manager.on\_chain\_end(outputs, verbose=self.verbose)  
 118 return self.prep\_outputs(inputs, outputs, return\_only\_outputs)  
  
  
 File ~/code/lc/lckg/langchain/chains/base.py:113, in Chain.\_\_call\_\_(self, inputs, return\_only\_outputs)  
 107 self.callback\_manager.on\_chain\_start(  
 108 {"name": self.\_\_class\_\_.\_\_name\_\_},  
 109 inputs,  
 110 verbose=self.verbose,  
 111 )  
 112 try:  
 --> 113 outputs = self.\_call(inputs)  
 114 except (KeyboardInterrupt, Exception) as e:  
 115 self.callback\_manager.on\_chain\_error(e, verbose=self.verbose)  
  
  
 File ~/code/lc/lckg/langchain/agents/agent.py:792, in AgentExecutor.\_call(self, inputs)  
 790 # We now enter the agent loop (until it returns something).  
 791 while self.\_should\_continue(iterations, time\_elapsed):  
 --> 792 next\_step\_output = self.\_take\_next\_step(  
 793 name\_to\_tool\_map, color\_mapping, inputs, intermediate\_steps  
 794 )  
 795 if isinstance(next\_step\_output, AgentFinish):  
 796 return self.\_return(next\_step\_output, intermediate\_steps)  
  
  
 File ~/code/lc/lckg/langchain/agents/agent.py:695, in AgentExecutor.\_take\_next\_step(self, name\_to\_tool\_map, color\_mapping, inputs, intermediate\_steps)  
 693 tool\_run\_kwargs["llm\_prefix"] = ""  
 694 # We then call the tool on the tool input to get an observation  
 --> 695 observation = tool.run(  
 696 agent\_action.tool\_input,  
 697 verbose=self.verbose,  
 698 color=color,  
 699 \*\*tool\_run\_kwargs,  
 700 )  
 701 else:  
 702 tool\_run\_kwargs = self.agent.tool\_run\_logging\_kwargs()  
  
  
 File ~/code/lc/lckg/langchain/tools/base.py:110, in BaseTool.run(self, tool\_input, verbose, start\_color, color, \*\*kwargs)  
 101 def run(  
 102 self,  
 103 tool\_input: Union[str, Dict],  
 (...)  
 107 \*\*kwargs: Any,  
 108 ) -> str:  
 109 """Run the tool."""  
 --> 110 run\_input = self.\_parse\_input(tool\_input)  
 111 if not self.verbose and verbose is not None:  
 112 verbose\_ = verbose  
  
  
 File ~/code/lc/lckg/langchain/tools/base.py:71, in BaseTool.\_parse\_input(self, tool\_input)  
 69 if issubclass(input\_args, BaseModel):  
 70 key\_ = next(iter(input\_args.\_\_fields\_\_.keys()))  
 ---> 71 input\_args.parse\_obj({key\_: tool\_input})  
 72 # Passing as a positional argument is more straightforward for  
 73 # backwards compatability  
 74 return tool\_input  
  
  
 File ~/code/lc/lckg/.venv/lib/python3.11/site-packages/pydantic/main.py:526, in pydantic.main.BaseModel.parse\_obj()  
  
  
 File ~/code/lc/lckg/.venv/lib/python3.11/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.\_\_init\_\_()  
  
  
 ValidationError: 1 validation error for ToolInputSchema  
 \_\_root\_\_  
 Domain google is not on the approved list: ['langchain', 'wikipedia'] (type=value\_error)  

```

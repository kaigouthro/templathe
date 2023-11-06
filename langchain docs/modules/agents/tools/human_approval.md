# Human-in-the-loop Tool Validation

This walkthrough demonstrates how to add human validation to any Tool. We'll do this using the `HumanApprovalCallbackhandler`.

Let's suppose we need to make use of the `ShellTool`. Adding this tool to an automated flow poses obvious risks. Let's see how we could enforce manual human approval of inputs going into this tool.

**Note**: We generally recommend against using the `ShellTool`. There's a lot of ways to misuse it, and it's not required for most use cases. We employ it here only for demonstration purposes.

```python
from langchain.callbacks import HumanApprovalCallbackHandler  
from langchain.tools import ShellTool  

```

```python
tool = ShellTool()  

```

```python
print(tool.run("echo Hello World!"))  

```

```text
 Hello World!  
   

```

## Adding Human Approval[​](#adding-human-approval "Direct link to Adding Human Approval")

Adding the default `HumanApprovalCallbackHandler` to the tool will make it so that a user has to manually approve every input to the tool before the command is actually executed.

```python
tool = ShellTool(callbacks=[HumanApprovalCallbackHandler()])  

```

```python
print(tool.run("ls /usr"))  

```

```text
 Do you approve of the following input? Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no.  
   
 ls /usr  
 yes  
 X11  
 X11R6  
 bin  
 lib  
 libexec  
 local  
 sbin  
 share  
 standalone  
   

```

```python
print(tool.run("ls /private"))  

```

```text
 Do you approve of the following input? Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no.  
   
 ls /private  
 no  
  
  
  
 ---------------------------------------------------------------------------  
  
 HumanRejectedException Traceback (most recent call last)  
  
 Cell In[17], line 1  
 ----> 1 print(tool.run("ls /private"))  
  
  
 File ~/langchain/langchain/tools/base.py:257, in BaseTool.run(self, tool\_input, verbose, start\_color, color, callbacks, \*\*kwargs)  
 255 # TODO: maybe also pass through run\_manager is \_run supports kwargs  
 256 new\_arg\_supported = signature(self.\_run).parameters.get("run\_manager")  
 --> 257 run\_manager = callback\_manager.on\_tool\_start(  
 258 {"name": self.name, "description": self.description},  
 259 tool\_input if isinstance(tool\_input, str) else str(tool\_input),  
 260 color=start\_color,  
 261 \*\*kwargs,  
 262 )  
 263 try:  
 264 tool\_args, tool\_kwargs = self.\_to\_args\_and\_kwargs(parsed\_input)  
  
  
 File ~/langchain/langchain/callbacks/manager.py:672, in CallbackManager.on\_tool\_start(self, serialized, input\_str, run\_id, parent\_run\_id, \*\*kwargs)  
 669 if run\_id is None:  
 670 run\_id = uuid4()  
 --> 672 \_handle\_event(  
 673 self.handlers,  
 674 "on\_tool\_start",  
 675 "ignore\_agent",  
 676 serialized,  
 677 input\_str,  
 678 run\_id=run\_id,  
 679 parent\_run\_id=self.parent\_run\_id,  
 680 \*\*kwargs,  
 681 )  
 683 return CallbackManagerForToolRun(  
 684 run\_id, self.handlers, self.inheritable\_handlers, self.parent\_run\_id  
 685 )  
  
  
 File ~/langchain/langchain/callbacks/manager.py:157, in \_handle\_event(handlers, event\_name, ignore\_condition\_name, \*args, \*\*kwargs)  
 155 except Exception as e:  
 156 if handler.raise\_error:  
 --> 157 raise e  
 158 logging.warning(f"Error in {event\_name} callback: {e}")  
  
  
 File ~/langchain/langchain/callbacks/manager.py:139, in \_handle\_event(handlers, event\_name, ignore\_condition\_name, \*args, \*\*kwargs)  
 135 try:  
 136 if ignore\_condition\_name is None or not getattr(  
 137 handler, ignore\_condition\_name  
 138 ):  
 --> 139 getattr(handler, event\_name)(\*args, \*\*kwargs)  
 140 except NotImplementedError as e:  
 141 if event\_name == "on\_chat\_model\_start":  
  
  
 File ~/langchain/langchain/callbacks/human.py:48, in HumanApprovalCallbackHandler.on\_tool\_start(self, serialized, input\_str, run\_id, parent\_run\_id, \*\*kwargs)  
 38 def on\_tool\_start(  
 39 self,  
 40 serialized: Dict[str, Any],  
 (...)  
 45 \*\*kwargs: Any,  
 46 ) -> Any:  
 47 if self.\_should\_check(serialized) and not self.\_approve(input\_str):  
 ---> 48 raise HumanRejectedException(  
 49 f"Inputs {input\_str} to tool {serialized} were rejected."  
 50 )  
  
  
 HumanRejectedException: Inputs ls /private to tool {'name': 'terminal', 'description': 'Run shell commands on this MacOS machine.'} were rejected.  

```

## Configuring Human Approval[​](#configuring-human-approval "Direct link to Configuring Human Approval")

Let's suppose we have an agent that takes in multiple tools, and we want it to only trigger human approval requests on certain tools and certain inputs. We can configure out callback handler to do just this.

```python
from langchain.agents import load\_tools  
from langchain.agents import initialize\_agent  
from langchain.agents import AgentType  
from langchain.llms import OpenAI  

```

```python
def \_should\_check(serialized\_obj: dict) -> bool:  
 # Only require approval on ShellTool.  
 return serialized\_obj.get("name") == "terminal"  
  
  
def \_approve(\_input: str) -> bool:  
 if \_input == "echo 'Hello World'":  
 return True  
 msg = (  
 "Do you approve of the following input? "  
 "Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no."  
 )  
 msg += "\n\n" + \_input + "\n"  
 resp = input(msg)  
 return resp.lower() in ("yes", "y")  
  
  
callbacks = [HumanApprovalCallbackHandler(should\_check=\_should\_check, approve=\_approve)]  

```

```python
llm = OpenAI(temperature=0)  
tools = load\_tools(["wikipedia", "llm-math", "terminal"], llm=llm)  
agent = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,  
)  

```

```python
agent.run(  
 "It's 2023 now. How many years ago did Konrad Adenauer become Chancellor of Germany.",  
 callbacks=callbacks,  
)  

```

```text
 'Konrad Adenauer became Chancellor of Germany in 1949, 74 years ago.'  

```

```python
agent.run("print 'Hello World' in the terminal", callbacks=callbacks)  

```

```text
 'Hello World'  

```

```python
agent.run("list all directories in /private", callbacks=callbacks)  

```

```text
 Do you approve of the following input? Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no.  
   
 ls /private  
 no  
  
  
  
 ---------------------------------------------------------------------------  
  
 HumanRejectedException Traceback (most recent call last)  
  
 Cell In[39], line 1  
 ----> 1 agent.run("list all directories in /private", callbacks=callbacks)  
  
  
 File ~/langchain/langchain/chains/base.py:236, in Chain.run(self, callbacks, \*args, \*\*kwargs)  
 234 if len(args) != 1:  
 235 raise ValueError("`run` supports only one positional argument.")  
 --> 236 return self(args[0], callbacks=callbacks)[self.output\_keys[0]]  
 238 if kwargs and not args:  
 239 return self(kwargs, callbacks=callbacks)[self.output\_keys[0]]  
  
  
 File ~/langchain/langchain/chains/base.py:140, in Chain.\_\_call\_\_(self, inputs, return\_only\_outputs, callbacks)  
 138 except (KeyboardInterrupt, Exception) as e:  
 139 run\_manager.on\_chain\_error(e)  
 --> 140 raise e  
 141 run\_manager.on\_chain\_end(outputs)  
 142 return self.prep\_outputs(inputs, outputs, return\_only\_outputs)  
  
  
 File ~/langchain/langchain/chains/base.py:134, in Chain.\_\_call\_\_(self, inputs, return\_only\_outputs, callbacks)  
 128 run\_manager = callback\_manager.on\_chain\_start(  
 129 {"name": self.\_\_class\_\_.\_\_name\_\_},  
 130 inputs,  
 131 )  
 132 try:  
 133 outputs = (  
 --> 134 self.\_call(inputs, run\_manager=run\_manager)  
 135 if new\_arg\_supported  
 136 else self.\_call(inputs)  
 137 )  
 138 except (KeyboardInterrupt, Exception) as e:  
 139 run\_manager.on\_chain\_error(e)  
  
  
 File ~/langchain/langchain/agents/agent.py:953, in AgentExecutor.\_call(self, inputs, run\_manager)  
 951 # We now enter the agent loop (until it returns something).  
 952 while self.\_should\_continue(iterations, time\_elapsed):  
 --> 953 next\_step\_output = self.\_take\_next\_step(  
 954 name\_to\_tool\_map,  
 955 color\_mapping,  
 956 inputs,  
 957 intermediate\_steps,  
 958 run\_manager=run\_manager,  
 959 )  
 960 if isinstance(next\_step\_output, AgentFinish):  
 961 return self.\_return(  
 962 next\_step\_output, intermediate\_steps, run\_manager=run\_manager  
 963 )  
  
  
 File ~/langchain/langchain/agents/agent.py:820, in AgentExecutor.\_take\_next\_step(self, name\_to\_tool\_map, color\_mapping, inputs, intermediate\_steps, run\_manager)  
 818 tool\_run\_kwargs["llm\_prefix"] = ""  
 819 # We then call the tool on the tool input to get an observation  
 --> 820 observation = tool.run(  
 821 agent\_action.tool\_input,  
 822 verbose=self.verbose,  
 823 color=color,  
 824 callbacks=run\_manager.get\_child() if run\_manager else None,  
 825 \*\*tool\_run\_kwargs,  
 826 )  
 827 else:  
 828 tool\_run\_kwargs = self.agent.tool\_run\_logging\_kwargs()  
  
  
 File ~/langchain/langchain/tools/base.py:257, in BaseTool.run(self, tool\_input, verbose, start\_color, color, callbacks, \*\*kwargs)  
 255 # TODO: maybe also pass through run\_manager is \_run supports kwargs  
 256 new\_arg\_supported = signature(self.\_run).parameters.get("run\_manager")  
 --> 257 run\_manager = callback\_manager.on\_tool\_start(  
 258 {"name": self.name, "description": self.description},  
 259 tool\_input if isinstance(tool\_input, str) else str(tool\_input),  
 260 color=start\_color,  
 261 \*\*kwargs,  
 262 )  
 263 try:  
 264 tool\_args, tool\_kwargs = self.\_to\_args\_and\_kwargs(parsed\_input)  
  
  
 File ~/langchain/langchain/callbacks/manager.py:672, in CallbackManager.on\_tool\_start(self, serialized, input\_str, run\_id, parent\_run\_id, \*\*kwargs)  
 669 if run\_id is None:  
 670 run\_id = uuid4()  
 --> 672 \_handle\_event(  
 673 self.handlers,  
 674 "on\_tool\_start",  
 675 "ignore\_agent",  
 676 serialized,  
 677 input\_str,  
 678 run\_id=run\_id,  
 679 parent\_run\_id=self.parent\_run\_id,  
 680 \*\*kwargs,  
 681 )  
 683 return CallbackManagerForToolRun(  
 684 run\_id, self.handlers, self.inheritable\_handlers, self.parent\_run\_id  
 685 )  
  
  
 File ~/langchain/langchain/callbacks/manager.py:157, in \_handle\_event(handlers, event\_name, ignore\_condition\_name, \*args, \*\*kwargs)  
 155 except Exception as e:  
 156 if handler.raise\_error:  
 --> 157 raise e  
 158 logging.warning(f"Error in {event\_name} callback: {e}")  
  
  
 File ~/langchain/langchain/callbacks/manager.py:139, in \_handle\_event(handlers, event\_name, ignore\_condition\_name, \*args, \*\*kwargs)  
 135 try:  
 136 if ignore\_condition\_name is None or not getattr(  
 137 handler, ignore\_condition\_name  
 138 ):  
 --> 139 getattr(handler, event\_name)(\*args, \*\*kwargs)  
 140 except NotImplementedError as e:  
 141 if event\_name == "on\_chat\_model\_start":  
  
  
 File ~/langchain/langchain/callbacks/human.py:48, in HumanApprovalCallbackHandler.on\_tool\_start(self, serialized, input\_str, run\_id, parent\_run\_id, \*\*kwargs)  
 38 def on\_tool\_start(  
 39 self,  
 40 serialized: Dict[str, Any],  
 (...)  
 45 \*\*kwargs: Any,  
 46 ) -> Any:  
 47 if self.\_should\_check(serialized) and not self.\_approve(input\_str):  
 ---> 48 raise HumanRejectedException(  
 49 f"Inputs {input\_str} to tool {serialized} were rejected."  
 50 )  
  
  
 HumanRejectedException: Inputs ls /private to tool {'name': 'terminal', 'description': 'Run shell commands on this MacOS machine.'} were rejected.  

```

- [Adding Human Approval](#adding-human-approval)
- [Configuring Human Approval](#configuring-human-approval)

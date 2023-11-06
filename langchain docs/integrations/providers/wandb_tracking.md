# Weights & Biases

This notebook goes over how to track your LangChain experiments into one centralized Weights and Biases dashboard. To learn more about prompt engineering and the callback please refer to this Report which explains both alongside the resultant dashboards you can expect to see.

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

[View Report](https://wandb.ai/a-sh0ts/langchain_callback_demo/reports/Prompt-Engineering-LLMs-with-LangChain-and-W-B--VmlldzozNjk1NTUw#%F0%9F%91%8B-how-to-build-a-callback-in-langchain-for-better-prompt-engineering)

**Note**: *the `WandbCallbackHandler` is being deprecated in favour of the `WandbTracer`* . In future please use the `WandbTracer` as it is more flexible and allows for more granular logging. To know more about the `WandbTracer` refer to the [agent_with_wandb_tracing.html](https://python.langchain.com/en/latest/integrations/agent_with_wandb_tracing.html) notebook or use the following [colab notebook](http://wandb.me/prompts-quickstart). To know more about Weights & Biases Prompts refer to the following [prompts documentation](https://docs.wandb.ai/guides/prompts).

```bash
pip install wandb  
pip install pandas  
pip install textstat  
pip install spacy  
python -m spacy download en\_core\_web\_sm  

```

```python
import os  
  
os.environ["WANDB\_API\_KEY"] = ""  
# os.environ["OPENAI\_API\_KEY"] = ""  
# os.environ["SERPAPI\_API\_KEY"] = ""  

```

```python
from datetime import datetime  
from langchain.callbacks import WandbCallbackHandler, StdOutCallbackHandler  
from langchain.llms import OpenAI  

```

```text
Callback Handler that logs to Weights and Biases.  
  
Parameters:  
 job\_type (str): The type of job.  
 project (str): The project to log to.  
 entity (str): The entity to log to.  
 tags (list): The tags to log.  
 group (str): The group to log to.  
 name (str): The name of the run.  
 notes (str): The notes to log.  
 visualize (bool): Whether to visualize the run.  
 complexity\_metrics (bool): Whether to log complexity metrics.  
 stream\_logs (bool): Whether to stream callback actions to W&B  

```

```text
Default values for WandbCallbackHandler(...)  
  
visualize: bool = False,  
complexity\_metrics: bool = False,  
stream\_logs: bool = False,  

```

NOTE: For beta workflows we have made the default analysis based on textstat and the visualizations based on spacy

```python
"""Main function.  
  
This function is used to try the callback handler.  
Scenarios:  
1. OpenAI LLM  
2. Chain with multiple SubChains on multiple generations  
3. Agent with Tools  
"""  
session\_group = datetime.now().strftime("%m.%d.%Y\_%H.%M.%S")  
wandb\_callback = WandbCallbackHandler(  
 job\_type="inference",  
 project="langchain\_callback\_demo",  
 group=f"minimal\_{session\_group}",  
 name="llm",  
 tags=["test"],  
)  
callbacks = [StdOutCallbackHandler(), wandb\_callback]  
llm = OpenAI(temperature=0, callbacks=callbacks)  

```

```text
[34m[1mwandb[0m: Currently logged in as: [33mharrison-chase[0m. Use [1m`wandb login --relogin`[0m to force relogin  

```

```html
Tracking run with wandb version 0.14.0  

```

```html
Run data is saved locally in <code>/Users/harrisonchase/workplace/langchain/docs/ecosystem/wandb/run-20230318\_150408-e47j1914</code>  

```

```html
Syncing run <strong><a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/e47j1914' target="\_blank">llm</a></strong> to <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo' target="\_blank">Weights & Biases</a> (<a href='https://wandb.me/run' target="\_blank">docs</a>)<br/>  

```

```html
View project at <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo</a>  

```

```html
View run at <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/e47j1914' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/e47j1914</a>  

```

```text
[34m[1mwandb[0m: [33mWARNING[0m The wandb callback is currently in beta and is subject to change based on updates to `langchain`. Please report any issues to https://github.com/wandb/wandb/issues with the tag `langchain`.  

```

```text
# Defaults for WandbCallbackHandler.flush\_tracker(...)  
  
reset: bool = True,  
finish: bool = False,  

```

The `flush_tracker` function is used to log LangChain sessions to Weights & Biases. It takes in the LangChain module or agent, and logs at minimum the prompts and generations alongside the serialized form of the LangChain module to the specified Weights & Biases project. By default we reset the session as opposed to concluding the session outright.

```python
# SCENARIO 1 - LLM  
llm\_result = llm.generate(["Tell me a joke", "Tell me a poem"] \* 3)  
wandb\_callback.flush\_tracker(llm, name="simple\_sequential")  

```

```html
Waiting for W&B process to finish... <strong style="color:green">(success).</strong>  

```

```html
View run <strong style="color:#cdcd00">llm</strong> at: <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/e47j1914' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/e47j1914</a><br/>Synced 5 W&B file(s), 2 media file(s), 5 artifact file(s) and 0 other file(s)  

```

```html
Find logs at: <code>./wandb/run-20230318\_150408-e47j1914/logs</code>  

```

```text
VBox(children=(Label(value='Waiting for wandb.init()...\r'), FloatProgress(value=0.016745895149999985, max=1.0…  

```

```html
Tracking run with wandb version 0.14.0  

```

```html
Run data is saved locally in <code>/Users/harrisonchase/workplace/langchain/docs/ecosystem/wandb/run-20230318\_150534-jyxma7hu</code>  

```

```html
Syncing run <strong><a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/jyxma7hu' target="\_blank">simple\_sequential</a></strong> to <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo' target="\_blank">Weights & Biases</a> (<a href='https://wandb.me/run' target="\_blank">docs</a>)<br/>  

```

```html
View project at <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo</a>  

```

```html
View run at <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/jyxma7hu' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/jyxma7hu</a>  

```

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
# SCENARIO 2 - Chain  
template = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.  
Title: {title}  
Playwright: This is a synopsis for the above play:"""  
prompt\_template = PromptTemplate(input\_variables=["title"], template=template)  
synopsis\_chain = LLMChain(llm=llm, prompt=prompt\_template, callbacks=callbacks)  
  
test\_prompts = [  
 {  
 "title": "documentary about good video games that push the boundary of game design"  
 },  
 {"title": "cocaine bear vs heroin wolf"},  
 {"title": "the best in class mlops tooling"},  
]  
synopsis\_chain.apply(test\_prompts)  
wandb\_callback.flush\_tracker(synopsis\_chain, name="agent")  

```

```html
Waiting for W&B process to finish... <strong style="color:green">(success).</strong>  

```

```html
View run <strong style="color:#cdcd00">simple\_sequential</strong> at: <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/jyxma7hu' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/jyxma7hu</a><br/>Synced 4 W&B file(s), 2 media file(s), 6 artifact file(s) and 0 other file(s)  

```

```html
Find logs at: <code>./wandb/run-20230318\_150534-jyxma7hu/logs</code>  

```

```text
VBox(children=(Label(value='Waiting for wandb.init()...\r'), FloatProgress(value=0.016736786816666675, max=1.0…  

```

```html
Tracking run with wandb version 0.14.0  

```

```html
Run data is saved locally in <code>/Users/harrisonchase/workplace/langchain/docs/ecosystem/wandb/run-20230318\_150550-wzy59zjq</code>  

```

```html
Syncing run <strong><a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/wzy59zjq' target="\_blank">agent</a></strong> to <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo' target="\_blank">Weights & Biases</a> (<a href='https://wandb.me/run' target="\_blank">docs</a>)<br/>  

```

```html
View project at <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo</a>  

```

```html
View run at <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/wzy59zjq' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/wzy59zjq</a>  

```

```python
from langchain.agents import initialize\_agent, load\_tools  
from langchain.agents import AgentType  

```

```python
# SCENARIO 3 - Agent with Tools  
tools = load\_tools(["serpapi", "llm-math"], llm=llm)  
agent = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,  
)  
agent.run(  
 "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?",  
 callbacks=callbacks,  
)  
wandb\_callback.flush\_tracker(agent, reset=False, finish=True)  

```

```text
> Entering new AgentExecutor chain...  
 I need to find out who Leo DiCaprio's girlfriend is and then calculate her age raised to the 0.43 power.  
Action: Search  
Action Input: "Leo DiCaprio girlfriend"  
Observation: DiCaprio had a steady girlfriend in Camila Morrone. He had been with the model turned actress for nearly five years, as they were first said to be dating at the end of 2017. And the now 26-year-old Morrone is no stranger to Hollywood.  
Thought: I need to calculate her age raised to the 0.43 power.  
Action: Calculator  
Action Input: 26^0.43  
Observation: Answer: 4.059182145592686  
  
Thought: I now know the final answer.  
Final Answer: Leo DiCaprio's girlfriend is Camila Morrone and her current age raised to the 0.43 power is 4.059182145592686.  
  
> Finished chain.  

```

```html
Waiting for W&B process to finish... <strong style="color:green">(success).</strong>  

```

```html
View run <strong style="color:#cdcd00">agent</strong> at: <a href='https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/wzy59zjq' target="\_blank">https://wandb.ai/harrison-chase/langchain\_callback\_demo/runs/wzy59zjq</a><br/>Synced 5 W&B file(s), 2 media file(s), 7 artifact file(s) and 0 other file(s)  

```

```html
Find logs at: <code>./wandb/run-20230318\_150550-wzy59zjq/logs</code>  

```

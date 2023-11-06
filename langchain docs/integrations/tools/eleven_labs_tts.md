# Eleven Labs Text2Speech

This notebook shows how to interact with the `ElevenLabs API` to achieve text-to-speech capabilities.

First, you need to set up an ElevenLabs account. You can follow the instructions [here](https://docs.elevenlabs.io/welcome/introduction).

```python
# !pip install elevenlabs  

```

```python
import os  
  
os.environ["ELEVEN\_API\_KEY"] = ""  

```

## Usage[​](#usage "Direct link to Usage")

```python
from langchain.tools import ElevenLabsText2SpeechTool  
  
text\_to\_speak = "Hello world! I am the real slim shady"  
  
tts = ElevenLabsText2SpeechTool()  
tts.name  

```

```text
 'eleven\_labs\_text2speech'  

```

We can generate audio, save it to the temporary file and then play it.

```python
speech\_file = tts.run(text\_to\_speak)  
tts.play(speech\_file)  

```

Or stream audio directly.

```python
tts.stream\_speech(text\_to\_speak)  

```

## Use within an Agent[​](#use-within-an-agent "Direct link to Use within an Agent")

```python
from langchain.llms import OpenAI  
from langchain.agents import initialize\_agent, AgentType, load\_tools  

```

```python
llm = OpenAI(temperature=0)  
tools = load\_tools(["eleven\_labs\_text2speech"])  
agent = initialize\_agent(  
 tools=tools,  
 llm=llm,  
 agent=AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
)  

```

```python
audio\_file = agent.run("Tell me a joke and read it out for me.")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 Action:  
```

{\
"action": "eleven_labs_text2speech",\
"action_input": {\
"query": "Why did the chicken cross the playground? To get to the other slide!"\
}\
}

```
  
  
Observation: /tmp/tmpsfg783f1.wav  
Thought: I have the audio file ready to be sent to the human  
Action:  
```

{\
"action": "Final Answer",\
"action_input": "/tmp/tmpsfg783f1.wav"\
}

```
  
  
  
> Finished chain.  

```

```python
tts.play(audio\_file)  

```

- [Usage](#usage)
- [Use within an Agent](#use-within-an-agent)

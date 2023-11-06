# Log10

This page covers how to use the [Log10](https://log10.io) within LangChain.

## What is Log10?[​](#what-is-log10 "Direct link to What is Log10?")

Log10 is an [open-source](https://github.com/log10-io/log10) proxiless LLM data management and application development platform that lets you log, debug and tag your Langchain calls.

## Quick start[​](#quick-start "Direct link to Quick start")

1. Create your free account at [log10.io](https://log10.io)
1. Add your `LOG10_TOKEN` and `LOG10_ORG_ID` from the Settings and Organization tabs respectively as environment variables.
1. Also add `LOG10_URL=https://log10.io` and your usual LLM API key: for e.g. `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` to your environment

## How to enable Log10 data management for Langchain[​](#how-to-enable-log10-data-management-for-langchain "Direct link to How to enable Log10 data management for Langchain")

Integration with log10 is a simple one-line `log10_callback` integration as shown below:

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import HumanMessage  
  
from log10.langchain import Log10Callback  
from log10.llm import Log10Config  
  
log10\_callback = Log10Callback(log10\_config=Log10Config())  
  
messages = [  
 HumanMessage(content="You are a ping pong machine"),  
 HumanMessage(content="Ping?"),  
]  
  
llm = ChatOpenAI(model\_name="gpt-3.5-turbo", callbacks=[log10\_callback])  

```

[Log10 + Langchain + Logs docs](https://github.com/log10-io/log10/blob/main/logging.md#langchain-logger)

[More details + screenshots](https://log10.io/docs/logs) including instructions for self-hosting logs

## How to use tags with Log10[​](#how-to-use-tags-with-log10 "Direct link to How to use tags with Log10")

```python
from langchain.llms import OpenAI  
from langchain.chat\_models import ChatAnthropic  
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import HumanMessage  
  
from log10.langchain import Log10Callback  
from log10.llm import Log10Config  
  
log10\_callback = Log10Callback(log10\_config=Log10Config())  
  
messages = [  
 HumanMessage(content="You are a ping pong machine"),  
 HumanMessage(content="Ping?"),  
]  
  
llm = ChatOpenAI(model\_name="gpt-3.5-turbo", callbacks=[log10\_callback], temperature=0.5, tags=["test"])  
completion = llm.predict\_messages(messages, tags=["foobar"])  
print(completion)  
  
llm = ChatAnthropic(model="claude-2", callbacks=[log10\_callback], temperature=0.7, tags=["baz"])  
llm.predict\_messages(messages)  
print(completion)  
  
llm = OpenAI(model\_name="text-davinci-003", callbacks=[log10\_callback], temperature=0.5)  
completion = llm.predict("You are a ping pong machine.\nPing?\n")  
print(completion)  

```

You can also intermix direct OpenAI calls and Langchain LLM calls:

```python
import os  
from log10.load import log10, log10\_session  
import openai  
from langchain.llms import OpenAI  
  
log10(openai)  
  
with log10\_session(tags=["foo", "bar"]):  
 # Log a direct OpenAI call  
 response = openai.Completion.create(  
 model="text-ada-001",  
 prompt="Where is the Eiffel Tower?",  
 temperature=0,  
 max\_tokens=1024,  
 top\_p=1,  
 frequency\_penalty=0,  
 presence\_penalty=0,  
 )  
 print(response)  
  
 # Log a call via Langchain  
 llm = OpenAI(model\_name="text-ada-001", temperature=0.5)  
 response = llm.predict("You are a ping pong machine.\nPing?\n")  
 print(response)  

```

## How to debug Langchain calls[​](#how-to-debug-langchain-calls "Direct link to How to debug Langchain calls")

[Example of debugging](https://log10.io/docs/prompt_chain_debugging)

[More Langchain examples](https://github.com/log10-io/log10/tree/main/examples#langchain)

- [What is Log10?](#what-is-log10)
- [Quick start](#quick-start)
- [How to enable Log10 data management for Langchain](#how-to-enable-log10-data-management-for-langchain)
- [How to use tags with Log10](#how-to-use-tags-with-log10)
- [How to debug Langchain calls](#how-to-debug-langchain-calls)

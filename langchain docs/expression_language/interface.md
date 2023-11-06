# Interface

To make it as easy as possible to create custom chains, we've implemented a ["Runnable"](https://api.python.langchain.com/en/latest/schema/langchain.schema.runnable.base.Runnable.html#langchain.schema.runnable.base.Runnable) protocol. The `Runnable` protocol is implemented for most components. This is a standard interface, which makes it easy to define custom chains as well as invoke them in a standard way. The standard interface includes:

- [`stream`](#stream): stream back chunks of the response
- [`invoke`](#invoke): call the chain on an input
- [`batch`](#batch): call the chain on a list of inputs

These also have corresponding async methods:

- [`astream`](#async-stream): stream back chunks of the response async
- [`ainvoke`](#async-invoke): call the chain on an input async
- [`abatch`](#async-batch): call the chain on a list of inputs async
- [`astream_log`](#async-stream-intermediate-steps): stream back intermediate steps as they happen, in addition to the final response

The **input type** varies by component:

Component      | Input Type
-------------- | -----------------------------------------------------
Prompt         | Dictionary
Retriever      | Single string
LLM, ChatModel | Single string, list of chat messages or a PromptValue
Tool           | Single string, or dictionary, depending on the tool
OutputParser   | The output of an LLM or ChatModel

The **output type** also varies by component:

Component    | Output Type
------------ | ---------------------
LLM          | String
ChatModel    | ChatMessage
Prompt       | PromptValue
Retriever    | List of documents
Tool         | Depends on the tool
OutputParser | Depends on the parser

All runnables expose input and output **schemas** to inspect the inputs and outputs:

- [`input_schema`](#input-schema): an input Pydantic model auto-generated from the structure of the Runnable
- [`output_schema`](#output-schema): an output Pydantic model auto-generated from the structure of the Runnable

Let's take a look at these methods. To do so, we'll create a super simple PromptTemplate + ChatModel chain.

```python
from langchain.prompts import ChatPromptTemplate
from langchain.chat\_models import ChatOpenAI

model = ChatOpenAI()
prompt = ChatPromptTemplate.from\_template("tell me a joke about {topic}")
chain = prompt | model
```

## Input Schema[​](#input-schema "Direct link to Input Schema")

A description of the inputs accepted by a Runnable. This is a Pydantic model dynamically generated from the structure of any Runnable. You can call `.schema()` on it to obtain a JSONSchema representation.

```python
# The input schema of the chain is the input schema of its first part, the prompt.
chain.input\_schema.schema()
```

```text
{'title': 'PromptInput',
 'type': 'object',
 'properties': {'topic': {'title': 'Topic', 'type': 'string'}}}
```

```python
prompt.input\_schema.schema()
```

```text
{'title': 'PromptInput',
 'type': 'object',
 'properties': {'topic': {'title': 'Topic', 'type': 'string'}}}
```

```python
model.input\_schema.schema()
```

```text
{'title': 'ChatOpenAIInput',
 'anyOf': [{'type': 'string'},
 {'$ref': '#/definitions/StringPromptValue'},
 {'$ref': '#/definitions/ChatPromptValueConcrete'},
 {'type': 'array',
 'items': {'anyOf': [{'$ref': '#/definitions/AIMessage'},
 {'$ref': '#/definitions/HumanMessage'},
 {'$ref': '#/definitions/ChatMessage'},
 {'$ref': '#/definitions/SystemMessage'},
 {'$ref': '#/definitions/FunctionMessage'}]}}],
 'definitions': {'StringPromptValue': {'title': 'StringPromptValue',
 'description': 'String prompt value.',
 'type': 'object',
 'properties': {'text': {'title': 'Text', 'type': 'string'},
 'type': {'title': 'Type',
 'default': 'StringPromptValue',
 'enum': ['StringPromptValue'],
 'type': 'string'}},
 'required': ['text']},
 'AIMessage': {'title': 'AIMessage',
 'description': 'A Message from an AI.',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'ai',
 'enum': ['ai'],
 'type': 'string'},
 'example': {'title': 'Example', 'default': False, 'type': 'boolean'}},
 'required': ['content']},
 'HumanMessage': {'title': 'HumanMessage',
 'description': 'A Message from a human.',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'human',
 'enum': ['human'],
 'type': 'string'},
 'example': {'title': 'Example', 'default': False, 'type': 'boolean'}},
 'required': ['content']},
 'ChatMessage': {'title': 'ChatMessage',
 'description': 'A Message that can be assigned an arbitrary speaker (i.e. role).',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'chat',
 'enum': ['chat'],
 'type': 'string'},
 'role': {'title': 'Role', 'type': 'string'}},
 'required': ['content', 'role']},
 'SystemMessage': {'title': 'SystemMessage',
 'description': 'A Message for priming AI behavior, usually passed in as the first of a sequence\nof input messages.',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'system',
 'enum': ['system'],
 'type': 'string'}},
 'required': ['content']},
 'FunctionMessage': {'title': 'FunctionMessage',
 'description': 'A Message for passing the result of executing a function back to a model.',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'function',
 'enum': ['function'],
 'type': 'string'},
 'name': {'title': 'Name', 'type': 'string'}},
 'required': ['content', 'name']},
 'ChatPromptValueConcrete': {'title': 'ChatPromptValueConcrete',
 'description': 'Chat prompt value which explicitly lists out the message types it accepts.\nFor use in external schemas.',
 'type': 'object',
 'properties': {'messages': {'title': 'Messages',
 'type': 'array',
 'items': {'anyOf': [{'$ref': '#/definitions/AIMessage'},
 {'$ref': '#/definitions/HumanMessage'},
 {'$ref': '#/definitions/ChatMessage'},
 {'$ref': '#/definitions/SystemMessage'},
 {'$ref': '#/definitions/FunctionMessage'}]}},
 'type': {'title': 'Type',
 'default': 'ChatPromptValueConcrete',
 'enum': ['ChatPromptValueConcrete'],
 'type': 'string'}},
 'required': ['messages']}}}
```

## Output Schema[​](#output-schema "Direct link to Output Schema")

A description of the outputs produced by a Runnable. This is a Pydantic model dynamically generated from the structure of any Runnable. You can call `.schema()` on it to obtain a JSONSchema representation.

```python
# The output schema of the chain is the output schema of its last part, in this case a ChatModel, which outputs a ChatMessage
chain.output\_schema.schema()
```

```text
{'title': 'ChatOpenAIOutput',
 'anyOf': [{'$ref': '#/definitions/HumanMessage'},
 {'$ref': '#/definitions/AIMessage'},
 {'$ref': '#/definitions/ChatMessage'},
 {'$ref': '#/definitions/FunctionMessage'},
 {'$ref': '#/definitions/SystemMessage'}],
 'definitions': {'HumanMessage': {'title': 'HumanMessage',
 'description': 'A Message from a human.',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'human',
 'enum': ['human'],
 'type': 'string'},
 'example': {'title': 'Example', 'default': False, 'type': 'boolean'}},
 'required': ['content']},
 'AIMessage': {'title': 'AIMessage',
 'description': 'A Message from an AI.',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'ai',
 'enum': ['ai'],
 'type': 'string'},
 'example': {'title': 'Example', 'default': False, 'type': 'boolean'}},
 'required': ['content']},
 'ChatMessage': {'title': 'ChatMessage',
 'description': 'A Message that can be assigned an arbitrary speaker (i.e. role).',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'chat',
 'enum': ['chat'],
 'type': 'string'},
 'role': {'title': 'Role', 'type': 'string'}},
 'required': ['content', 'role']},
 'FunctionMessage': {'title': 'FunctionMessage',
 'description': 'A Message for passing the result of executing a function back to a model.',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'function',
 'enum': ['function'],
 'type': 'string'},
 'name': {'title': 'Name', 'type': 'string'}},
 'required': ['content', 'name']},
 'SystemMessage': {'title': 'SystemMessage',
 'description': 'A Message for priming AI behavior, usually passed in as the first of a sequence\nof input messages.',
 'type': 'object',
 'properties': {'content': {'title': 'Content', 'type': 'string'},
 'additional\_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
 'type': {'title': 'Type',
 'default': 'system',
 'enum': ['system'],
 'type': 'string'}},
 'required': ['content']}}}
```

## Stream[​](#stream "Direct link to Stream")

```python
for s in chain.stream({"topic": "bears"}):
 print(s.content, end="", flush=True)
```

```text
Why don't bears wear shoes?

 Because they already have bear feet!
```

## Invoke[​](#invoke "Direct link to Invoke")

```python
chain.invoke({"topic": "bears"})
```

```text
AIMessage(content="Why don't bears wear shoes?\n\nBecause they already have bear feet!")
```

## Batch[​](#batch "Direct link to Batch")

```python
chain.batch([{"topic": "bears"}, {"topic": "cats"}])
```

```text
[AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!"),
 AIMessage(content="Why don't cats play poker in the wild?\n\nToo many cheetahs!")]
```

You can set the number of concurrent requests by using the `max_concurrency` parameter

```python
chain.batch([{"topic": "bears"}, {"topic": "cats"}], config={"max\_concurrency": 5})
```

```text
[AIMessage(content="Why don't bears wear shoes? \n\nBecause they have bear feet!"),
 AIMessage(content="Why don't cats play poker in the wild?\n\nToo many cheetahs!")]
```

## Async Stream[​](#async-stream "Direct link to Async Stream")

```python
async for s in chain.astream({"topic": "bears"}):
 print(s.content, end="", flush=True)
```

```text
Sure, here's a bear-themed joke for you:

 Why don't bears wear shoes?

 Because they already have bear feet!
```

## Async Invoke[​](#async-invoke "Direct link to Async Invoke")

```python
await chain.ainvoke({"topic": "bears"})
```

```text
AIMessage(content="Why don't bears wear shoes? \n\nBecause they have bear feet!")
```

## Async Batch[​](#async-batch "Direct link to Async Batch")

```python
await chain.abatch([{"topic": "bears"}])
```

```text
[AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!")]
```

## Async Stream Intermediate Steps[​](#async-stream-intermediate-steps "Direct link to Async Stream Intermediate Steps")

All runnables also have a method `.astream_log()` which is used to stream (as they happen) all or part of the intermediate steps of your chain/sequence.

This is useful to show progress to the user, to use intermediate results, or to debug your chain.

You can stream all steps (default) or include/exclude steps by name, tags or metadata.

This method yields [JSONPatch](https://jsonpatch.com) ops that when applied in the same order as received build up the RunState.

```python
class LogEntry(TypedDict):
 id: str
 """ID of the sub-run."""
 name: str
 """Name of the object being run."""
 type: str
 """Type of the object being run, eg. prompt, chain, llm, etc."""
 tags: List[str]
 """List of tags for the run."""
 metadata: Dict[str, Any]
 """Key-value pairs of metadata for the run."""
 start\_time: str
 """ISO-8601 timestamp of when the run started."""

 streamed\_output\_str: List[str]
 """List of LLM tokens streamed by this run, if applicable."""
 final\_output: Optional[Any]
 """Final output of this run.
 Only available after the run has finished successfully."""
 end\_time: Optional[str]
 """ISO-8601 timestamp of when the run ended.
 Only available after the run has finished."""


class RunState(TypedDict):
 id: str
 """ID of the run."""
 streamed\_output: List[Any]
 """List of output chunks streamed by Runnable.stream()"""
 final\_output: Optional[Any]
 """Final output of the run, usually the result of aggregating (`+`) streamed\_output.
 Only available after the run has finished successfully."""

 logs: Dict[str, LogEntry]
 """Map of run names to sub-runs. If filters were supplied, this list will
 contain only the runs that matched the filters."""
```

### Streaming JSONPatch chunks[​](#streaming-jsonpatch-chunks "Direct link to Streaming JSONPatch chunks")

This is useful eg. to stream the `JSONPatch` in an HTTP server, and then apply the ops on the client to rebuild the run state there. See [LangServe](https://github.com/langchain-ai/langserve) for tooling to make it easier to build a webserver from any Runnable.

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.output\_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import FAISS

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from\_template(template)

vectorstore = FAISS.from\_texts(["harrison worked at kensho"], embedding=OpenAIEmbeddings())
retriever = vectorstore.as\_retriever()

retrieval\_chain = (
 {"context": retriever.with\_config(run\_name='Docs'), "question": RunnablePassthrough()}
 | prompt
 | model
 | StrOutputParser()
)

async for chunk in retrieval\_chain.astream\_log("where did harrison work?", include\_names=['Docs']):
 print("-"\*40)
 print(chunk)
```

```text
----------------------------------------
 RunLogPatch({'op': 'replace',
 'path': '',
 'value': {'final\_output': None,
 'id': 'e2f2cc72-eb63-4d20-8326-237367482efb',
 'logs': {},
 'streamed\_output': []}})
 ----------------------------------------
 RunLogPatch({'op': 'add',
 'path': '/logs/Docs',
 'value': {'end\_time': None,
 'final\_output': None,
 'id': '8da492cc-4492-4e74-b8b0-9e60e8693390',
 'metadata': {},
 'name': 'Docs',
 'start\_time': '2023-10-19T17:50:13.526',
 'streamed\_output\_str': [],
 'tags': ['map:key:context', 'FAISS'],
 'type': 'retriever'}})
 ----------------------------------------
 RunLogPatch({'op': 'add',
 'path': '/logs/Docs/final\_output',
 'value': {'documents': [Document(page\_content='harrison worked at kensho')]}},
 {'op': 'add',
 'path': '/logs/Docs/end\_time',
 'value': '2023-10-19T17:50:13.713'})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': ''})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': 'H'})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': 'arrison'})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': ' worked'})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': ' at'})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': ' Kens'})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': 'ho'})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': '.'})
 ----------------------------------------
 RunLogPatch({'op': 'add', 'path': '/streamed\_output/-', 'value': ''})
 ----------------------------------------
 RunLogPatch({'op': 'replace',
 'path': '/final\_output',
 'value': {'output': 'Harrison worked at Kensho.'}})
```

### Streaming the incremental RunState[​](#streaming-the-incremental-runstate "Direct link to Streaming the incremental RunState")

You can simply pass `diff=False` to get incremental values of `RunState`. You get more verbose output with more repetitive parts.

```python
async for chunk in retrieval\_chain.astream\_log("where did harrison work?", include\_names=['Docs'], diff=False):
 print("-"\*70)
 print(chunk)
```

## Parallelism[​](#parallelism "Direct link to Parallelism")

Let's take a look at how LangChain Expression Language supports parallel requests. For example, when using a `RunnableParallel` (often written as a dictionary) it executes each element in parallel.

```python
from langchain.schema.runnable import RunnableParallel
chain1 = ChatPromptTemplate.from\_template("tell me a joke about {topic}") | model
chain2 = ChatPromptTemplate.from\_template("write a short (2 line) poem about {topic}") | model
combined = RunnableParallel(joke=chain1, poem=chain2)
```

```python
chain1.invoke({"topic": "bears"})
```

```text
CPU times: user 54.3 ms, sys: 0 ns, total: 54.3 ms
 Wall time: 2.29 s

 AIMessage(content="Why don't bears wear shoes?\n\nBecause they already have bear feet!")
```

```python
chain2.invoke({"topic": "bears"})
```

```text
CPU times: user 7.8 ms, sys: 0 ns, total: 7.8 ms
 Wall time: 1.43 s

 AIMessage(content="In wild embrace,\nNature's strength roams with grace.")
```

```python
combined.invoke({"topic": "bears"})
```

```text
CPU times: user 167 ms, sys: 921 µs, total: 168 ms
 Wall time: 1.56 s

 {'joke': AIMessage(content="Why don't bears wear shoes?\n\nBecause they already have bear feet!"),
 'poem': AIMessage(content="Fierce and wild, nature's might,\nBears roam the woods, shadows of the night.")}
```

### Parallelism on batches[​](#parallelism-on-batches "Direct link to Parallelism on batches")

Parallelism can be combined with other runnables. Let's try to use parallelism with batches.

```python
chain1.batch([{"topic": "bears"}, {"topic": "cats"}])
```

```text
CPU times: user 159 ms, sys: 3.66 ms, total: 163 ms
 Wall time: 1.34 s

 [AIMessage(content="Why don't bears wear shoes?\n\nBecause they already have bear feet!"),
 AIMessage(content="Sure, here's a cat joke for you:\n\nWhy don't cats play poker in the wild?\n\nBecause there are too many cheetahs!")]
```

```python
chain2.batch([{"topic": "bears"}, {"topic": "cats"}])
```

```text
CPU times: user 165 ms, sys: 0 ns, total: 165 ms
 Wall time: 1.73 s

 [AIMessage(content="Silent giants roam,\nNature's strength, love's emblem shown."),
 AIMessage(content='Whiskers aglow, paws tiptoe,\nGraceful hunters, hearts aglow.')]
```

```python
combined.batch([{"topic": "bears"}, {"topic": "cats"}])
```

```text
CPU times: user 507 ms, sys: 125 ms, total: 632 ms
 Wall time: 1.49 s

 [{'joke': AIMessage(content="Why don't bears wear shoes?\n\nBecause they already have bear feet!"),
 'poem': AIMessage(content="Majestic bears roam,\nNature's wild guardians of home.")},
 {'joke': AIMessage(content="Sure, here's a cat joke for you:\n\nWhy did the cat sit on the computer?\n\nBecause it wanted to keep an eye on the mouse!"),
 'poem': AIMessage(content='Whiskers twitch, eyes gleam,\nGraceful creatures, feline dream.')}]
```

- [Input Schema](#input-schema)

- [Output Schema](#output-schema)

- [Stream](#stream)

- [Invoke](#invoke)

- [Batch](#batch)

- [Async Stream](#async-stream)

- [Async Invoke](#async-invoke)

- [Async Batch](#async-batch)

- [Async Stream Intermediate Steps](#async-stream-intermediate-steps)

  - [Streaming JSONPatch chunks](#streaming-jsonpatch-chunks)
  - [Streaming the incremental RunState](#streaming-the-incremental-runstate)

- [Parallelism](#parallelism)

  - [Parallelism on batches](#parallelism-on-batches)

- [Streaming JSONPatch chunks](#streaming-jsonpatch-chunks)

- [Streaming the incremental RunState](#streaming-the-incremental-runstate)

- [Parallelism on batches](#parallelism-on-batches)

# JSON

[JSON (JavaScript Object Notation)](https://en.wikipedia.org/wiki/JSON) is an open standard file format and data interchange format that uses human-readable text to store and transmit data objects consisting of attribute–value pairs and arrays (or other serializable values).

[JSON Lines](https://jsonlines.org/) is a file format where each line is a valid JSON value.

The `JSONLoader` uses a specified [jq schema](<https://en.wikipedia.org/wiki/Jq_(programming_language)>) to parse the JSON files. It uses the `jq` python package.
Check this [manual](https://stedolan.github.io/jq/manual/#Basicfilters) for a detailed documentation of the `jq` syntax.

```python
#!pip install jq  

```

```python
from langchain.document\_loaders import JSONLoader  

```

```python
import json  
from pathlib import Path  
from pprint import pprint  
  
  
file\_path='./example\_data/facebook\_chat.json'  
data = json.loads(Path(file\_path).read\_text())  

```

```python
pprint(data)  

```

```text
 {'image': {'creation\_timestamp': 1675549016, 'uri': 'image\_of\_the\_chat.jpg'},  
 'is\_still\_participant': True,  
 'joinable\_mode': {'link': '', 'mode': 1},  
 'magic\_words': [],  
 'messages': [{'content': 'Bye!',  
 'sender\_name': 'User 2',  
 'timestamp\_ms': 1675597571851},  
 {'content': 'Oh no worries! Bye',  
 'sender\_name': 'User 1',  
 'timestamp\_ms': 1675597435669},  
 {'content': 'No Im sorry it was my mistake, the blue one is not '  
 'for sale',  
 'sender\_name': 'User 2',  
 'timestamp\_ms': 1675596277579},  
 {'content': 'I thought you were selling the blue one!',  
 'sender\_name': 'User 1',  
 'timestamp\_ms': 1675595140251},  
 {'content': 'Im not interested in this bag. Im interested in the '  
 'blue one!',  
 'sender\_name': 'User 1',  
 'timestamp\_ms': 1675595109305},  
 {'content': 'Here is $129',  
 'sender\_name': 'User 2',  
 'timestamp\_ms': 1675595068468},  
 {'photos': [{'creation\_timestamp': 1675595059,  
 'uri': 'url\_of\_some\_picture.jpg'}],  
 'sender\_name': 'User 2',  
 'timestamp\_ms': 1675595060730},  
 {'content': 'Online is at least $100',  
 'sender\_name': 'User 2',  
 'timestamp\_ms': 1675595045152},  
 {'content': 'How much do you want?',  
 'sender\_name': 'User 1',  
 'timestamp\_ms': 1675594799696},  
 {'content': 'Goodmorning! $50 is too low.',  
 'sender\_name': 'User 2',  
 'timestamp\_ms': 1675577876645},  
 {'content': 'Hi! Im interested in your bag. Im offering $50. Let '  
 'me know if you are interested. Thanks!',  
 'sender\_name': 'User 1',  
 'timestamp\_ms': 1675549022673}],  
 'participants': [{'name': 'User 1'}, {'name': 'User 2'}],  
 'thread\_path': 'inbox/User 1 and User 2 chat',  
 'title': 'User 1 and User 2 chat'}  

```

## Using `JSONLoader`[​](#using-jsonloader "Direct link to using-jsonloader")

Suppose we are interested in extracting the values under the `content` field within the `messages` key of the JSON data. This can easily be done through the `JSONLoader` as shown below.

### JSON file[​](#json-file "Direct link to JSON file")

```python
loader = JSONLoader(  
 file\_path='./example\_data/facebook\_chat.json',  
 jq\_schema='.messages[].content',  
 text\_content=False)  
  
data = loader.load()  

```

```python
pprint(data)  

```

```text
 [Document(page\_content='Bye!', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 1}),  
 Document(page\_content='Oh no worries! Bye', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 2}),  
 Document(page\_content='No Im sorry it was my mistake, the blue one is not for sale', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 3}),  
 Document(page\_content='I thought you were selling the blue one!', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 4}),  
 Document(page\_content='Im not interested in this bag. Im interested in the blue one!', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 5}),  
 Document(page\_content='Here is $129', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 6}),  
 Document(page\_content='', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 7}),  
 Document(page\_content='Online is at least $100', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 8}),  
 Document(page\_content='How much do you want?', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 9}),  
 Document(page\_content='Goodmorning! $50 is too low.', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 10}),  
 Document(page\_content='Hi! Im interested in your bag. Im offering $50. Let me know if you are interested. Thanks!', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 11})]  

```

### JSON Lines file[​](#json-lines-file "Direct link to JSON Lines file")

If you want to load documents from a JSON Lines file, you pass `json_lines=True`
and specify `jq_schema` to extract `page_content` from a single JSON object.

```python
file\_path = './example\_data/facebook\_chat\_messages.jsonl'  
pprint(Path(file\_path).read\_text())  

```

```text
 ('{"sender\_name": "User 2", "timestamp\_ms": 1675597571851, "content": "Bye!"}\n'  
 '{"sender\_name": "User 1", "timestamp\_ms": 1675597435669, "content": "Oh no '  
 'worries! Bye"}\n'  
 '{"sender\_name": "User 2", "timestamp\_ms": 1675596277579, "content": "No Im '  
 'sorry it was my mistake, the blue one is not for sale"}\n')  

```

```python
loader = JSONLoader(  
 file\_path='./example\_data/facebook\_chat\_messages.jsonl',  
 jq\_schema='.content',  
 text\_content=False,  
 json\_lines=True)  
  
data = loader.load()  

```

```python
pprint(data)  

```

```text
 [Document(page\_content='Bye!', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat\_messages.jsonl', 'seq\_num': 1}),  
 Document(page\_content='Oh no worries! Bye', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat\_messages.jsonl', 'seq\_num': 2}),  
 Document(page\_content='No Im sorry it was my mistake, the blue one is not for sale', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat\_messages.jsonl', 'seq\_num': 3})]  

```

Another option is set `jq_schema='.'` and provide `content_key`:

```python
loader = JSONLoader(  
 file\_path='./example\_data/facebook\_chat\_messages.jsonl',  
 jq\_schema='.',  
 content\_key='sender\_name',  
 json\_lines=True)  
  
data = loader.load()  

```

```python
pprint(data)  

```

```text
 [Document(page\_content='User 2', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat\_messages.jsonl', 'seq\_num': 1}),  
 Document(page\_content='User 1', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat\_messages.jsonl', 'seq\_num': 2}),  
 Document(page\_content='User 2', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat\_messages.jsonl', 'seq\_num': 3})]  

```

## Extracting metadata[​](#extracting-metadata "Direct link to Extracting metadata")

Generally, we want to include metadata available in the JSON file into the documents that we create from the content.

The following demonstrates how metadata can be extracted using the `JSONLoader`.

There are some key changes to be noted. In the previous example where we didn't collect the metadata, we managed to directly specify in the schema where the value for the `page_content` can be extracted from.

```text
.messages[].content  

```

In the current example, we have to tell the loader to iterate over the records in the `messages` field. The jq_schema then has to be:

```text
.messages[]  

```

This allows us to pass the records (dict) into the `metadata_func` that has to be implemented. The `metadata_func` is responsible for identifying which pieces of information in the record should be included in the metadata stored in the final `Document` object.

Additionally, we now have to explicitly specify in the loader, via the `content_key` argument, the key from the record where the value for the `page_content` needs to be extracted from.

```python
# Define the metadata extraction function.  
def metadata\_func(record: dict, metadata: dict) -> dict:  
  
 metadata["sender\_name"] = record.get("sender\_name")  
 metadata["timestamp\_ms"] = record.get("timestamp\_ms")  
  
 return metadata  
  
  
loader = JSONLoader(  
 file\_path='./example\_data/facebook\_chat.json',  
 jq\_schema='.messages[]',  
 content\_key="content",  
 metadata\_func=metadata\_func  
)  
  
data = loader.load()  

```

```python
pprint(data)  

```

```text
 [Document(page\_content='Bye!', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 1, 'sender\_name': 'User 2', 'timestamp\_ms': 1675597571851}),  
 Document(page\_content='Oh no worries! Bye', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 2, 'sender\_name': 'User 1', 'timestamp\_ms': 1675597435669}),  
 Document(page\_content='No Im sorry it was my mistake, the blue one is not for sale', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 3, 'sender\_name': 'User 2', 'timestamp\_ms': 1675596277579}),  
 Document(page\_content='I thought you were selling the blue one!', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 4, 'sender\_name': 'User 1', 'timestamp\_ms': 1675595140251}),  
 Document(page\_content='Im not interested in this bag. Im interested in the blue one!', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 5, 'sender\_name': 'User 1', 'timestamp\_ms': 1675595109305}),  
 Document(page\_content='Here is $129', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 6, 'sender\_name': 'User 2', 'timestamp\_ms': 1675595068468}),  
 Document(page\_content='', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 7, 'sender\_name': 'User 2', 'timestamp\_ms': 1675595060730}),  
 Document(page\_content='Online is at least $100', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 8, 'sender\_name': 'User 2', 'timestamp\_ms': 1675595045152}),  
 Document(page\_content='How much do you want?', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 9, 'sender\_name': 'User 1', 'timestamp\_ms': 1675594799696}),  
 Document(page\_content='Goodmorning! $50 is too low.', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 10, 'sender\_name': 'User 2', 'timestamp\_ms': 1675577876645}),  
 Document(page\_content='Hi! Im interested in your bag. Im offering $50. Let me know if you are interested. Thanks!', metadata={'source': '/Users/avsolatorio/WBG/langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 11, 'sender\_name': 'User 1', 'timestamp\_ms': 1675549022673})]  

```

Now, you will see that the documents contain the metadata associated with the content we extracted.

## The `metadata_func`[​](#the-metadata_func "Direct link to the-metadata_func")

As shown above, the `metadata_func` accepts the default metadata generated by the `JSONLoader`. This allows full control to the user with respect to how the metadata is formatted.

For example, the default metadata contains the `source` and the `seq_num` keys. However, it is possible that the JSON data contain these keys as well. The user can then exploit the `metadata_func` to rename the default keys and use the ones from the JSON data.

The example below shows how we can modify the `source` to only contain information of the file source relative to the `langchain` directory.

```python
# Define the metadata extraction function.  
def metadata\_func(record: dict, metadata: dict) -> dict:  
  
 metadata["sender\_name"] = record.get("sender\_name")  
 metadata["timestamp\_ms"] = record.get("timestamp\_ms")  
  
 if "source" in metadata:  
 source = metadata["source"].split("/")  
 source = source[source.index("langchain"):]  
 metadata["source"] = "/".join(source)  
  
 return metadata  
  
  
loader = JSONLoader(  
 file\_path='./example\_data/facebook\_chat.json',  
 jq\_schema='.messages[]',  
 content\_key="content",  
 metadata\_func=metadata\_func  
)  
  
data = loader.load()  

```

```python
pprint(data)  

```

```text
 [Document(page\_content='Bye!', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 1, 'sender\_name': 'User 2', 'timestamp\_ms': 1675597571851}),  
 Document(page\_content='Oh no worries! Bye', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 2, 'sender\_name': 'User 1', 'timestamp\_ms': 1675597435669}),  
 Document(page\_content='No Im sorry it was my mistake, the blue one is not for sale', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 3, 'sender\_name': 'User 2', 'timestamp\_ms': 1675596277579}),  
 Document(page\_content='I thought you were selling the blue one!', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 4, 'sender\_name': 'User 1', 'timestamp\_ms': 1675595140251}),  
 Document(page\_content='Im not interested in this bag. Im interested in the blue one!', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 5, 'sender\_name': 'User 1', 'timestamp\_ms': 1675595109305}),  
 Document(page\_content='Here is $129', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 6, 'sender\_name': 'User 2', 'timestamp\_ms': 1675595068468}),  
 Document(page\_content='', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 7, 'sender\_name': 'User 2', 'timestamp\_ms': 1675595060730}),  
 Document(page\_content='Online is at least $100', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 8, 'sender\_name': 'User 2', 'timestamp\_ms': 1675595045152}),  
 Document(page\_content='How much do you want?', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 9, 'sender\_name': 'User 1', 'timestamp\_ms': 1675594799696}),  
 Document(page\_content='Goodmorning! $50 is too low.', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 10, 'sender\_name': 'User 2', 'timestamp\_ms': 1675577876645}),  
 Document(page\_content='Hi! Im interested in your bag. Im offering $50. Let me know if you are interested. Thanks!', metadata={'source': 'langchain/docs/modules/indexes/document\_loaders/examples/example\_data/facebook\_chat.json', 'seq\_num': 11, 'sender\_name': 'User 1', 'timestamp\_ms': 1675549022673})]  

```

## Common JSON structures with jq schema[​](#common-json-structures-with-jq-schema "Direct link to Common JSON structures with jq schema")

The list below provides a reference to the possible `jq_schema` the user can use to extract content from the JSON data depending on the structure.

```text
JSON -> [{"text": ...}, {"text": ...}, {"text": ...}]  
jq\_schema -> ".[].text"  
  
JSON -> {"key": [{"text": ...}, {"text": ...}, {"text": ...}]}  
jq\_schema -> ".key[].text"  
  
JSON -> ["...", "...", "..."]  
jq\_schema -> ".[]"  

```

- [Using `JSONLoader`](#using-jsonloader)

  - [JSON file](#json-file)
  - [JSON Lines file](#json-lines-file)

- [Extracting metadata](#extracting-metadata)

- [The `metadata_func`](#the-metadata_func)

- [Common JSON structures with jq schema](#common-json-structures-with-jq-schema)

- [JSON file](#json-file)

- [JSON Lines file](#json-lines-file)

# Airbyte CDK

[Airbyte](https://github.com/airbytehq/airbyte) is a data integration platform for ELT pipelines from APIs, databases & files to warehouses & lakes. It has the largest catalog of ELT connectors to data warehouses and databases.

A lot of source connectors are implemented using the [Airbyte CDK](https://docs.airbyte.com/connector-development/cdk-python/). This loader allows to run any of these connectors and return the data as documents.

## Installation[​](#installation "Direct link to Installation")

First, you need to install the `airbyte-cdk` python package.

```python
#!pip install airbyte-cdk  

```

Then, either install an existing connector from the [Airbyte Github repository](https://github.com/airbytehq/airbyte/tree/master/airbyte-integrations/connectors) or create your own connector using the [Airbyte CDK](https://docs.airbyte.io/connector-development/connector-development).

For example, to install the Github connector, run

```python
#!pip install "source\_github@git+https://github.com/airbytehq/airbyte.git@master#subdirectory=airbyte-integrations/connectors/source-github"  

```

Some sources are also published as regular packages on PyPI

## Example[​](#example "Direct link to Example")

Now you can create an `AirbyteCDKLoader` based on the imported source. It takes a `config` object that's passed to the connector. You also have to pick the stream you want to retrieve records from by name (`stream_name`). Check the connectors documentation page and spec definition for more information on the config object and available streams. For the Github connectors these are:

- <https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-github/source_github/spec.json>.
- <https://docs.airbyte.com/integrations/sources/github/>

```python
from langchain.document\_loaders.airbyte import AirbyteCDKLoader  
from source\_github.source import SourceGithub # plug in your own source here  
  
config = {  
 # your github configuration  
 "credentials": {  
 "api\_url": "api.github.com",  
 "personal\_access\_token": "<token>"  
 },  
 "repository": "<repo>",  
 "start\_date": "<date from which to start retrieving records from in ISO format, e.g. 2020-10-20T00:00:00Z>"  
}  
  
issues\_loader = AirbyteCDKLoader(source\_class=SourceGithub, config=config, stream\_name="issues")  

```

Now you can load documents the usual way

```python
docs = issues\_loader.load()  

```

As `load` returns a list, it will block until all documents are loaded. To have better control over this process, you can also you the `lazy_load` method which returns an iterator instead:

```python
docs\_iterator = issues\_loader.lazy\_load()  

```

Keep in mind that by default the page content is empty and the metadata object contains all the information from the record. To create documents in a different, pass in a record_handler function when creating the loader:

```python
from langchain.docstore.document import Document  
  
def handle\_record(record, id):  
 return Document(page\_content=record.data["title"] + "\n" + (record.data["body"] or ""), metadata=record.data)  
  
issues\_loader = AirbyteCDKLoader(source\_class=SourceGithub, config=config, stream\_name="issues", record\_handler=handle\_record)  
  
docs = issues\_loader.load()  

```

## Incremental loads[​](#incremental-loads "Direct link to Incremental loads")

Some streams allow incremental loading, this means the source keeps track of synced records and won't load them again. This is useful for sources that have a high volume of data and are updated frequently.

To take advantage of this, store the `last_state` property of the loader and pass it in when creating the loader again. This will ensure that only new records are loaded.

```python
last\_state = issues\_loader.last\_state # store safely  
  
incremental\_issue\_loader = AirbyteCDKLoader(source\_class=SourceGithub, config=config, stream\_name="issues", state=last\_state)  
  
new\_docs = incremental\_issue\_loader.load()  

```

- [Installation](#installation)
- [Example](#example)
- [Incremental loads](#incremental-loads)

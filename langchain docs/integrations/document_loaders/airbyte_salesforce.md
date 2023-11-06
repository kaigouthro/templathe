# Airbyte Salesforce

[Airbyte](https://github.com/airbytehq/airbyte) is a data integration platform for ELT pipelines from APIs, databases & files to warehouses & lakes. It has the largest catalog of ELT connectors to data warehouses and databases.

This loader exposes the Salesforce connector as a document loader, allowing you to load various Salesforce objects as documents.

## Installation[​](#installation "Direct link to Installation")

First, you need to install the `airbyte-source-salesforce` python package.

```python
#!pip install airbyte-source-salesforce  

```

## Example[​](#example "Direct link to Example")

Check out the [Airbyte documentation page](https://docs.airbyte.com/integrations/sources/salesforce/) for details about how to configure the reader.
The JSON schema the config object should adhere to can be found on Github: <https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-salesforce/source_salesforce/spec.yaml>.

The general shape looks like this:

```python
{  
 "client\_id": "<oauth client id>",  
 "client\_secret": "<oauth client secret>",  
 "refresh\_token": "<oauth refresh token>",  
 "start\_date": "<date from which to start retrieving records from in ISO format, e.g. 2020-10-20T00:00:00Z>",  
 "is\_sandbox": False, # set to True if you're using a sandbox environment  
 "streams\_criteria": [ # Array of filters for salesforce objects that should be loadable  
 {"criteria": "exacts", "value": "Account"}, # Exact name of salesforce object  
 {"criteria": "starts with", "value": "Asset"}, # Prefix of the name  
 # Other allowed criteria: ends with, contains, starts not with, ends not with, not contains, not exacts  
 ],  
}  

```

By default all fields are stored as metadata in the documents and the text is set to an empty string. Construct the text of the document by transforming the documents returned by the reader.

```python
from langchain.document\_loaders.airbyte import AirbyteSalesforceLoader  
  
config = {  
 # your salesforce configuration  
}  
  
loader = AirbyteSalesforceLoader(config=config, stream\_name="asset") # check the documentation linked above for a list of all streams  

```

Now you can load documents the usual way

```python
docs = loader.load()  

```

As `load` returns a list, it will block until all documents are loaded. To have better control over this process, you can also you the `lazy_load` method which returns an iterator instead:

```python
docs\_iterator = loader.lazy\_load()  

```

Keep in mind that by default the page content is empty and the metadata object contains all the information from the record. To create documents in a different, pass in a record_handler function when creating the loader:

```python
from langchain.docstore.document import Document  
  
def handle\_record(record, id):  
 return Document(page\_content=record.data["title"], metadata=record.data)  
  
loader = AirbyteSalesforceLoader(config=config, record\_handler=handle\_record, stream\_name="asset")  
docs = loader.load()  

```

## Incremental loads[​](#incremental-loads "Direct link to Incremental loads")

Some streams allow incremental loading, this means the source keeps track of synced records and won't load them again. This is useful for sources that have a high volume of data and are updated frequently.

To take advantage of this, store the `last_state` property of the loader and pass it in when creating the loader again. This will ensure that only new records are loaded.

```python
last\_state = loader.last\_state # store safely  
  
incremental\_loader = AirbyteSalesforceLoader(config=config, stream\_name="asset", state=last\_state)  
  
new\_docs = incremental\_loader.load()  

```

- [Installation](#installation)
- [Example](#example)
- [Incremental loads](#incremental-loads)

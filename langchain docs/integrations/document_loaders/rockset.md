# Rockset

Rockset is a real-time analytics database which enables queries on massive, semi-structured data without operational burden. With Rockset, ingested data is queryable within one second and analytical queries against that data typically execute in milliseconds. Rockset is compute optimized, making it suitable for serving high concurrency applications in the sub-100TB range (or larger than 100s of TBs with rollups).

This notebook demonstrates how to use Rockset as a document loader in langchain. To get started, make sure you have a Rockset account and an API key available.

## Setting up the environment[​](#setting-up-the-environment "Direct link to Setting up the environment")

1. Go to the [Rockset console](https://console.rockset.com/apikeys) and get an API key. Find your API region from the [API reference](https://rockset.com/docs/rest-api/#introduction). For the purpose of this notebook, we will assume you're using Rockset from `Oregon(us-west-2)`.
1. Set your the environment variable `ROCKSET_API_KEY`.
1. Install the Rockset python client, which will be used by langchain to interact with the Rockset database.

```python
$ pip3 install rockset  

```

# Loading Documents

The Rockset integration with LangChain allows you to load documents from Rockset collections with SQL queries. In order to do this you must construct a `RocksetLoader` object. Here is an example snippet that initializes a `RocksetLoader`.

```python
from langchain.document\_loaders import RocksetLoader  
from rockset import RocksetClient, Regions, models  
  
loader = RocksetLoader(  
 RocksetClient(Regions.usw2a1, "<api key>"),  
 models.QueryRequestSql(query="SELECT \* FROM langchain\_demo LIMIT 3"), # SQL query  
 ["text"], # content columns  
 metadata\_keys=["id", "date"], # metadata columns  
)  

```

Here, you can see that the following query is run:

```sql
SELECT \* FROM langchain\_demo LIMIT 3  

```

The `text` column in the collection is used as the page content, and the record's `id` and `date` columns are used as metadata (if you do not pass anything into `metadata_keys`, the whole Rockset document will be used as metadata).

To execute the query and access an iterator over the resulting `Document`s, run:

```python
loader.lazy\_load()  

```

To execute the query and access all resulting `Document`s at once, run:

```python
loader.load()  

```

Here is an example response of `loader.load()`:

```python
[  
 Document(  
 page\_content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas a libero porta, dictum ipsum eget, hendrerit neque. Morbi blandit, ex ut suscipit viverra, enim velit tincidunt tellus, a tempor velit nunc et ex. Proin hendrerit odio nec convallis lobortis. Aenean in purus dolor. Vestibulum orci orci, laoreet eget magna in, commodo euismod justo.",   
 metadata={"id": 83209, "date": "2022-11-13T18:26:45.000000Z"}  
 ),  
 Document(  
 page\_content="Integer at finibus odio. Nam sit amet enim cursus lacus gravida feugiat vestibulum sed libero. Aenean eleifend est quis elementum tincidunt. Curabitur sit amet ornare erat. Nulla id dolor ut magna volutpat sodales fringilla vel ipsum. Donec ultricies, lacus sed fermentum dignissim, lorem elit aliquam ligula, sed suscipit sapien purus nec ligula.",   
 metadata={"id": 89313, "date": "2022-11-13T18:28:53.000000Z"}  
 ),  
 Document(  
 page\_content="Morbi tortor enim, commodo id efficitur vitae, fringilla nec mi. Nullam molestie faucibus aliquet. Praesent a est facilisis, condimentum justo sit amet, viverra erat. Fusce volutpat nisi vel purus blandit, et facilisis felis accumsan. Phasellus luctus ligula ultrices tellus tempor hendrerit. Donec at ultricies leo.",   
 metadata={"id": 87732, "date": "2022-11-13T18:49:04.000000Z"}  
 )  
]  

```

## Using multiple columns as content[​](#using-multiple-columns-as-content "Direct link to Using multiple columns as content")

You can choose to use multiple columns as content:

```python
from langchain.document\_loaders import RocksetLoader  
from rockset import RocksetClient, Regions, models  
  
loader = RocksetLoader(  
 RocksetClient(Regions.usw2a1, "<api key>"),  
 models.QueryRequestSql(query="SELECT \* FROM langchain\_demo LIMIT 1 WHERE id=38"),  
 ["sentence1", "sentence2"], # TWO content columns  
)  

```

Assuming the "sentence1" field is `"This is the first sentence."` and the "sentence2" field is `"This is the second sentence."`, the `page_content` of the resulting `Document` would be:

```text
This is the first sentence.  
This is the second sentence.  

```

You can define you own function to join content columns by setting the `content_columns_joiner` argument in the `RocksetLoader` constructor. `content_columns_joiner` is a method that takes in a `List[Tuple[str, Any]]]` as an argument, representing a list of tuples of (column name, column value). By default, this is a method that joins each column value with a new line.

For example, if you wanted to join sentence1 and sentence2 with a space instead of a new line, you could set `content_columns_joiner` like so:

```python
RocksetLoader(  
 RocksetClient(Regions.usw2a1, "<api key>"),  
 models.QueryRequestSql(query="SELECT \* FROM langchain\_demo LIMIT 1 WHERE id=38"),  
 ["sentence1", "sentence2"],  
 content\_columns\_joiner=lambda docs: " ".join(  
 [doc[1] for doc in docs]  
 ), # join with space instead of /n  
)  

```

The `page_content` of the resulting `Document` would be:

```text
This is the first sentence. This is the second sentence.  

```

Oftentimes you want to include the column name in the `page_content`. You can do that like this:

```python
RocksetLoader(  
 RocksetClient(Regions.usw2a1, "<api key>"),  
 models.QueryRequestSql(query="SELECT \* FROM langchain\_demo LIMIT 1 WHERE id=38"),  
 ["sentence1", "sentence2"],  
 content\_columns\_joiner=lambda docs: "\n".join(  
 [f"{doc[0]}: {doc[1]}" for doc in docs]  
 ),  
)  

```

This would result in the following `page_content`:

```text
sentence1: This is the first sentence.  
sentence2: This is the second sentence.  

```

- [Setting up the environment](#setting-up-the-environment)
- [Using multiple columns as content](#using-multiple-columns-as-content)

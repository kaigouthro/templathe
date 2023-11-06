# MongoDB

[MongoDB](https://www.mongodb.com/) is a NoSQL , document-oriented database that supports JSON-like documents with a dynamic schema.

## Overview[​](#overview "Direct link to Overview")

The MongoDB Document Loader returns a list of Langchain Documents from a MongoDB database.

The Loader requires the following parameters:

- MongoDB connection string
- MongoDB database name
- MongoDB collection name
- (Optional) Content Filter dictionary

The output takes the following format:

- pageContent= Mongo Document
- metadata={'database': '\[database_name\]', 'collection': '\[collection_name\]'}

## Load the Document Loader[​](#load-the-document-loader "Direct link to Load the Document Loader")

```python
# add this import for running in jupyter notebook  
import nest\_asyncio  
nest\_asyncio.apply()  

```

```python
from langchain.document\_loaders.mongodb import MongodbLoader  

```

```python
loader = MongodbLoader(connection\_string="mongodb://localhost:27017/",  
 db\_name="sample\_restaurants",   
 collection\_name="restaurants",  
 filter\_criteria={"borough": "Bronx", "cuisine": "Bakery" },  
 )  

```

```python
docs = loader.load()  
  
len(docs)  

```

```text
 25359  

```

```python
docs[0]  

```

```text
 Document(page\_content="{'\_id': ObjectId('5eb3d668b31de5d588f4292a'), 'address': {'building': '2780', 'coord': [-73.98241999999999, 40.579505], 'street': 'Stillwell Avenue', 'zipcode': '11224'}, 'borough': 'Brooklyn', 'cuisine': 'American', 'grades': [{'date': datetime.datetime(2014, 6, 10, 0, 0), 'grade': 'A', 'score': 5}, {'date': datetime.datetime(2013, 6, 5, 0, 0), 'grade': 'A', 'score': 7}, {'date': datetime.datetime(2012, 4, 13, 0, 0), 'grade': 'A', 'score': 12}, {'date': datetime.datetime(2011, 10, 12, 0, 0), 'grade': 'A', 'score': 12}], 'name': 'Riviera Caterer', 'restaurant\_id': '40356018'}", metadata={'database': 'sample\_restaurants', 'collection': 'restaurants'})  

```

- [Overview](#overview)
- [Load the Document Loader](#load-the-document-loader)

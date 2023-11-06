# Fauna

[Fauna](https://fauna.com/) is a Document Database.

Query `Fauna` documents

```python
#!pip install fauna  

```

## Query data example[​](#query-data-example "Direct link to Query data example")

```python
from langchain.document\_loaders.fauna import FaunaLoader  
  
secret = "<enter-valid-fauna-secret>"  
query = "Item.all()" # Fauna query. Assumes that the collection is called "Item"  
field = "text" # The field that contains the page content. Assumes that the field is called "text"  
  
loader = FaunaLoader(query, field, secret)  
docs = loader.lazy\_load()  
  
for value in docs:  
 print(value)  

```

### Query with Pagination[​](#query-with-pagination "Direct link to Query with Pagination")

You get a `after` value if there are more data. You can get values after the curcor by passing in the `after` string in query.

To learn more following [this link](https://fqlx-beta--fauna-docs.netlify.app/fqlx/beta/reference/schema_entities/set/static-paginate)

```python
query = """  
Item.paginate("hs+DzoPOg ... aY1hOohozrV7A")  
Item.all()  
"""  
loader = FaunaLoader(query, field, secret)  

```

- [Query data example](#query-data-example)

  - [Query with Pagination](#query-with-pagination)

- [Query with Pagination](#query-with-pagination)

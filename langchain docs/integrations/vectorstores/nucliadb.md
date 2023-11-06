# NucliaDB

You can use a local NucliaDB instance or use [Nuclia Cloud](https://nuclia.cloud).

When using a local instance, you need a Nuclia Understanding API key, so your texts are properly vectorized and indexed. You can get a key by creating a free account at <https://nuclia.cloud>, and then [create a NUA key](https://docs.nuclia.dev/docs/docs/using/understanding/intro).

```python
#!pip install langchain nuclia  

```

## Usage with nuclia.cloud[​](#usage-with-nucliacloud "Direct link to Usage with nuclia.cloud")

```python
from langchain.vectorstores.nucliadb import NucliaDB  
API\_KEY = "YOUR\_API\_KEY"  
  
ndb = NucliaDB(knowledge\_box="YOUR\_KB\_ID", local=False, api\_key=API\_KEY)  

```

## Usage with a local instance[​](#usage-with-a-local-instance "Direct link to Usage with a local instance")

Note: By default `backend` is set to `http://localhost:8080`.

```python
from langchain.vectorstores.nucliadb import NucliaDB  
  
ndb = NucliaDB(knowledge\_box="YOUR\_KB\_ID", local=True, backend="http://my-local-server")  

```

## Add and delete texts to your Knowledge Box[​](#add-and-delete-texts-to-your-knowledge-box "Direct link to Add and delete texts to your Knowledge Box")

```python
ids = ndb.add\_texts(["This is a new test", "This is a second test"])  

```

```python
ndb.delete(ids=ids)  

```

## Search in your Knowledge Box[​](#search-in-your-knowledge-box "Direct link to Search in your Knowledge Box")

```python
results = ndb.similarity\_search("Who was inspired by Ada Lovelace?")  
print(res.page\_content)  

```

- [Usage with nuclia.cloud](#usage-with-nucliacloud)
- [Usage with a local instance](#usage-with-a-local-instance)
- [Add and delete texts to your Knowledge Box](#add-and-delete-texts-to-your-knowledge-box)
- [Search in your Knowledge Box](#search-in-your-knowledge-box)

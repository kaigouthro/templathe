# Vespa

[Vespa](https://vespa.ai/) is a fully featured search engine and vector database. It supports vector search (ANN), lexical search, and search in structured data, all in the same query.

This notebook shows how to use `Vespa.ai` as a LangChain vector store.

In order to create the vector store, we use
[pyvespa](https://pyvespa.readthedocs.io/en/latest/index.html) to create a
connection a `Vespa` service.

```python
#!pip install pyvespa  

```

Using the `pyvespa` package, you can either connect to a
[Vespa Cloud instance](https://pyvespa.readthedocs.io/en/latest/deploy-vespa-cloud.html)
or a local
[Docker instance](https://pyvespa.readthedocs.io/en/latest/deploy-docker.html).
Here, we will create a new Vespa application and deploy that using Docker.

#### Creating a Vespa application[​](#creating-a-vespa-application "Direct link to Creating a Vespa application")

First, we need to create an application package:

```python
from vespa.package import ApplicationPackage, Field, RankProfile  
  
app\_package = ApplicationPackage(name="testapp")  
app\_package.schema.add\_fields(  
 Field(name="text", type="string", indexing=["index", "summary"], index="enable-bm25"),  
 Field(name="embedding", type="tensor<float>(x[384])",  
 indexing=["attribute", "summary"],  
 attribute=[f"distance-metric: angular"]),  
)  
app\_package.schema.add\_rank\_profile(  
 RankProfile(name="default",  
 first\_phase="closeness(field, embedding)",  
 inputs=[("query(query\_embedding)", "tensor<float>(x[384])")]  
 )  
)  

```

This sets up a Vespa application with a schema for each document that contains
two fields: `text` for holding the document text and `embedding` for holding
the embedding vector. The `text` field is set up to use a BM25 index for
efficient text retrieval, and we'll see how to use this and hybrid search a
bit later.

The `embedding` field is set up with a vector of length 384 to hold the
embedding representation of the text. See
[Vespa's Tensor Guide](https://docs.vespa.ai/en/tensor-user-guide.html)
for more on tensors in Vespa.

Lastly, we add a [rank profile](https://docs.vespa.ai/en/ranking.html) to
instruct Vespa how to order documents. Here we set this up with a
[nearest neighbor search](https://docs.vespa.ai/en/nearest-neighbor-search.html).

Now we can deploy this application locally:

```python
from vespa.deployment import VespaDocker  
  
vespa\_docker = VespaDocker()  
vespa\_app = vespa\_docker.deploy(application\_package=app\_package)  

```

This deploys and creates a connection to a `Vespa` service. In case you
already have a Vespa application running, for instance in the cloud,
please refer to the PyVespa application for how to connect.

#### Creating a Vespa vector store[​](#creating-a-vespa-vector-store "Direct link to Creating a Vespa vector store")

Now, let's load some documents:

```python
from langchain.document\_loaders import TextLoader  
from langchain.text\_splitter import CharacterTextSplitter  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
from langchain.embeddings.sentence\_transformer import SentenceTransformerEmbeddings  
  
embedding\_function = SentenceTransformerEmbeddings(model\_name="all-MiniLM-L6-v2")  

```

Here, we also set up local sentence embedder to transform the text to embedding
vectors. One could also use OpenAI embeddings, but the vector length needs to
be updated to `1536` to reflect the larger size of that embedding.

To feed these to Vespa, we need to configure how the vector store should map to
fields in the Vespa application. Then we create the vector store directly from
this set of documents:

```python
vespa\_config = dict(  
 page\_content\_field="text",  
 embedding\_field="embedding",  
 input\_field="query\_embedding"  
)  
  
from langchain.vectorstores import VespaStore  
  
db = VespaStore.from\_documents(docs, embedding\_function, app=vespa\_app, \*\*vespa\_config)  

```

This creates a Vespa vector store and feeds that set of documents to Vespa.
The vector store takes care of calling the embedding function for each document
and inserts them into the database.

We can now query the vector store:

```python
query = "What did the president say about Ketanji Brown Jackson"  
results = db.similarity\_search(query)  
  
print(results[0].page\_content)  

```

This will use the embedding function given above to create a representation
for the query and use that to search Vespa. Note that this will use the
`default` ranking function, which we set up in the application package
above. You can use the `ranking` argument to `similarity_search` to
specify which ranking function to use.

Please refer to the [pyvespa documentation](https://pyvespa.readthedocs.io/en/latest/getting-started-pyvespa.html#Query)
for more information.

This covers the basic usage of the Vespa store in LangChain.
Now you can return the results and continue using these in LangChain.

#### Updating documents[​](#updating-documents "Direct link to Updating documents")

An alternative to calling `from_documents`, you can create the vector
store directly and call `add_texts` from that. This can also be used to update
documents:

```python
query = "What did the president say about Ketanji Brown Jackson"  
results = db.similarity\_search(query)  
result = results[0]  
  
result.page\_content = "UPDATED: " + result.page\_content  
db.add\_texts([result.page\_content], [result.metadata], result.metadata["id"])  
  
results = db.similarity\_search(query)  
print(results[0].page\_content)  

```

However, the `pyvespa` library contains methods to manipulate
content on Vespa which you can use directly.

#### Deleting documents[​](#deleting-documents "Direct link to Deleting documents")

You can delete documents using the `delete` function:

```python
result = db.similarity\_search(query)  
# docs[0].metadata["id"] == "id:testapp:testapp::32"  
  
db.delete(["32"])  
result = db.similarity\_search(query)  
# docs[0].metadata["id"] != "id:testapp:testapp::32"  

```

Again, the `pyvespa` connection contains methods to delete documents as well.

### Returning with scores[​](#returning-with-scores "Direct link to Returning with scores")

The `similarity_search` method only returns the documents in order of
relevancy. To retrieve the actual scores:

```python
results = db.similarity\_search\_with\_score(query)  
result = results[0]  
# result[1] ~= 0.463  

```

This is a result of using the `"all-MiniLM-L6-v2"` embedding model using the
cosine distance function (as given by the argument `angular` in the
application function).

Different embedding functions need different distance functions, and Vespa
needs to know which distance function to use when orderings documents.
Please refer to the
[documentation on distance functions](https://docs.vespa.ai/en/reference/schema-reference.html#distance-metric)
for more information.

### As retriever[​](#as-retriever "Direct link to As retriever")

To use this vector store as a
[LangChain retriever](https://python.langchain.com/docs/modules/data_connection/retrievers/)
simply call the `as_retriever` function, which is a standard vector store
method:

```python
db = VespaStore.from\_documents(docs, embedding\_function, app=vespa\_app, \*\*vespa\_config)  
retriever = db.as\_retriever()  
query = "What did the president say about Ketanji Brown Jackson"  
results = retriever.get\_relevant\_documents(query)  
  
# results[0].metadata["id"] == "id:testapp:testapp::32"  

```

This allows for more general, unstructured, retrieval from the vector store.

### Metadata[​](#metadata "Direct link to Metadata")

In the example so far, we've only used the text and the embedding for that
text. Documents usually contain additional information, which in LangChain
is referred to as metadata.

Vespa can contain many fields with different types by adding them to the application
package:

```python
app\_package.schema.add\_fields(  
 # ...  
 Field(name="date", type="string", indexing=["attribute", "summary"]),  
 Field(name="rating", type="int", indexing=["attribute", "summary"]),  
 Field(name="author", type="string", indexing=["attribute", "summary"]),  
 # ...  
)  
vespa\_app = vespa\_docker.deploy(application\_package=app\_package)  

```

We can add some metadata fields in the documents:

```python
# Add metadata  
for i, doc in enumerate(docs):  
 doc.metadata["date"] = f"2023-{(i % 12)+1}-{(i % 28)+1}"  
 doc.metadata["rating"] = range(1, 6)[i % 5]  
 doc.metadata["author"] = ["Joe Biden", "Unknown"][min(i, 1)]  

```

And let the Vespa vector store know about these fields:

```python
vespa\_config.update(dict(metadata\_fields=["date", "rating", "author"]))  

```

Now, when searching for these documents, these fields will be returned.
Also, these fields can be filtered on:

```python
db = VespaStore.from\_documents(docs, embedding\_function, app=vespa\_app, \*\*vespa\_config)  
query = "What did the president say about Ketanji Brown Jackson"  
results = db.similarity\_search(query, filter="rating > 3")  
# results[0].metadata["id"] == "id:testapp:testapp::34"  
# results[0].metadata["author"] == "Unknown"  

```

### Custom query[​](#custom-query "Direct link to Custom query")

If the default behavior of the similarity search does not fit your
requirements, you can always provide your own query. Thus, you don't
need to provide all of the configuration to the vector store, but
rather just write this yourself.

First, let's add a BM25 ranking function to our application:

```python
from vespa.package import FieldSet  
  
app\_package.schema.add\_field\_set(FieldSet(name="default", fields=["text"]))  
app\_package.schema.add\_rank\_profile(RankProfile(name="bm25", first\_phase="bm25(text)"))  
vespa\_app = vespa\_docker.deploy(application\_package=app\_package)  
db = VespaStore.from\_documents(docs, embedding\_function, app=vespa\_app, \*\*vespa\_config)  

```

Then, to perform a regular text search based on BM25:

```python
query = "What did the president say about Ketanji Brown Jackson"  
custom\_query = {  
 "yql": f"select \* from sources \* where userQuery()",  
 "query": query,  
 "type": "weakAnd",  
 "ranking": "bm25",  
 "hits": 4  
}  
results = db.similarity\_search\_with\_score(query, custom\_query=custom\_query)  
# results[0][0].metadata["id"] == "id:testapp:testapp::32"  
# results[0][1] ~= 14.384  

```

All of the powerful search and query capabilities of Vespa can be used
by using a custom query. Please refer to the Vespa documentation on it's
[Query API](https://docs.vespa.ai/en/query-api.html) for more details.

### Hybrid search[​](#hybrid-search "Direct link to Hybrid search")

Hybrid search means using both a classic term-based search such as
BM25 and a vector search and combining the results. We need to create
a new rank profile for hybrid search on Vespa:

```python
app\_package.schema.add\_rank\_profile(  
 RankProfile(name="hybrid",  
 first\_phase="log(bm25(text)) + 0.5 \* closeness(field, embedding)",  
 inputs=[("query(query\_embedding)", "tensor<float>(x[384])")]  
 )  
)  
vespa\_app = vespa\_docker.deploy(application\_package=app\_package)  
db = VespaStore.from\_documents(docs, embedding\_function, app=vespa\_app, \*\*vespa\_config)  

```

Here, we score each document as a combination of it's BM25 score and its
distance score. We can query using a custom query:

```python
query = "What did the president say about Ketanji Brown Jackson"  
query\_embedding = embedding\_function.embed\_query(query)  
nearest\_neighbor\_expression = "{targetHits: 4}nearestNeighbor(embedding, query\_embedding)"  
custom\_query = {  
 "yql": f"select \* from sources \* where {nearest\_neighbor\_expression} and userQuery()",  
 "query": query,  
 "type": "weakAnd",  
 "input.query(query\_embedding)": query\_embedding,  
 "ranking": "hybrid",  
 "hits": 4  
}  
results = db.similarity\_search\_with\_score(query, custom\_query=custom\_query)  
# results[0][0].metadata["id"], "id:testapp:testapp::32")  
# results[0][1] ~= 2.897  

```

### Native embedders in Vespa[​](#native-embedders-in-vespa "Direct link to Native embedders in Vespa")

Up until this point we've used an embedding function in Python to provide
embeddings for the texts. Vespa supports embedding function natively, so
you can defer this calculation in to Vespa. One benefit is the ability to use
GPUs when embedding documents if you have a large collections.

Please refer to [Vespa embeddings](https://docs.vespa.ai/en/embedding.html)
for more information.

First, we need to modify our application package:

```python
from vespa.package import Component, Parameter  
  
app\_package.components = [  
 Component(id="hf-embedder", type="hugging-face-embedder",  
 parameters=[  
 Parameter("transformer-model", {"path": "..."}),  
 Parameter("tokenizer-model", {"url": "..."}),  
 ]  
 )  
]  
Field(name="hfembedding", type="tensor<float>(x[384])",  
 is\_document\_field=False,  
 indexing=["input text", "embed hf-embedder", "attribute", "summary"],  
 attribute=[f"distance-metric: angular"],  
 )  
app\_package.schema.add\_rank\_profile(  
 RankProfile(name="hf\_similarity",  
 first\_phase="closeness(field, hfembedding)",  
 inputs=[("query(query\_embedding)", "tensor<float>(x[384])")]  
 )  
)  

```

Please refer to the embeddings documentation on adding embedder models
and tokenizers to the application. Note that the `hfembedding` field
includes instructions for embedding using the `hf-embedder`.

Now we can query with a custom query:

```python
query = "What did the president say about Ketanji Brown Jackson"  
nearest\_neighbor\_expression = "{targetHits: 4}nearestNeighbor(internalembedding, query\_embedding)"  
custom\_query = {  
 "yql": f"select \* from sources \* where {nearest\_neighbor\_expression}",  
 "input.query(query\_embedding)": f"embed(hf-embedder, \"{query}\")",  
 "ranking": "internal\_similarity",  
 "hits": 4  
}  
results = db.similarity\_search\_with\_score(query, custom\_query=custom\_query)  
# results[0][0].metadata["id"], "id:testapp:testapp::32")  
# results[0][1] ~= 0.630  

```

Note that the query here includes an `embed` instruction to embed the query
using the same model as for the documents.

### Approximate nearest neighbor[​](#approximate-nearest-neighbor "Direct link to Approximate nearest neighbor")

In all of the above examples, we've used exact nearest neighbor to
find results. However, for large collections of documents this is
not feasible as one has to scan through all documents to find the
best matches. To avoid this, we can use
[approximate nearest neighbors](https://docs.vespa.ai/en/approximate-nn-hnsw.html).

First, we can change the embedding field to create a HNSW index:

```python
from vespa.package import HNSW  
  
app\_package.schema.add\_fields(  
 Field(name="embedding", type="tensor<float>(x[384])",  
 indexing=["attribute", "summary", "index"],  
 ann=HNSW(distance\_metric="angular", max\_links\_per\_node=16, neighbors\_to\_explore\_at\_insert=200)  
 )  
)  

```

This creates a HNSW index on the embedding data which allows for efficient
searching. With this set, we can easily search using ANN by setting
the `approximate` argument to `True`:

```python
query = "What did the president say about Ketanji Brown Jackson"  
results = db.similarity\_search(query, approximate=True)  
# results[0][0].metadata["id"], "id:testapp:testapp::32")  

```

This covers most of the functionality in the Vespa vector store in LangChain.

- [Returning with scores](#returning-with-scores)
- [As retriever](#as-retriever)
- [Metadata](#metadata)
- [Custom query](#custom-query)
- [Hybrid search](#hybrid-search)
- [Native embedders in Vespa](#native-embedders-in-vespa)
- [Approximate nearest neighbor](#approximate-nearest-neighbor)

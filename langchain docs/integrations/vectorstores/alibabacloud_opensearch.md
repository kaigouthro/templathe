# Alibaba Cloud OpenSearch

[Alibaba Cloud Opensearch](https://www.alibabacloud.com/product/opensearch) is a one-stop platform to develop intelligent search services. `OpenSearch` was built on the large-scale distributed search engine developed by `Alibaba`. `OpenSearch` serves more than 500 business cases in Alibaba Group and thousands of Alibaba Cloud customers. `OpenSearch` helps develop search services in different search scenarios, including e-commerce, O2O, multimedia, the content industry, communities and forums, and big data query in enterprises.

`OpenSearch` helps you develop high quality, maintenance-free, and high performance intelligent search services to provide your users with high search efficiency and accuracy.

`OpenSearch` provides the vector search feature. In specific scenarios, especially test question search and image search scenarios, you can use the vector search feature together with the multimodal search feature to improve the accuracy of search results.

This notebook shows how to use functionality related to the `Alibaba Cloud OpenSearch Vector Search Edition`.
To run, you should have an [OpenSearch Vector Search Edition](https://opensearch.console.aliyun.com) instance up and running:

Read the [help document](https://www.alibabacloud.com/help/en/opensearch/latest/vector-search) to quickly familiarize and configure OpenSearch Vector Search Edition instance.

After the instance is up and running, follow these steps to split documents, get embeddings, connect to the alibaba cloud opensearch instance, index documents, and perform vector retrieval.

We need to install the following Python packages first.

```python
#!pip install alibabacloud\_ha3engine\_vector  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores import (  
 AlibabaCloudOpenSearch,  
 AlibabaCloudOpenSearchSettings,  
)  

```

Split documents and get embeddings.

```python
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../../state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

Create opensearch settings.

```python
settings = AlibabaCloudOpenSearchSettings(  
 endpoint=" The endpoint of opensearch instance, You can find it from the console of Alibaba Cloud OpenSearch.",  
 instance\_id="The identify of opensearch instance, You can find it from the console of Alibaba Cloud OpenSearch.",  
 protocol="Communication Protocol between SDK and Server, default is http.",  
 username="The username specified when purchasing the instance.",  
 password="The password specified when purchasing the instance.",  
 namespace="The instance data will be partitioned based on the namespace field. If the namespace is enabled, you need to specify the namespace field name during initialization. Otherwise, the queries cannot be executed correctly.",  
 tablename="The table name specified during instance configuration.",  
 embedding\_field\_separator="Delimiter specified for writing vector field data, default is comma.",  
 output\_fields="Specify the field list returned when invoking OpenSearch, by default it is the value list of the field mapping field.",  
 field\_name\_mapping={  
 "id": "id", # The id field name mapping of index document.  
 "document": "document", # The text field name mapping of index document.  
 "embedding": "embedding", # The embedding field name mapping of index document.  
 "name\_of\_the\_metadata\_specified\_during\_search": "opensearch\_metadata\_field\_name,=",  
 # The metadata field name mapping of index document, could specify multiple, The value field contains mapping name and operator, the operator would be used when executing metadata filter query,  
 # Currently supported logical operators are: > (greater than), < (less than), = (equal to), <= (less than or equal to), >= (greater than or equal to), != (not equal to).  
 # Refer to this link: https://help.aliyun.com/zh/open-search/vector-search-edition/filter-expression  
 },  
)  
  
# for example  
  
# settings = AlibabaCloudOpenSearchSettings(  
# endpoint='ha-cn-5yd3fhdm102.public.ha.aliyuncs.com',  
# instance\_id='ha-cn-5yd3fhdm102',  
# username='instance user name',  
# password='instance password',  
# table\_name='test\_table',  
# field\_name\_mapping={  
# "id": "id",  
# "document": "document",  
# "embedding": "embedding",  
# "string\_field": "string\_filed,=",  
# "int\_field": "int\_filed,=",  
# "float\_field": "float\_field,=",  
# "double\_field": "double\_field,="  
#  
# },  
# )  

```

Create an opensearch access instance by settings.

```python
# Create an opensearch instance and index docs.  
opensearch = AlibabaCloudOpenSearch.from\_texts(  
 texts=docs, embedding=embeddings, config=settings  
)  

```

or

```python
# Create an opensearch instance.  
opensearch = AlibabaCloudOpenSearch(embedding=embeddings, config=settings)  

```

Add texts and build index.

```python
metadatas = [{'string\_field': "value1", "int\_field": 1, 'float\_field': 1.0, 'double\_field': 2.0},  
 {'string\_field': "value2", "int\_field": 2, 'float\_field': 3.0, 'double\_field': 4.0},  
 {'string\_field': "value3", "int\_field": 3, 'float\_field': 5.0, 'double\_field': 6.0}]  
# the key of metadatas must match field\_name\_mapping in settings.  
opensearch.add\_texts(texts=docs, ids=[], metadatas=metadatas)  

```

Query and retrieve data.

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs = opensearch.similarity\_search(query)  
print(docs[0].page\_content)  

```

Query and retrieve data with metadata.

```python
query = "What did the president say about Ketanji Brown Jackson"  
metadata = {'string\_field': "value1", "int\_field": 1, 'float\_field': 1.0, 'double\_field': 2.0}  
docs = opensearch.similarity\_search(query, filter=metadata)  
print(docs[0].page\_content)  

```

If you encounter any problems during use, please feel free to contact [xingshaomin.xsm@alibaba-inc.com](mailto:xingshaomin.xsm@alibaba-inc.com), and we will do our best to provide you with assistance and support.

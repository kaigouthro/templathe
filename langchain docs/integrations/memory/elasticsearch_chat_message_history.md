# Elasticsearch Chat Message History

[Elasticsearch](https://www.elastic.co/elasticsearch/) is a distributed, RESTful search and analytics engine, capable of performing both vector and lexical search. It is built on top of the Apache Lucene library.

This notebook shows how to use chat message history functionality with Elasticsearch.

## Set up Elasticsearch[​](#set-up-elasticsearch "Direct link to Set up Elasticsearch")

There are two main ways to set up an Elasticsearch instance:

1. **Elastic Cloud.** Elastic Cloud is a managed Elasticsearch service. Sign up for a [free trial](https://cloud.elastic.co/registration?storm=langchain-notebook).
1. **Local Elasticsearch installation.** Get started with Elasticsearch by running it locally. The easiest way is to use the official Elasticsearch Docker image. See the [Elasticsearch Docker documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) for more information.

**Elastic Cloud.** Elastic Cloud is a managed Elasticsearch service. Sign up for a [free trial](https://cloud.elastic.co/registration?storm=langchain-notebook).

**Local Elasticsearch installation.** Get started with Elasticsearch by running it locally. The easiest way is to use the official Elasticsearch Docker image. See the [Elasticsearch Docker documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) for more information.

## Install dependencies[​](#install-dependencies "Direct link to Install dependencies")

```python
%pip install elasticsearch langchain  

```

## Initialize Elasticsearch client and chat message history[​](#initialize-elasticsearch-client-and-chat-message-history "Direct link to Initialize Elasticsearch client and chat message history")

```python
import os  
from langchain.memory import ElasticsearchChatMessageHistory  
  
es\_url = os.environ.get("ES\_URL", "http://localhost:9200")  
  
# If using Elastic Cloud:  
# es\_cloud\_id = os.environ.get("ES\_CLOUD\_ID")  
  
# Note: see Authentication section for various authentication methods  
  
history = ElasticsearchChatMessageHistory(  
 es\_url=es\_url,  
 index="test-history",  
 session\_id="test-session"  
)  

```

## Use the chat message history[​](#use-the-chat-message-history "Direct link to Use the chat message history")

```python
history.add\_user\_message("hi!")  
history.add\_ai\_message("whats up?")  

```

```text
 indexing message content='hi!' additional\_kwargs={} example=False  
 indexing message content='whats up?' additional\_kwargs={} example=False  

```

# Authentication

## Username/password[​](#usernamepassword "Direct link to Username/password")

```python
es\_username = os.environ.get("ES\_USERNAME", "elastic")  
es\_password = os.environ.get("ES\_PASSWORD", "changeme")  
  
history = ElasticsearchChatMessageHistory(  
 es\_url=es\_url,  
 es\_user=es\_username,  
 es\_password=es\_password,  
 index="test-history",  
 session\_id="test-session"  
)  

```

### How to obtain a password for the default "elastic" user[​](#how-to-obtain-a-password-for-the-default-elastic-user "Direct link to How to obtain a password for the default \"elastic\" user")

To obtain your Elastic Cloud password for the default "elastic" user:

1. Log in to the Elastic Cloud console at <https://cloud.elastic.co>
1. Go to "Security" > "Users"
1. Locate the "elastic" user and click "Edit"
1. Click "Reset password"
1. Follow the prompts to reset the password

## API key[​](#api-key "Direct link to API key")

```python
es\_api\_key = os.environ.get("ES\_API\_KEY")  
  
history = ElasticsearchChatMessageHistory(  
 es\_api\_key=es\_api\_key,  
 index="test-history",  
 session\_id="test-session"  
)  

```

### How to obtain an API key[​](#how-to-obtain-an-api-key "Direct link to How to obtain an API key")

To obtain an API key:

1. Log in to the Elastic Cloud console at <https://cloud.elastic.co>
1. Open Kibana and go to Stack Management > API Keys
1. Click "Create API key"
1. Enter a name for the API key and click "Create"

- [Set up Elasticsearch](#set-up-elasticsearch)

- [Install dependencies](#install-dependencies)

- [Initialize Elasticsearch client and chat message history](#initialize-elasticsearch-client-and-chat-message-history)

- [Use the chat message history](#use-the-chat-message-history)

- [Username/password](#usernamepassword)

  - [How to obtain a password for the default "elastic" user](#how-to-obtain-a-password-for-the-default-elastic-user)

- [API key](#api-key)

  - [How to obtain an API key](#how-to-obtain-an-api-key)

- [How to obtain a password for the default "elastic" user](#how-to-obtain-a-password-for-the-default-elastic-user)

- [How to obtain an API key](#how-to-obtain-an-api-key)

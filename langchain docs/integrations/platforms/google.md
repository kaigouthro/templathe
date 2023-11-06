# Google

All functionality related to [Google Cloud Platform](https://cloud.google.com/)

## LLMs[​](#llms "Direct link to LLMs")

### Vertex AI[​](#vertex-ai "Direct link to Vertex AI")

Access PaLM LLMs like `text-bison` and `code-bison` via Google Cloud.

```python
from langchain.llms import VertexAI  

```

### Model Garden[​](#model-garden "Direct link to Model Garden")

Access PaLM and hundreds of OSS models via Vertex AI Model Garden.

```python
from langchain.llms import VertexAIModelGarden  

```

## Chat models[​](#chat-models "Direct link to Chat models")

### Vertex AI[​](#vertex-ai-1 "Direct link to Vertex AI")

Access PaLM chat models like `chat-bison` and `codechat-bison` via Google Cloud.

```python
from langchain.chat\_models import ChatVertexAI  

```

## Document Loader[​](#document-loader "Direct link to Document Loader")

### Google BigQuery[​](#google-bigquery "Direct link to Google BigQuery")

[Google BigQuery](https://cloud.google.com/bigquery) is a serverless and cost-effective enterprise data warehouse that works across clouds and scales with your data.
`BigQuery` is a part of the `Google Cloud Platform`.

First, we need to install `google-cloud-bigquery` python package.

```bash
pip install google-cloud-bigquery  

```

See a [usage example](/docs/integrations/document_loaders/google_bigquery).

```python
from langchain.document\_loaders import BigQueryLoader  

```

### Google Cloud Storage[​](#google-cloud-storage "Direct link to Google Cloud Storage")

[Google Cloud Storage](https://en.wikipedia.org/wiki/Google_Cloud_Storage) is a managed service for storing unstructured data.

First, we need to install `google-cloud-storage` python package.

```bash
pip install google-cloud-storage  

```

There are two loaders for the `Google Cloud Storage`: the `Directory` and the `File` loaders.

See a [usage example](/docs/integrations/document_loaders/google_cloud_storage_directory).

```python
from langchain.document\_loaders import GCSDirectoryLoader  

```

See a [usage example](/docs/integrations/document_loaders/google_cloud_storage_file).

```python
from langchain.document\_loaders import GCSFileLoader  

```

### Google Drive[​](#google-drive "Direct link to Google Drive")

[Google Drive](https://en.wikipedia.org/wiki/Google_Drive) is a file storage and synchronization service developed by Google.

Currently, only `Google Docs` are supported.

First, we need to install several python packages.

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib  

```

See a [usage example and authorizing instructions](/docs/integrations/document_loaders/google_drive.html).

```python
from langchain.document\_loaders import GoogleDriveLoader  

```

## Vector Store[​](#vector-store "Direct link to Vector Store")

### Google Vertex AI Vector Search[​](#google-vertex-ai-vector-search "Direct link to Google Vertex AI Vector Search")

[Google Vertex AI Vector Search](https://cloud.google.com/vertex-ai/docs/matching-engine/overview),
formerly known as Vertex AI Matching Engine, provides the industry's leading high-scale
low latency vector database. These vector databases are commonly
referred to as vector similarity-matching or an approximate nearest neighbor (ANN) service.

We need to install several python packages.

```bash
pip install tensorflow google-cloud-aiplatform tensorflow-hub tensorflow-text  

```

See a [usage example](/docs/integrations/vectorstores/matchingengine).

```python
from langchain.vectorstores import MatchingEngine  

```

### Google ScaNN[​](#google-scann "Direct link to Google ScaNN")

[Google ScaNN](https://github.com/google-research/google-research/tree/master/scann)
(Scalable Nearest Neighbors) is a python package.

`ScaNN` is a method for efficient vector similarity search at scale.

`ScaNN` includes search space pruning and quantization for Maximum Inner
Product Search and also supports other distance functions such as
Euclidean distance. The implementation is optimized for x86 processors
with AVX2 support. See its [Google Research github](https://github.com/google-research/google-research/tree/master/scann)
for more details.

We need to install `scann` python package.

```bash
pip install scann  

```

See a [usage example](/docs/integrations/vectorstores/scann).

```python
from langchain.vectorstores import ScaNN  

```

## Retrievers[​](#retrievers "Direct link to Retrievers")

### Vertex AI Search[​](#vertex-ai-search "Direct link to Vertex AI Search")

[Google Cloud Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/introduction)
allows developers to quickly build generative AI powered search engines for customers and employees.

First, you need to install the `google-cloud-discoveryengine` Python package.

```bash
pip install google-cloud-discoveryengine  

```

See a [usage example](/docs/integrations/retrievers/google_vertex_ai_search).

```python
from langchain.retrievers import GoogleVertexAISearchRetriever  

```

### Document AI Warehouse[​](#document-ai-warehouse "Direct link to Document AI Warehouse")

[Google Cloud Document AI Warehouse](https://cloud.google.com/document-ai-warehouse)
allows enterprises to search, store, govern, and manage documents and their AI-extracted
data and metadata in a single platform. Documents should be uploaded outside of Langchain,

```python
from langchain.retrievers import GoogleDocumentAIWarehouseRetriever  
docai\_wh\_retriever = GoogleDocumentAIWarehouseRetriever(  
 project\_number=...  
)  
query = ...  
documents = docai\_wh\_retriever.get\_relevant\_documents(  
 query, user\_ldap=...  
)  

```

## Tools[​](#tools "Direct link to Tools")

### Google Search[​](#google-search "Direct link to Google Search")

- Install requirements with `pip install google-api-python-client`
- Set up a Custom Search Engine, following [these instructions](https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search)
- Get an API Key and Custom Search Engine ID from the previous step, and set them as environment variables `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` respectively

There exists a `GoogleSearchAPIWrapper` utility which wraps this API. To import this utility:

```python
from langchain.utilities import GoogleSearchAPIWrapper  

```

For a more detailed walkthrough of this wrapper, see [this notebook](/docs/integrations/tools/google_search.html).

We can easily load this wrapper as a Tool (to use with an Agent). We can do this with:

```python
from langchain.agents import load\_tools  
tools = load\_tools(["google-search"])  

```

### Google Places[​](#google-places "Direct link to Google Places")

See a [usage example](/docs/integrations/tools/google_places).

```text
pip install googlemaps  

```

```python
from langchain.tools import GooglePlacesTool  

```

## Document Transformer[​](#document-transformer "Direct link to Document Transformer")

### Google Document AI[​](#google-document-ai "Direct link to Google Document AI")

[Document AI](https://cloud.google.com/document-ai/docs/overview) is a `Google Cloud Platform`
service to transform unstructured data from documents into structured data, making it easier
to understand, analyze, and consume.

We need to set up a [`GCS` bucket and create your own OCR processor](https://cloud.google.com/document-ai/docs/create-processor)

The `GCS_OUTPUT_PATH` should be a path to a folder on GCS (starting with `gs://`)
and a processor name should look like `projects/PROJECT_NUMBER/locations/LOCATION/processors/PROCESSOR_ID`.
We can get it either programmatically or copy from the `Prediction endpoint` section of the `Processor details`
tab in the Google Cloud Console.

```bash
pip install google-cloud-documentai  
pip install google-cloud-documentai-toolbox  

```

See a [usage example](/docs/integrations/document_transformers/docai).

```python
from langchain.document\_loaders.blob\_loaders import Blob  
from langchain.document\_loaders.parsers import DocAIParser  

```

## Chat loaders[​](#chat-loaders "Direct link to Chat loaders")

### Gmail[​](#gmail "Direct link to Gmail")

[Gmail](https://en.wikipedia.org/wiki/Gmail) is a free email service provided by Google.

First, we need to install several python packages.

```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client  

```

See a [usage example and authorizing instructions](/docs/integrations/chat_loaders/gmail).

```python
from langchain.chat\_loaders.gmail import GMailLoader  

```

## Agents and Toolkits[​](#agents-and-toolkits "Direct link to Agents and Toolkits")

### Gmail[​](#gmail-1 "Direct link to Gmail")

See a [usage example and authorizing instructions](/docs/integrations/toolkits/gmail).

```python
from langchain.agents.agent\_toolkits import GmailToolkit  
  
toolkit = GmailToolkit()  

```

### Google Drive[​](#google-drive-1 "Direct link to Google Drive")

See a [usage example and authorizing instructions](/docs/integrations/toolkits/google_drive).

```python
from langchain\_googledrive.utilities.google\_drive import GoogleDriveAPIWrapper  
from langchain\_googledrive.tools.google\_drive.tool import GoogleDriveSearchTool  

```

- [LLMs](#llms)

  - [Vertex AI](#vertex-ai)
  - [Model Garden](#model-garden)

- [Chat models](#chat-models)

  - [Vertex AI](#vertex-ai-1)

- [Document Loader](#document-loader)

  - [Google BigQuery](#google-bigquery)
  - [Google Cloud Storage](#google-cloud-storage)
  - [Google Drive](#google-drive)

- [Vector Store](#vector-store)

  - [Google Vertex AI Vector Search](#google-vertex-ai-vector-search)
  - [Google ScaNN](#google-scann)

- [Retrievers](#retrievers)

  - [Vertex AI Search](#vertex-ai-search)
  - [Document AI Warehouse](#document-ai-warehouse)

- [Tools](#tools)

  - [Google Search](#google-search)
  - [Google Places](#google-places)

- [Document Transformer](#document-transformer)

  - [Google Document AI](#google-document-ai)

- [Chat loaders](#chat-loaders)

  - [Gmail](#gmail)

- [Agents and Toolkits](#agents-and-toolkits)

  - [Gmail](#gmail-1)
  - [Google Drive](#google-drive-1)

- [Vertex AI](#vertex-ai)

- [Model Garden](#model-garden)

- [Vertex AI](#vertex-ai-1)

- [Google BigQuery](#google-bigquery)

- [Google Cloud Storage](#google-cloud-storage)

- [Google Drive](#google-drive)

- [Google Vertex AI Vector Search](#google-vertex-ai-vector-search)

- [Google ScaNN](#google-scann)

- [Vertex AI Search](#vertex-ai-search)

- [Document AI Warehouse](#document-ai-warehouse)

- [Google Search](#google-search)

- [Google Places](#google-places)

- [Google Document AI](#google-document-ai)

- [Gmail](#gmail)

- [Gmail](#gmail-1)

- [Google Drive](#google-drive-1)

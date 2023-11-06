# Clarifai

[Clarifai](https://clarifai.com) is one of first deep learning platforms having been founded in 2013. Clarifai provides an AI platform with the full AI lifecycle for data exploration, data labeling, model training, evaluation and inference around images, video, text and audio data. In the LangChain ecosystem, as far as we're aware, Clarifai is the only provider that supports LLMs, embeddings and a vector store in one production scale platform, making it an excellent choice to operationalize your LangChain implementations.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install the Python SDK:

```bash
pip install clarifai  

```

[Sign-up](https://clarifai.com/signup) for a Clarifai account, then get a personal access token to access the Clarifai API from your [security settings](https://clarifai.com/settings/security) and set it as an environment variable (`CLARIFAI_PAT`).

## Models[​](#models "Direct link to Models")

Clarifai provides 1,000s of AI models for many different use cases. You can [explore them here](https://clarifai.com/explore) to find the one most suited for your use case. These models include those created by other providers such as OpenAI, Anthropic, Cohere, AI21, etc. as well as state of the art from open source such as Falcon, InstructorXL, etc. so that you build the best in AI into your products. You'll find these organized by the creator's user_id and into projects we call applications denoted by their app_id. Those IDs will be needed in additional to the model_id and optionally the version_id, so make note of all these IDs once you found the best model for your use case!

Also note that given there are many models for images, video, text and audio understanding, you can build some interested AI agents that utilize the variety of AI models as experts to understand those data types.

### LLMs[​](#llms "Direct link to LLMs")

To find the selection of LLMs in the Clarifai platform you can select the text to text model type [here](https://clarifai.com/explore/models?filterData=%5B%7B%22field%22%3A%22model_type_id%22%2C%22value%22%3A%5B%22text-to-text%22%5D%7D%5D&page=1&perPage=24).

```python
from langchain.llms import Clarifai  
llm = Clarifai(pat=CLARIFAI\_PAT, user\_id=USER\_ID, app\_id=APP\_ID, model\_id=MODEL\_ID)  

```

For more details, the docs on the Clarifai LLM wrapper provide a [detailed walkthrough](/docs/integrations/llms/clarifai.html).

### Text Embedding Models[​](#text-embedding-models "Direct link to Text Embedding Models")

To find the selection of text embeddings models in the Clarifai platform you can select the text to embedding model type [here](https://clarifai.com/explore/models?page=1&perPage=24&filterData=%5B%7B%22field%22%3A%22model_type_id%22%2C%22value%22%3A%5B%22text-embedder%22%5D%7D%5D).

There is a Clarifai Embedding model in LangChain, which you can access with:

```python
from langchain.embeddings import ClarifaiEmbeddings  
embeddings = ClarifaiEmbeddings(pat=CLARIFAI\_PAT, user\_id=USER\_ID, app\_id=APP\_ID, model\_id=MODEL\_ID)  

```

For more details, the docs on the Clarifai Embeddings wrapper provide a [detailed walkthrough](/docs/integrations/text_embedding/clarifai.html).

## Vectorstore[​](#vectorstore "Direct link to Vectorstore")

Clarifai's vector DB was launched in 2016 and has been optimized to support live search queries. With workflows in the Clarifai platform, you data is automatically indexed by am embedding model and optionally other models as well to index that information in the DB for search. You can query the DB not only via the vectors but also filter by metadata matches, other AI predicted concepts, and even do geo-coordinate search. Simply create an application, select the appropriate base workflow for your type of data, and upload it (through the API as [documented here](https://docs.clarifai.com/api-guide/data/create-get-update-delete) or the UIs at clarifai.com).

You can also add data directly from LangChain as well, and the auto-indexing will take place for you. You'll notice this is a little different than other vectorstores where you need to provide an embedding model in their constructor and have LangChain coordinate getting the embeddings from text and writing those to the index. Not only is it more convenient, but it's much more scalable to use Clarifai's distributed cloud to do all the index in the background.

```python
from langchain.vectorstores import Clarifai  
clarifai\_vector\_db = Clarifai.from\_texts(user\_id=USER\_ID, app\_id=APP\_ID, texts=texts, pat=CLARIFAI\_PAT, number\_of\_docs=NUMBER\_OF\_DOCS, metadatas = metadatas)  

```

For more details, the docs on the Clarifai vector store provide a [detailed walkthrough](/docs/integrations/vectorstores/clarifai).

- [Installation and Setup](#installation-and-setup)

- [Models](#models)

  - [LLMs](#llms)
  - [Text Embedding Models](#text-embedding-models)

- [Vectorstore](#vectorstore)

- [LLMs](#llms)

- [Text Embedding Models](#text-embedding-models)

# Chat models

## Features (natively supported)[​](#features-natively-supported "Direct link to Features (natively supported)")

All ChatModels implement the Runnable interface, which comes with default implementations of all methods, ie. `ainvoke`, `batch`, `abatch`, `stream`, `astream`. This gives all ChatModels basic support for async, streaming and batch, which by default is implemented as below:

- *Async* support defaults to calling the respective sync method in asyncio's default thread pool executor. This lets other async functions in your application make progress while the ChatModel is being executed, by moving this call to a background thread.
- *Streaming* support defaults to returning an `Iterator` (or `AsyncIterator` in the case of async streaming) of a single value, the final result returned by the underlying ChatModel provider. This obviously doesn't give you token-by-token streaming, which requires native support from the ChatModel provider, but ensures your code that expects an iterator of tokens can work for any of our ChatModel integrations.
- *Batch* support defaults to calling the underlying ChatModel in parallel for each input by making use of a thread pool executor (in the sync batch case) or `asyncio.gather` (in the async batch case). The concurrency can be controlled with the `max_concurrency` key in `RunnableConfig`.

Each ChatModel integration can optionally provide native implementations to truly enable async or streaming.
The table shows, for each integration, which features have been implemented with native support.

| Model | Invoke | Async invoke | Stream | Async stream |
| --- | --- | --- | --- | --- |
| AzureChatOpenAI | ✅ | ✅ | ✅ | ✅ |
| BedrockChat | ✅ | ❌ | ✅ | ❌ |
| ChatAnthropic | ✅ | ✅ | ✅ | ✅ |
| ChatAnyscale | ✅ | ✅ | ✅ | ✅ |
| ChatBaichuan | ✅ | ❌ | ✅ | ❌ |
| ChatCohere | ✅ | ✅ | ✅ | ✅ |
| ChatEverlyAI | ✅ | ✅ | ✅ | ✅ |
| ChatFireworks | ✅ | ✅ | ✅ | ✅ |
| ChatGooglePalm | ✅ | ✅ | ❌ | ❌ |
| ChatHunyuan | ✅ | ❌ | ✅ | ❌ |
| ChatJavelinAIGateway | ✅ | ✅ | ❌ | ❌ |
| ChatKonko | ✅ | ❌ | ❌ | ❌ |
| ChatLiteLLM | ✅ | ✅ | ✅ | ✅ |
| ChatMLflowAIGateway | ✅ | ❌ | ❌ | ❌ |
| ChatOllama | ✅ | ❌ | ✅ | ❌ |
| ChatOpenAI | ✅ | ✅ | ✅ | ✅ |
| ChatVertexAI | ✅ | ✅ | ✅ | ❌ |
| ChatYandexGPT | ✅ | ✅ | ❌ | ❌ |
| ErnieBotChat | ✅ | ❌ | ❌ | ❌ |
| GigaChat | ✅ | ✅ | ✅ | ✅ |
| JinaChat | ✅ | ✅ | ✅ | ✅ |
| MiniMaxChat | ✅ | ✅ | ❌ | ❌ |
| PaiEasChatEndpoint | ✅ | ✅ | ❌ | ✅ |
| PromptLayerChatOpenAI | ✅ | ❌ | ❌ | ❌ |
| QianfanChatEndpoint | ✅ | ✅ | ✅ | ✅ |

## 📄️ Chat models

Features (natively supported)

## 📄️ Anthropic

This notebook covers how to get started with Anthropic chat models.

## 📄️ Anthropic Functions

This notebook shows how to use an experimental wrapper around Anthropic that gives it the same API as OpenAI Functions.

## 📄️ Anyscale

This notebook demonstrates the use of langchain.chat_models.ChatAnyscale for Anyscale Endpoints.

## 📄️ Azure

This notebook goes over how to connect to an Azure hosted OpenAI endpoint

## 📄️ AzureML Chat Online Endpoint

AzureML is a platform used to build, train, and deploy machine learning models. Users can explore the types of models to deploy in the Model Catalog, which provides Azure Foundation Models and OpenAI Models. Azure Foundation Models include various open-source models and popular Hugging Face models. Users can also import models of their liking into AzureML.

## 📄️ Baichuan Chat

Baichuan chat models API by Baichuan Intelligent Technology. For more information, see https://platform.baichuan-ai.com/docs/api

## 📄️ Baidu Qianfan

Baidu AI Cloud Qianfan Platform is a one-stop large model development and service operation platform for enterprise developers. Qianfan not only provides including the model of Wenxin Yiyan (ERNIE-Bot) and the third-party open-source models, but also provides various AI development tools and the whole set of development environment, which facilitates customers to use and develop large model applications easily.

## 📄️ Bedrock Chat

Amazon Bedrock is a fully managed service that makes FMs from leading AI startups and Amazon available via an API, so you can choose from a wide range of FMs to find the model that is best suited for your use case

## 📄️ Cohere

This notebook covers how to get started with Cohere chat models.

## 📄️ ERNIE-Bot Chat

ERNIE-Bot is a large language model developed by Baidu, covering a huge amount of Chinese data.

## 📄️ EverlyAI

EverlyAI allows you to run your ML models at scale in the cloud. It also provides API access to several LLM models.

## 📄️ Fireworks

Fireworks accelerates product development on generative AI by creating an innovative AI experiment and production platform.

## 📄️ GigaChat

This notebook shows how to use LangChain with GigaChat.

## 📄️ Google Cloud Vertex AI

Note: This is separate from the Google PaLM integration. Google has chosen to offer an enterprise version of PaLM through GCP, and this supports the models made available through there.

## 📄️ Tencent Hunyuan

Hunyuan chat model API by Tencent. For more information, see https://cloud.tencent.com/document/product/1729

## 📄️ JinaChat

This notebook covers how to get started with JinaChat chat models.

## 📄️ Konko

Konko API is a fully managed Web API designed to help application developers:

## 📄️ 🚅 LiteLLM

LiteLLM is a library that simplifies calling Anthropic, Azure, Huggingface, Replicate, etc.

## 📄️ Llama API

This notebook shows how to use LangChain with LlamaAPI - a hosted version of Llama2 that adds in support for function calling.

## 📄️ MiniMax

Minimax is a Chinese startup that provides LLM service for companies and individuals.

## 📄️ Ollama

Ollama allows you to run open-source large language models, such as LLaMA2, locally.

## 📄️ OpenAI

This notebook covers how to get started with OpenAI chat models.

## 📄️ AliCloud PAI EAS

Machine Learning Platform for AI of Alibaba Cloud is a machine learning or deep learning engineering platform intended for enterprises and developers. It provides easy-to-use, cost-effective, high-performance, and easy-to-scale plug-ins that can be applied to various industry scenarios. With over 140 built-in optimization algorithms, Machine Learning Platform for AI provides whole-process AI engineering capabilities including data labeling (PAI-iTAG), model building (PAI-Designer and PAI-DSW), model training (PAI-DLC), compilation optimization, and inference deployment (PAI-EAS). PAI-EAS supports different types of hardware resources, including CPUs and GPUs, and features high throughput and low latency. It allows you to deploy large-scale complex models with a few clicks and perform elastic scale-ins and scale-outs in real time. It also provides a comprehensive O&M and monitoring system.

## 📄️ PromptLayer ChatOpenAI

This example showcases how to connect to PromptLayer to start recording your ChatOpenAI requests.

## 📄️ Tongyi Qwen

Tongyi Qwen is a large language model developed by Alibaba's Damo Academy. It is capable of understanding user intent through natural language understanding and semantic analysis, based on user input in natural language. It provides services and assistance to users in different domains and tasks. By providing clear and detailed instructions, you can obtain results that better align with your expectations.

## 📄️ vLLM Chat

vLLM can be deployed as a server that mimics the OpenAI API protocol. This allows vLLM to be used as a drop-in replacement for applications using OpenAI API. This server can be queried in the same format as OpenAI API.

## 📄️ YandexGPT

This notebook goes over how to use Langchain with YandexGPT chat model.

- [Features (natively supported)](#features-natively-supported)

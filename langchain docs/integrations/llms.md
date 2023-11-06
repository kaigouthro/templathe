# LLMs

## Features (natively supported)[​](#features-natively-supported "Direct link to Features (natively supported)")

All LLMs implement the Runnable interface, which comes with default implementations of all methods, ie. `ainvoke`, `batch`, `abatch`, `stream`, `astream`. This gives all LLMs basic support for async, streaming and batch, which by default is implemented as below:

- *Async* support defaults to calling the respective sync method in asyncio's default thread pool executor. This lets other async functions in your application make progress while the LLM is being executed, by moving this call to a background thread.
- *Streaming* support defaults to returning an `Iterator` (or `AsyncIterator` in the case of async streaming) of a single value, the final result returned by the underlying LLM provider. This obviously doesn't give you token-by-token streaming, which requires native support from the LLM provider, but ensures your code that expects an iterator of tokens can work for any of our LLM integrations.
- *Batch* support defaults to calling the underlying LLM in parallel for each input by making use of a thread pool executor (in the sync batch case) or `asyncio.gather` (in the async batch case). The concurrency can be controlled with the `max_concurrency` key in `RunnableConfig`.

Each LLM integration can optionally provide native implementations for async, streaming or batch, which, for providers that support it, can be more efficient. The table shows, for each integration, which features have been implemented with native support.

| Model | Invoke | Async invoke | Stream | Async stream | Batch | Async batch |
| --- | --- | --- | --- | --- | --- | --- |
| AI21 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| AlephAlpha | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| AmazonAPIGateway | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Anthropic | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Anyscale | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Arcee | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Aviary | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| AzureMLOnlineEndpoint | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| AzureOpenAI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Banana | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Baseten | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Beam | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Bedrock | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| CTransformers | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| CTranslate2 | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| CerebriumAI | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ChatGLM | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Clarifai | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Cohere | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Databricks | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| DeepInfra | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| DeepSparse | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| EdenAI | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Fireworks | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| ForefrontAI | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| GPT4All | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| GigaChat | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GooglePalm | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| GooseAI | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| GradientLLM | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| HuggingFaceEndpoint | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| HuggingFaceHub | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| HuggingFacePipeline | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| HuggingFaceTextGenInference | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| HumanInputLLM | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| JavelinAIGateway | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| KoboldApiLLM | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| LlamaCpp | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| ManifestWrapper | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Minimax | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| MlflowAIGateway | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Modal | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| MosaicML | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| NIBittensorLLM | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| NLPCloud | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Nebula | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| OctoAIEndpoint | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Ollama | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| OpaquePrompts | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| OpenAI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| OpenLLM | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| OpenLM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PaiEasEndpoint | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Petals | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| PipelineAI | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Predibase | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| PredictionGuard | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| PromptLayerOpenAI | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| QianfanLLMEndpoint | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| RWKV | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Replicate | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| SagemakerEndpoint | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| SelfHostedHuggingFaceLLM | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| SelfHostedPipeline | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| StochasticAI | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| TextGen | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| TitanTakeoff | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Tongyi | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| VLLM | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| VLLMOpenAI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| VertexAI | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| VertexAIModelGarden | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Writer | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Xinference | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| YandexGPT | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

## 📄️ LLMs

Features (natively supported)

## 📄️ AI21

AI21 Studio provides API access to Jurassic-2 large language models.

## 📄️ Aleph Alpha

The Luminous series is a family of large language models.

## 📄️ Amazon API Gateway

Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. APIs act as the "front door" for applications to access data, business logic, or functionality from your backend services. Using API Gateway, you can create RESTful APIs and WebSocket APIs that enable real-time two-way communication applications. API Gateway supports containerized and serverless workloads, as well as web applications.

## 📄️ Anyscale

Anyscale is a fully-managed Ray platform, on which you can build, deploy, and manage scalable AI and Python applications

## 📄️ Arcee

This notebook demonstrates how to use the Arcee class for generating text using Arcee's Domain Adapted Language Models (DALMs).

## 📄️ Azure ML

Azure ML is a platform used to build, train, and deploy machine learning models. Users can explore the types of models to deploy in the Model Catalog, which provides Azure Foundation Models and OpenAI Models. Azure Foundation Models include various open-source models and popular Hugging Face models. Users can also import models of their liking into AzureML.

## 📄️ Azure OpenAI

This notebook goes over how to use Langchain with Azure OpenAI.

## 📄️ Baidu Qianfan

Baidu AI Cloud Qianfan Platform is a one-stop large model development and service operation platform for enterprise developers. Qianfan not only provides including the model of Wenxin Yiyan (ERNIE-Bot) and the third-party open-source models, but also provides various AI development tools and the whole set of development environment, which facilitates customers to use and develop large model applications easily.

## 📄️ Banana

Banana is focused on building the machine learning infrastructure.

## 📄️ Baseten

Baseten provides all the infrastructure you need to deploy and serve ML models performantly, scalably, and cost-efficiently.

## 📄️ Beam

Calls the Beam API wrapper to deploy and make subsequent calls to an instance of the gpt2 LLM in a cloud deployment. Requires installation of the Beam library and registration of Beam Client ID and Client Secret. By calling the wrapper an instance of the model is created and run, with returned text relating to the prompt. Additional calls can then be made by directly calling the Beam API.

## 📄️ Bedrock

Amazon Bedrock is a fully managed service that makes FMs from leading AI startups and Amazon available via an API, so you can choose from a wide range of FMs to find the model that is best suited for your use case

## 📄️ Bittensor

Bittensor is a mining network, similar to Bitcoin, that includes built-in incentives designed to encourage miners to contribute compute + knowledge.

## 📄️ CerebriumAI

Cerebrium is an AWS Sagemaker alternative. It also provides API access to several LLM models.

## 📄️ ChatGLM

ChatGLM-6B is an open bilingual language model based on General Language Model (GLM) framework, with 6.2 billion parameters. With the quantization technique, users can deploy locally on consumer-grade graphics cards (only 6GB of GPU memory is required at the INT4 quantization level).

## 📄️ Clarifai

Clarifai is an AI Platform that provides the full AI lifecycle ranging from data exploration, data labeling, model training, evaluation, and inference.

## 📄️ Cohere

Cohere is a Canadian startup that provides natural language processing models that help companies improve human-machine interactions.

## 📄️ C Transformers

The C Transformers library provides Python bindings for GGML models.

## 📄️ CTranslate2

CTranslate2 is a C++ and Python library for efficient inference with Transformer models.

## 📄️ Databricks

The Databricks Lakehouse Platform unifies data, analytics, and AI on one platform.

## 📄️ DeepInfra

DeepInfra is a serverless inference as a service that provides access to a variety of LLMs and embeddings models. This notebook goes over how to use LangChain with DeepInfra for language models.

## 📄️ DeepSparse

This page covers how to use the DeepSparse inference runtime within LangChain.

## 📄️ Eden AI

Eden AI is revolutionizing the AI landscape by uniting the best AI providers, empowering users to unlock limitless possibilities and tap into the true potential of artificial intelligence. With an all-in-one comprehensive and hassle-free platform, it allows users to deploy AI features to production lightning fast, enabling effortless access to the full breadth of AI capabilities via a single API. (website//edenai.co/)

## 📄️ Fireworks

Fireworks accelerates product development on generative AI by creating an innovative AI experiment and production platform.

## 📄️ ForefrontAI

The Forefront platform gives you the ability to fine-tune and use open-source large language models.

## 📄️ GigaChat

This notebook shows how to use LangChain with GigaChat.

## 📄️ Google Cloud Vertex AI

Note: This is separate from the Google PaLM integration, it exposes Vertex AI PaLM API on Google Cloud.

## 📄️ GooseAI

GooseAI is a fully managed NLP-as-a-Service, delivered via API. GooseAI provides access to these models.

## 📄️ GPT4All

GitHub:nomic-ai/gpt4all an ecosystem of open-source chatbots trained on a massive collections of clean assistant data including code, stories and dialogue.

## 📄️ Gradient

Gradient allows to fine tune and get completions on LLMs with a simple web API.

## 📄️ Hugging Face Hub

The Hugging Face Hub is a platform with over 120k models, 20k datasets, and 50k demo apps (Spaces), all open source and publicly available, in an online platform where people can easily collaborate and build ML together.

## 📄️ Hugging Face Local Pipelines

Hugging Face models can be run locally through the HuggingFacePipeline class.

## 📄️ Huggingface TextGen Inference

Text Generation Inference is a Rust, Python and gRPC server for text generation inference. Used in production at HuggingFace to power LLMs api-inference widgets.

## 📄️ Javelin AI Gateway Tutorial

This Jupyter Notebook will explore how to interact with the Javelin AI Gateway using the Python SDK.

## 📄️ JSONFormer

JSONFormer is a library that wraps local Hugging Face pipeline models for structured decoding of a subset of the JSON Schema.

## 📄️ KoboldAI API

KoboldAI is a "a browser-based front-end for AI-assisted writing with multiple local & remote AI models...". It has a public and local API that is able to be used in langchain.

## 📄️ Llama.cpp

llama-cpp-python is a Python binding for llama.cpp.

## 📄️ LLM Caching integrations

This notebook covers how to cache results of individual LLM calls using different caches.

## 📄️ Manifest

This notebook goes over how to use Manifest and LangChain.

## 📄️ Minimax

Minimax is a Chinese startup that provides natural language processing models for companies and individuals.

## 📄️ Modal

The Modal cloud platform provides convenient, on-demand access to serverless cloud compute from Python scripts on your local computer.

## 📄️ MosaicML

MosaicML offers a managed inference service. You can either use a variety of open-source models, or deploy your own.

## 📄️ NLP Cloud

The NLP Cloud serves high performance pre-trained or custom models for NER, sentiment-analysis, classification, summarization, paraphrasing, grammar and spelling correction, keywords and keyphrases extraction, chatbot, product description and ad generation, intent classification, text generation, image generation, blog post generation, code generation, question answering, automatic speech recognition, machine translation, language detection, semantic search, semantic similarity, tokenization, POS tagging, embeddings, and dependency parsing. It is ready for production, served through a REST API.

## 📄️ OctoAI

OctoML is a service with efficient compute. It enables users to integrate their choice of AI models into applications. The OctoAI compute service helps you run, tune, and scale AI applications.

## 📄️ Ollama

Ollama allows you to run open-source large language models, such as Llama 2, locally.

## 📄️ OpaquePrompts

OpaquePrompts is a service that enables applications to leverage the power of language models without compromising user privacy. Designed for composability and ease of integration into existing applications and services, OpaquePrompts is consumable via a simple Python library as well as through LangChain. Perhaps more importantly, OpaquePrompts leverages the power of confidential computing to ensure that even the OpaquePrompts service itself cannot access the data it is protecting.

## 📄️ OpenAI

OpenAI offers a spectrum of models with different levels of power suitable for different tasks.

## 📄️ OpenLLM

🦾 OpenLLM is an open platform for operating large language models (LLMs) in production. It enables developers to easily run inference with any open-source LLMs, deploy to the cloud or on-premises, and build powerful AI apps.

## 📄️ OpenLM

OpenLM is a zero-dependency OpenAI-compatible LLM provider that can call different inference endpoints directly via HTTP.

## 📄️ AliCloud PAI EAS

Machine Learning Platform for AI of Alibaba Cloud is a machine learning or deep learning engineering platform intended for enterprises and developers. It provides easy-to-use, cost-effective, high-performance, and easy-to-scale plug-ins that can be applied to various industry scenarios. With over 140 built-in optimization algorithms, Machine Learning Platform for AI provides whole-process AI engineering capabilities including data labeling (PAI-iTAG), model building (PAI-Designer and PAI-DSW), model training (PAI-DLC), compilation optimization, and inference deployment (PAI-EAS). PAI-EAS supports different types of hardware resources, including CPUs and GPUs, and features high throughput and low latency. It allows you to deploy large-scale complex models with a few clicks and perform elastic scale-ins and scale-outs in real time. It also provides a comprehensive O&M and monitoring system.

## 📄️ Petals

Petals runs 100B+ language models at home, BitTorrent-style.

## 📄️ PipelineAI

PipelineAI allows you to run your ML models at scale in the cloud. It also provides API access to several LLM models.

## 📄️ Predibase

Predibase allows you to train, fine-tune, and deploy any ML model—from linear regression to large language model.

## 📄️ Prediction Guard

Basic LLM usage

## 📄️ PromptLayer OpenAI

PromptLayer is the first platform that allows you to track, manage, and share your GPT prompt engineering. PromptLayer acts a middleware between your code and OpenAI’s python library.

## 📄️ RELLM

RELLM is a library that wraps local Hugging Face pipeline models for structured decoding.

## 📄️ Replicate

Replicate runs machine learning models in the cloud. We have a library of open-source models that you can run with a few lines of code. If you're building your own machine learning models, Replicate makes it easy to deploy them at scale.

## 📄️ Runhouse

The Runhouse allows remote compute and data across environments and users. See the Runhouse docs.

## 📄️ SageMakerEndpoint

Amazon SageMaker is a system that can build, train, and deploy machine learning (ML) models for any use case with fully managed infrastructure, tools, and workflows.

## 📄️ StochasticAI

Stochastic Acceleration Platform aims to simplify the life cycle of a Deep Learning model. From uploading and versioning the model, through training, compression and acceleration to putting it into production.

## 📄️ Nebula (Symbl.ai)

Nebula is a large language model (LLM) built by Symbl.ai. It is trained to perform generative tasks on human conversations. Nebula excels at modeling the nuanced details of a conversation and performing tasks on the conversation.

## 📄️ TextGen

GitHub:oobabooga/text-generation-webui A gradio web UI for running Large Language Models like LLaMA, llama.cpp, GPT-J, Pythia, OPT, and GALACTICA.

## 📄️ Titan Takeoff

TitanML helps businesses build and deploy better, smaller, cheaper, and faster NLP models through our training, compression, and inference optimization platform.

## 📄️ Together AI

The Together API makes it easy to fine-tune or run leading open-source models with a couple lines of code. We have integrated the world’s leading open-source models, including Llama-2, RedPajama, Falcon, Alpaca, Stable Diffusion XL, and more. Read more//together.ai

## 📄️ Tongyi Qwen

Tongyi Qwen is a large-scale language model developed by Alibaba's Damo Academy. It is capable of understanding user intent through natural language understanding and semantic analysis, based on user input in natural language. It provides services and assistance to users in different domains and tasks. By providing clear and detailed instructions, you can obtain results that better align with your expectations.

## 📄️ vLLM

vLLM is a fast and easy-to-use library for LLM inference and serving, offering:

## 📄️ Writer

Writer is a platform to generate different language content.

## 📄️ Xorbits Inference (Xinference)

Xinference is a powerful and versatile library designed to serve LLMs,

## 📄️ YandexGPT

This notebook goes over how to use Langchain with YandexGPT.

- [Features (natively supported)](#features-natively-supported)

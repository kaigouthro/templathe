# AWS

All functionality related to [Amazon AWS](https://aws.amazon.com/) platform

## LLMs[​](#llms "Direct link to LLMs")

### Bedrock[​](#bedrock "Direct link to Bedrock")

See a [usage example](/docs/integrations/llms/bedrock).

```python
from langchain.llms.bedrock import Bedrock  

```

### Amazon API Gateway[​](#amazon-api-gateway "Direct link to Amazon API Gateway")

[Amazon API Gateway](https://aws.amazon.com/api-gateway/) is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. APIs act as the "front door" for applications to access data, business logic, or functionality from your backend services. Using API Gateway, you can create RESTful APIs and WebSocket APIs that enable real-time two-way communication applications. API Gateway supports containerized and serverless workloads, as well as web applications.

API Gateway handles all the tasks involved in accepting and processing up to hundreds of thousands of concurrent API calls, including traffic management, CORS support, authorization and access control, throttling, monitoring, and API version management. API Gateway has no minimum fees or startup costs. You pay for the API calls you receive and the amount of data transferred out and, with the API Gateway tiered pricing model, you can reduce your cost as your API usage scales.

See a [usage example](/docs/integrations/llms/amazon_api_gateway_example).

```python
from langchain.llms import AmazonAPIGateway  
  
api\_url = "https://<api\_gateway\_id>.execute-api.<region>.amazonaws.com/LATEST/HF"  
# These are sample parameters for Falcon 40B Instruct Deployed from Amazon SageMaker JumpStart  
model\_kwargs = {  
 "max\_new\_tokens": 100,  
 "num\_return\_sequences": 1,  
 "top\_k": 50,  
 "top\_p": 0.95,  
 "do\_sample": False,  
 "return\_full\_text": True,  
 "temperature": 0.2,  
}  
llm = AmazonAPIGateway(api\_url=api\_url, model\_kwargs=model\_kwargs)  

```

### SageMaker Endpoint[​](#sagemaker-endpoint "Direct link to SageMaker Endpoint")

[Amazon SageMaker](https://aws.amazon.com/sagemaker/) is a system that can build, train, and deploy machine learning (ML) models with fully managed infrastructure, tools, and workflows.

We use `SageMaker` to host our model and expose it as the `SageMaker Endpoint`.

See a [usage example](/docs/integrations/llms/sagemaker).

```python
from langchain.llms import SagemakerEndpoint  
from langchain.llms.sagemaker\_endpoint import LLMContentHandler  

```

## Text Embedding Models[​](#text-embedding-models "Direct link to Text Embedding Models")

### Bedrock[​](#bedrock-1 "Direct link to Bedrock")

See a [usage example](/docs/integrations/text_embedding/bedrock).

```python
from langchain.embeddings import BedrockEmbeddings  

```

### SageMaker Endpoint[​](#sagemaker-endpoint-1 "Direct link to SageMaker Endpoint")

See a [usage example](/docs/integrations/text_embedding/sagemaker-endpoint).

```python
from langchain.embeddings import SagemakerEndpointEmbeddings  
from langchain.llms.sagemaker\_endpoint import ContentHandlerBase  

```

## Document loaders[​](#document-loaders "Direct link to Document loaders")

### AWS S3 Directory and File[​](#aws-s3-directory-and-file "Direct link to AWS S3 Directory and File")

[Amazon Simple Storage Service (Amazon S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html) is an object storage service.
[AWS S3 Directory](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)
[AWS S3 Buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html)

See a [usage example for S3DirectoryLoader](/docs/integrations/document_loaders/aws_s3_directory.html).

See a [usage example for S3FileLoader](/docs/integrations/document_loaders/aws_s3_file.html).

```python
from langchain.document\_loaders import S3DirectoryLoader, S3FileLoader  

```

## Memory[​](#memory "Direct link to Memory")

### AWS DynamoDB[​](#aws-dynamodb "Direct link to AWS DynamoDB")

[AWS DynamoDB](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/dynamodb/index.html)
is a fully managed `NoSQL` database service that provides fast and predictable performance with seamless scalability.

We have to configure the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

We need to install the `boto3` library.

```bash
pip install boto3  

```

See a [usage example](/docs/integrations/memory/aws_dynamodb).

```python
from langchain.memory import DynamoDBChatMessageHistory  

```

- [LLMs](#llms)

  - [Bedrock](#bedrock)
  - [Amazon API Gateway](#amazon-api-gateway)
  - [SageMaker Endpoint](#sagemaker-endpoint)

- [Text Embedding Models](#text-embedding-models)

  - [Bedrock](#bedrock-1)
  - [SageMaker Endpoint](#sagemaker-endpoint-1)

- [Document loaders](#document-loaders)

  - [AWS S3 Directory and File](#aws-s3-directory-and-file)

- [Memory](#memory)

  - [AWS DynamoDB](#aws-dynamodb)

- [Bedrock](#bedrock)

- [Amazon API Gateway](#amazon-api-gateway)

- [SageMaker Endpoint](#sagemaker-endpoint)

- [Bedrock](#bedrock-1)

- [SageMaker Endpoint](#sagemaker-endpoint-1)

- [AWS S3 Directory and File](#aws-s3-directory-and-file)

- [AWS DynamoDB](#aws-dynamodb)

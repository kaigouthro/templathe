# AWS S3 Directory

[Amazon Simple Storage Service (Amazon S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html) is an object storage service

[AWS S3 Directory](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)

This covers how to load document objects from an `AWS S3 Directory` object.

```python
#!pip install boto3  

```

```python
from langchain.document\_loaders import S3DirectoryLoader  

```

```python
loader = S3DirectoryLoader("testing-hwc")  

```

```python
loader.load()  

```

## Specifying a prefix[​](#specifying-a-prefix "Direct link to Specifying a prefix")

You can also specify a prefix for more finegrained control over what files to load.

```python
loader = S3DirectoryLoader("testing-hwc", prefix="fake")  

```

```python
loader.load()  

```

```text
 [Document(page\_content='Lorem ipsum dolor sit amet.', lookup\_str='', metadata={'source': 's3://testing-hwc/fake.docx'}, lookup\_index=0)]  

```

## Configuring the AWS Boto3 client[​](#configuring-the-aws-boto3-client "Direct link to Configuring the AWS Boto3 client")

You can configure the AWS [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) client by passing
named arguments when creating the S3DirectoryLoader.
This is useful for instance when AWS credentials can't be set as environment variables.
See the [list of parameters](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session) that can be configured.

```python
loader = S3DirectoryLoader("testing-hwc", aws\_access\_key\_id="xxxx", aws\_secret\_access\_key="yyyy")  

```

```python
loader.load()  

```

- [Specifying a prefix](#specifying-a-prefix)
- [Configuring the AWS Boto3 client](#configuring-the-aws-boto3-client)

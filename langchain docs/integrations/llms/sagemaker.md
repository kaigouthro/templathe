# SageMakerEndpoint

[Amazon SageMaker](https://aws.amazon.com/sagemaker/) is a system that can build, train, and deploy machine learning (ML) models for any use case with fully managed infrastructure, tools, and workflows.

This notebooks goes over how to use an LLM hosted on a `SageMaker endpoint`.

```bash
pip3 install langchain boto3  

```

## Set up[​](#set-up "Direct link to Set up")

You have to set up following required parameters of the `SagemakerEndpoint` call:

- `endpoint_name`: The name of the endpoint from the deployed Sagemaker model.
  Must be unique within an AWS Region.
- `credentials_profile_name`: The name of the profile in the ~/.aws/credentials or ~/.aws/config files, which
  has either access keys or role information specified.
  If not specified, the default credential profile or, if on an EC2 instance,
  credentials from IMDS will be used.
  See: <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html>

## Example[​](#example "Direct link to Example")

```python
from langchain.docstore.document import Document  

```

```python
example\_doc\_1 = """  
Peter and Elizabeth took a taxi to attend the night party in the city. While in the party, Elizabeth collapsed and was rushed to the hospital.  
Since she was diagnosed with a brain injury, the doctor told Peter to stay besides her until she gets well.  
Therefore, Peter stayed with her at the hospital for 3 days without leaving.  
"""  
  
docs = [  
 Document(  
 page\_content=example\_doc\_1,  
 )  
]  

```

## Example to initialize with external boto3 session[​](#example-to-initialize-with-external-boto3-session "Direct link to Example to initialize with external boto3 session")

### for cross account scenarios[​](#for-cross-account-scenarios "Direct link to for cross account scenarios")

```python
from typing import Dict  
  
from langchain.prompts import PromptTemplate  
from langchain.llms import SagemakerEndpoint  
from langchain.llms.sagemaker\_endpoint import LLMContentHandler  
from langchain.chains.question\_answering import load\_qa\_chain  
import json  
import boto3  
  
query = """How long was Elizabeth hospitalized?  
"""  
  
prompt\_template = """Use the following pieces of context to answer the question at the end.  
  
{context}  
  
Question: {question}  
Answer:"""  
PROMPT = PromptTemplate(  
 template=prompt\_template, input\_variables=["context", "question"]  
)  
  
roleARN = 'arn:aws:iam::123456789:role/cross-account-role'  
sts\_client = boto3.client('sts')  
response = sts\_client.assume\_role(RoleArn=roleARN,   
 RoleSessionName='CrossAccountSession')  
  
client = boto3.client(  
 "sagemaker-runtime",  
 region\_name="us-west-2",   
 aws\_access\_key\_id=response['Credentials']['AccessKeyId'],  
 aws\_secret\_access\_key=response['Credentials']['SecretAccessKey'],  
 aws\_session\_token = response['Credentials']['SessionToken']  
)  
  
class ContentHandler(LLMContentHandler):  
 content\_type = "application/json"  
 accepts = "application/json"  
  
 def transform\_input(self, prompt: str, model\_kwargs: Dict) -> bytes:  
 input\_str = json.dumps({prompt: prompt, \*\*model\_kwargs})  
 return input\_str.encode("utf-8")  
  
 def transform\_output(self, output: bytes) -> str:  
 response\_json = json.loads(output.read().decode("utf-8"))  
 return response\_json[0]["generated\_text"]  
  
  
content\_handler = ContentHandler()  
  
chain = load\_qa\_chain(  
 llm=SagemakerEndpoint(  
 endpoint\_name="endpoint-name",  
 client=client,  
 model\_kwargs={"temperature": 1e-10},  
 content\_handler=content\_handler,  
 ),  
 prompt=PROMPT,  
)  
  
chain({"input\_documents": docs, "question": query}, return\_only\_outputs=True)  

```

```python
from typing import Dict  
  
from langchain.prompts import PromptTemplate  
from langchain.llms import SagemakerEndpoint  
from langchain.llms.sagemaker\_endpoint import LLMContentHandler  
from langchain.chains.question\_answering import load\_qa\_chain  
import json  
  
query = """How long was Elizabeth hospitalized?  
"""  
  
prompt\_template = """Use the following pieces of context to answer the question at the end.  
  
{context}  
  
Question: {question}  
Answer:"""  
PROMPT = PromptTemplate(  
 template=prompt\_template, input\_variables=["context", "question"]  
)  
  
  
class ContentHandler(LLMContentHandler):  
 content\_type = "application/json"  
 accepts = "application/json"  
  
 def transform\_input(self, prompt: str, model\_kwargs: Dict) -> bytes:  
 input\_str = json.dumps({prompt: prompt, \*\*model\_kwargs})  
 return input\_str.encode("utf-8")  
  
 def transform\_output(self, output: bytes) -> str:  
 response\_json = json.loads(output.read().decode("utf-8"))  
 return response\_json[0]["generated\_text"]  
  
  
content\_handler = ContentHandler()  
  
chain = load\_qa\_chain(  
 llm=SagemakerEndpoint(  
 endpoint\_name="endpoint-name",  
 credentials\_profile\_name="credentials-profile-name",  
 region\_name="us-west-2",  
 model\_kwargs={"temperature": 1e-10},  
 content\_handler=content\_handler,  
 ),  
 prompt=PROMPT,  
)  
  
chain({"input\_documents": docs, "question": query}, return\_only\_outputs=True)  

```

- [Set up](#set-up)

- [Example](#example)

- [Example to initialize with external boto3 session](#example-to-initialize-with-external-boto3-session)

  - [for cross account scenarios](#for-cross-account-scenarios)

- [for cross account scenarios](#for-cross-account-scenarios)

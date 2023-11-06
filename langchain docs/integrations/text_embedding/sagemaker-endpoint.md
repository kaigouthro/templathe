# SageMaker

Let's load the `SageMaker Endpoints Embeddings` class. The class can be used if you host, e.g. your own Hugging Face model on SageMaker.

For instructions on how to do this, please see [here](https://www.philschmid.de/custom-inference-huggingface-sagemaker).

**Note**: In order to handle batched requests, you will need to adjust the return line in the `predict_fn()` function within the custom `inference.py` script:

Change from

`return {"vectors": sentence_embeddings[0].tolist()}`

to:

`return {"vectors": sentence_embeddings.tolist()}`.

```bash
pip3 install langchain boto3  

```

```python
from typing import Dict, List  
from langchain.embeddings import SagemakerEndpointEmbeddings  
from langchain.embeddings.sagemaker\_endpoint import EmbeddingsContentHandler  
import json  
import boto3  
  
class ContentHandler(EmbeddingsContentHandler):  
 content\_type = "application/json"  
 accepts = "application/json"  
  
 def transform\_input(self, inputs: list[str], model\_kwargs: Dict) -> bytes:  
 """  
 Transforms the input into bytes that can be consumed by SageMaker endpoint.  
 Args:  
 inputs: List of input strings.  
 model\_kwargs: Additional keyword arguments to be passed to the endpoint.  
 Returns:  
 The transformed bytes input.  
 """  
 # Example: inference.py expects a JSON string with a "inputs" key:  
 input\_str = json.dumps({"inputs": inputs, \*\*model\_kwargs})   
 return input\_str.encode("utf-8")  
  
 def transform\_output(self, output: bytes) -> List[List[float]]:  
 """  
 Transforms the bytes output from the endpoint into a list of embeddings.  
 Args:  
 output: The bytes output from SageMaker endpoint.  
 Returns:  
 The transformed output - list of embeddings  
 Note:  
 The length of the outer list is the number of input strings.  
 The length of the inner lists is the embedding dimension.  
 """  
 # Example: inference.py returns a JSON string with the list of  
 # embeddings in a "vectors" key:  
 response\_json = json.loads(output.read().decode("utf-8"))  
 return response\_json["vectors"]  
  
  
content\_handler = ContentHandler()  
  
  
embeddings = SagemakerEndpointEmbeddings(  
 # credentials\_profile\_name="credentials-profile-name",  
 endpoint\_name="huggingface-pytorch-inference-2023-03-21-16-14-03-834",  
 region\_name="us-east-1",  
 content\_handler=content\_handler,  
)  
  
  
# client = boto3.client(  
# "sagemaker-runtime",  
# region\_name="us-west-2"   
# )  
# embeddings = SagemakerEndpointEmbeddings(  
# endpoint\_name="huggingface-pytorch-inference-2023-03-21-16-14-03-834",   
# client=client  
# content\_handler=content\_handler,  
# )  

```

```python
query\_result = embeddings.embed\_query("foo")  

```

```python
doc\_results = embeddings.embed\_documents(["foo"])  

```

```python
doc\_results  

```

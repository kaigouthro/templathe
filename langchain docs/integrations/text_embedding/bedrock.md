# Bedrock

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is a fully managed service that makes FMs from leading AI startups and Amazon available via an API, so you can choose from a wide range of FMs to find the model that is best suited for your use case.

```python
%pip install boto3  

```

```python
from langchain.embeddings import BedrockEmbeddings  
  
embeddings = BedrockEmbeddings(  
 credentials\_profile\_name="bedrock-admin", region\_name="us-east-1"  
)  

```

```python
embeddings.embed\_query("This is a content of the document")  

```

```python
embeddings.embed\_documents(["This is a content of the document", "This is another document"])  

```

```python
# async embed query  
await embeddings.aembed\_query("This is a content of the document")  

```

```python
# async embed documents  
await embeddings.aembed\_documents(["This is a content of the document", "This is another document"])  

```

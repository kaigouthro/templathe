# Google Vertex AI Vector Search

This notebook shows how to use functionality related to the `Google Cloud Vertex AI Vector Search` vector database.

[Google Vertex AI Vector Search](https://cloud.google.com/vertex-ai/docs/matching-engine/overview), formerly known as Vertex AI Matching Engine, provides the industry's leading high-scale low latency vector database. These vector databases are commonly referred to as vector similarity-matching or an approximate nearest neighbor (ANN) service.

**Note**: This module expects an endpoint and deployed index already created as the creation time takes close to one hour. To see how to create an index refer to the section [Create Index and deploy it to an Endpoint](#create-index-and-deploy-it-to-an-endpoint)

## Create VectorStore from texts[​](#create-vectorstore-from-texts "Direct link to Create VectorStore from texts")

```python
from langchain.vectorstores import MatchingEngine  

```

```python
texts = [  
 "The cat sat on",  
 "the mat.",  
 "I like to",  
 "eat pizza for",  
 "dinner.",  
 "The sun sets",  
 "in the west.",  
]  
  
  
vector\_store = MatchingEngine.from\_components(  
 texts=texts,  
 project\_id="<my\_project\_id>",  
 region="<my\_region>",  
 gcs\_bucket\_uri="<my\_gcs\_bucket>",  
 index\_id="<my\_matching\_engine\_index\_id>",  
 endpoint\_id="<my\_matching\_engine\_endpoint\_id>",  
)  
  
vector\_store.add\_texts(texts=texts)  
  
vector\_store.similarity\_search("lunch", k=2)  

```

## Create Index and deploy it to an Endpoint[​](#create-index-and-deploy-it-to-an-endpoint "Direct link to Create Index and deploy it to an Endpoint")

### Imports, Constants and Configs[​](#imports-constants-and-configs "Direct link to Imports, Constants and Configs")

```bash
# Installing dependencies.  
pip install tensorflow \  
 google-cloud-aiplatform \  
 tensorflow-hub \  
 tensorflow-text  

```

```python
import os  
import json  
  
from google.cloud import aiplatform  
import tensorflow\_hub as hub  
import tensorflow\_text  

```

```python
PROJECT\_ID = "<my\_project\_id>"  
REGION = "<my\_region>"  
VPC\_NETWORK = "<my\_vpc\_network\_name>"  
PEERING\_RANGE\_NAME = "ann-langchain-me-range" # Name for creating the VPC peering.  
BUCKET\_URI = "gs://<bucket\_uri>"  
# The number of dimensions for the tensorflow universal sentence encoder.  
# If other embedder is used, the dimensions would probably need to change.  
DIMENSIONS = 512  
DISPLAY\_NAME = "index-test-name"  
EMBEDDING\_DIR = f"{BUCKET\_URI}/banana"  
DEPLOYED\_INDEX\_ID = "endpoint-test-name"  
  
PROJECT\_NUMBER = !gcloud projects list --filter="PROJECT\_ID:'{PROJECT\_ID}'" --format='value(PROJECT\_NUMBER)'  
PROJECT\_NUMBER = PROJECT\_NUMBER[0]  
VPC\_NETWORK\_FULL = f"projects/{PROJECT\_NUMBER}/global/networks/{VPC\_NETWORK}"  
  
# Change this if you need the VPC to be created.  
CREATE\_VPC = False  

```

```bash
# Set the project id  
 gcloud config set project {PROJECT\_ID}  

```

```bash
# Remove the if condition to run the encapsulated code  
if CREATE\_VPC:  
 # Create a VPC network  
 gcloud compute networks create {VPC\_NETWORK} --bgp-routing-mode=regional --subnet-mode=auto --project={PROJECT\_ID}  
  
 # Add necessary firewall rules  
 gcloud compute firewall-rules create {VPC\_NETWORK}-allow-icmp --network {VPC\_NETWORK} --priority 65534 --project {PROJECT\_ID} --allow icmp  
 gcloud compute firewall-rules create {VPC\_NETWORK}-allow-internal --network {VPC\_NETWORK} --priority 65534 --project {PROJECT\_ID} --allow all --source-ranges 10.128.0.0/9  
 gcloud compute firewall-rules create {VPC\_NETWORK}-allow-rdp --network {VPC\_NETWORK} --priority 65534 --project {PROJECT\_ID} --allow tcp:3389  
 gcloud compute firewall-rules create {VPC\_NETWORK}-allow-ssh --network {VPC\_NETWORK} --priority 65534 --project {PROJECT\_ID} --allow tcp:22  
  
 # Reserve IP range  
 gcloud compute addresses create {PEERING\_RANGE\_NAME} --global --prefix-length=16 --network={VPC\_NETWORK} --purpose=VPC\_PEERING --project={PROJECT\_ID} --description="peering range"  
  
 # Set up peering with service networking  
 # Your account must have the "Compute Network Admin" role to run the following.  
 gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --network={VPC\_NETWORK} --ranges={PEERING\_RANGE\_NAME} --project={PROJECT\_ID}  

```

```bash
# Creating bucket.  
 gsutil mb -l $REGION -p $PROJECT\_ID $BUCKET\_URI  

```

### Using Tensorflow Universal Sentence Encoder as an Embedder[​](#using-tensorflow-universal-sentence-encoder-as-an-embedder "Direct link to Using Tensorflow Universal Sentence Encoder as an Embedder")

```python
# Load the Universal Sentence Encoder module  
module\_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"  
model = hub.load(module\_url)  

```

```python
# Generate embeddings for each word  
embeddings = model(["banana"])  

```

### Inserting a test embedding[​](#inserting-a-test-embedding "Direct link to Inserting a test embedding")

```bash
initial\_config = {  
 "id": "banana\_id",  
 "embedding": [float(x) for x in list(embeddings.numpy()[0])],  
}  
  
with open("data.json", "w") as f:  
 json.dump(initial\_config, f)  
gsutil cp data.json {EMBEDDING\_DIR}/file.json  

```

```python
aiplatform.init(project=PROJECT\_ID, location=REGION, staging\_bucket=BUCKET\_URI)  

```

### Creating Index[​](#creating-index "Direct link to Creating Index")

```python
my\_index = aiplatform.MatchingEngineIndex.create\_tree\_ah\_index(  
 display\_name=DISPLAY\_NAME,  
 contents\_delta\_uri=EMBEDDING\_DIR,  
 dimensions=DIMENSIONS,  
 approximate\_neighbors\_count=150,  
 distance\_measure\_type="DOT\_PRODUCT\_DISTANCE",  
)  

```

### Creating Endpoint[​](#creating-endpoint "Direct link to Creating Endpoint")

```python
my\_index\_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(  
 display\_name=f"{DISPLAY\_NAME}-endpoint",  
 network=VPC\_NETWORK\_FULL,  
)  

```

### Deploy Index[​](#deploy-index "Direct link to Deploy Index")

```python
my\_index\_endpoint = my\_index\_endpoint.deploy\_index(  
 index=my\_index, deployed\_index\_id=DEPLOYED\_INDEX\_ID  
)  
  
my\_index\_endpoint.deployed\_indexes  

```

- [Create VectorStore from texts](#create-vectorstore-from-texts)

- [Create Index and deploy it to an Endpoint](#create-index-and-deploy-it-to-an-endpoint)

  - [Imports, Constants and Configs](#imports-constants-and-configs)
  - [Using Tensorflow Universal Sentence Encoder as an Embedder](#using-tensorflow-universal-sentence-encoder-as-an-embedder)
  - [Inserting a test embedding](#inserting-a-test-embedding)
  - [Creating Index](#creating-index)
  - [Creating Endpoint](#creating-endpoint)
  - [Deploy Index](#deploy-index)

- [Imports, Constants and Configs](#imports-constants-and-configs)

- [Using Tensorflow Universal Sentence Encoder as an Embedder](#using-tensorflow-universal-sentence-encoder-as-an-embedder)

- [Inserting a test embedding](#inserting-a-test-embedding)

- [Creating Index](#creating-index)

- [Creating Endpoint](#creating-endpoint)

- [Deploy Index](#deploy-index)

# Datadog Logs

[Datadog](https://www.datadoghq.com/) is a monitoring and analytics platform for cloud-scale applications.

This loader fetches the logs from your applications in Datadog using the `datadog_api_client` Python package. You must initialize the loader with your `Datadog API key` and `APP key`, and you need to pass in the query to extract the desired logs.

```python
from langchain.document\_loaders import DatadogLogsLoader  

```

```python
#!pip install datadog-api-client  

```

```python
query = "service:agent status:error"  
  
loader = DatadogLogsLoader(  
 query=query,  
 api\_key=DD\_API\_KEY,  
 app\_key=DD\_APP\_KEY,  
 from\_time=1688732708951, # Optional, timestamp in milliseconds  
 to\_time=1688736308951, # Optional, timestamp in milliseconds  
 limit=100, # Optional, default is 100  
)  

```

```python
documents = loader.load()  
documents  

```

```text
 [Document(page\_content='message: grep: /etc/datadog-agent/system-probe.yaml: No such file or directory', metadata={'id': 'AgAAAYkwpLImvkjRpQAAAAAAAAAYAAAAAEFZa3dwTUFsQUFEWmZfLU5QdElnM3dBWQAAACQAAAAAMDE4OTMwYTQtYzk3OS00MmJjLTlhNDAtOTY4N2EwY2I5ZDdk', 'status': 'error', 'service': 'agent', 'tags': ['accessible-from-goog-gke-node', 'allow-external-ingress-high-ports', 'allow-external-ingress-http', 'allow-external-ingress-https', 'container\_id:c7d8ecd27b5b3cfdf3b0df04b8965af6f233f56b7c3c2ffabfab5e3b6ccbd6a5', 'container\_name:lab\_datadog\_1', 'datadog.pipelines:false', 'datadog.submission\_auth:private\_api\_key', 'docker\_image:datadog/agent:7.41.1', 'env:dd101-dev', 'hostname:lab-host', 'image\_name:datadog/agent', 'image\_tag:7.41.1', 'instance-id:7497601202021312403', 'instance-type:custom-1-4096', 'instruqt\_aws\_accounts:', 'instruqt\_azure\_subscriptions:', 'instruqt\_gcp\_projects:', 'internal-hostname:lab-host.d4rjybavkary.svc.cluster.local', 'numeric\_project\_id:3390740675', 'p-d4rjybavkary', 'project:instruqt-prod', 'service:agent', 'short\_image:agent', 'source:agent', 'zone:europe-west1-b'], 'timestamp': datetime.datetime(2023, 7, 7, 13, 57, 27, 206000, tzinfo=tzutc())}),  
 Document(page\_content='message: grep: /etc/datadog-agent/system-probe.yaml: No such file or directory', metadata={'id': 'AgAAAYkwpLImvkjRpgAAAAAAAAAYAAAAAEFZa3dwTUFsQUFEWmZfLU5QdElnM3dBWgAAACQAAAAAMDE4OTMwYTQtYzk3OS00MmJjLTlhNDAtOTY4N2EwY2I5ZDdk', 'status': 'error', 'service': 'agent', 'tags': ['accessible-from-goog-gke-node', 'allow-external-ingress-high-ports', 'allow-external-ingress-http', 'allow-external-ingress-https', 'container\_id:c7d8ecd27b5b3cfdf3b0df04b8965af6f233f56b7c3c2ffabfab5e3b6ccbd6a5', 'container\_name:lab\_datadog\_1', 'datadog.pipelines:false', 'datadog.submission\_auth:private\_api\_key', 'docker\_image:datadog/agent:7.41.1', 'env:dd101-dev', 'hostname:lab-host', 'image\_name:datadog/agent', 'image\_tag:7.41.1', 'instance-id:7497601202021312403', 'instance-type:custom-1-4096', 'instruqt\_aws\_accounts:', 'instruqt\_azure\_subscriptions:', 'instruqt\_gcp\_projects:', 'internal-hostname:lab-host.d4rjybavkary.svc.cluster.local', 'numeric\_project\_id:3390740675', 'p-d4rjybavkary', 'project:instruqt-prod', 'service:agent', 'short\_image:agent', 'source:agent', 'zone:europe-west1-b'], 'timestamp': datetime.datetime(2023, 7, 7, 13, 57, 27, 206000, tzinfo=tzutc())})]  

```

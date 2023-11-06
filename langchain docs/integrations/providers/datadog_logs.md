# Datadog Logs

[Datadog](https://www.datadoghq.com/) is a monitoring and analytics platform for cloud-scale applications.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install datadog\_api\_client  

```

We must initialize the loader with the Datadog API key and APP key, and we need to set up the query to extract the desired logs.

## Document Loader[​](#document-loader "Direct link to Document Loader")

See a [usage example](/docs/integrations/document_loaders/datadog_logs).

```python
from langchain.document\_loaders import DatadogLogsLoader  

```

- [Installation and Setup](#installation-and-setup)
- [Document Loader](#document-loader)

# Airbyte

[Airbyte](https://github.com/airbytehq/airbyte) is a data integration platform for ELT pipelines from APIs,
databases & files to warehouses & lakes. It has the largest catalog of ELT connectors to data warehouses and databases.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

This instruction shows how to load any source from `Airbyte` into a local `JSON` file that can be read in as a document.

**Prerequisites:**
Have `docker desktop` installed.

**Steps:**

1. Clone Airbyte from GitHub - `git clone https://github.com/airbytehq/airbyte.git`.
1. Switch into Airbyte directory - `cd airbyte`.
1. Start Airbyte - `docker compose up`.
1. In your browser, just visit http://localhost:8000. You will be asked for a username and password. By default, that's username `airbyte` and password `password`.
1. Setup any source you wish.
1. Set destination as Local JSON, with specified destination path - lets say `/json_data`. Set up a manual sync.
1. Run the connection.
1. To see what files are created, navigate to: `file:///tmp/airbyte_local/`.

## Document Loader[​](#document-loader "Direct link to Document Loader")

See a [usage example](/docs/integrations/document_loaders/airbyte_json).

```python
from langchain.document\_loaders import AirbyteJSONLoader  

```

- [Installation and Setup](#installation-and-setup)
- [Document Loader](#document-loader)

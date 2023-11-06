# Alibaba Cloud MaxCompute

[Alibaba Cloud MaxCompute](https://www.alibabacloud.com/product/maxcompute) (previously known as ODPS) is a general purpose, fully managed, multi-tenancy data processing platform for large-scale data warehousing. MaxCompute supports various data importing solutions and distributed computing models, enabling users to effectively query massive datasets, reduce production costs, and ensure data security.

The `MaxComputeLoader` lets you execute a MaxCompute SQL query and loads the results as one document per row.

```bash
pip install pyodps  

```

```text
 Collecting pyodps  
 Downloading pyodps-0.11.4.post0-cp39-cp39-macosx\_10\_9\_universal2.whl (2.0 MB)  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 1.7 MB/s eta 0:00:0000:0100:010m  
 Requirement already satisfied: charset-normalizer>=2 in /Users/newboy/anaconda3/envs/langchain/lib/python3.9/site-packages (from pyodps) (3.1.0)  
 Requirement already satisfied: urllib3<2.0,>=1.26.0 in /Users/newboy/anaconda3/envs/langchain/lib/python3.9/site-packages (from pyodps) (1.26.15)  
 Requirement already satisfied: idna>=2.5 in /Users/newboy/anaconda3/envs/langchain/lib/python3.9/site-packages (from pyodps) (3.4)  
 Requirement already satisfied: certifi>=2017.4.17 in /Users/newboy/anaconda3/envs/langchain/lib/python3.9/site-packages (from pyodps) (2023.5.7)  
 Installing collected packages: pyodps  
 Successfully installed pyodps-0.11.4.post0  

```

## Basic Usage[​](#basic-usage "Direct link to Basic Usage")

To instantiate the loader you'll need a SQL query to execute, your MaxCompute endpoint and project name, and you access ID and secret access key. The access ID and secret access key can either be passed in direct via the `access_id` and `secret_access_key` parameters or they can be set as environment variables `MAX_COMPUTE_ACCESS_ID` and `MAX_COMPUTE_SECRET_ACCESS_KEY`.

```python
from langchain.document\_loaders import MaxComputeLoader  

```

```python
base\_query = """  
SELECT \*  
FROM (  
 SELECT 1 AS id, 'content1' AS content, 'meta\_info1' AS meta\_info  
 UNION ALL  
 SELECT 2 AS id, 'content2' AS content, 'meta\_info2' AS meta\_info  
 UNION ALL  
 SELECT 3 AS id, 'content3' AS content, 'meta\_info3' AS meta\_info  
) mydata;  
"""  

```

```python
endpoint = "<ENDPOINT>"  
project = "<PROJECT>"  
ACCESS\_ID = "<ACCESS ID>"  
SECRET\_ACCESS\_KEY = "<SECRET ACCESS KEY>"  

```

```python
loader = MaxComputeLoader.from\_params(  
 base\_query,  
 endpoint,  
 project,  
 access\_id=ACCESS\_ID,  
 secret\_access\_key=SECRET\_ACCESS\_KEY,  
)  
data = loader.load()  

```

```python
print(data)  

```

```text
 [Document(page\_content='id: 1\ncontent: content1\nmeta\_info: meta\_info1', metadata={}), Document(page\_content='id: 2\ncontent: content2\nmeta\_info: meta\_info2', metadata={}), Document(page\_content='id: 3\ncontent: content3\nmeta\_info: meta\_info3', metadata={})]  

```

```python
print(data[0].page\_content)  

```

```text
 id: 1  
 content: content1  
 meta\_info: meta\_info1  

```

```python
print(data[0].metadata)  

```

```text
 {}  

```

## Specifying Which Columns are Content vs Metadata[​](#specifying-which-columns-are-content-vs-metadata "Direct link to Specifying Which Columns are Content vs Metadata")

You can configure which subset of columns should be loaded as the contents of the Document and which as the metadata using the `page_content_columns` and `metadata_columns` parameters.

```python
loader = MaxComputeLoader.from\_params(  
 base\_query,  
 endpoint,  
 project,  
 page\_content\_columns=["content"], # Specify Document page content  
 metadata\_columns=["id", "meta\_info"], # Specify Document metadata  
 access\_id=ACCESS\_ID,  
 secret\_access\_key=SECRET\_ACCESS\_KEY,  
)  
data = loader.load()  

```

```python
print(data[0].page\_content)  

```

```text
 content: content1  

```

```python
print(data[0].metadata)  

```

```text
 {'id': 1, 'meta\_info': 'meta\_info1'}  

```

- [Basic Usage](#basic-usage)
- [Specifying Which Columns are Content vs Metadata](#specifying-which-columns-are-content-vs-metadata)

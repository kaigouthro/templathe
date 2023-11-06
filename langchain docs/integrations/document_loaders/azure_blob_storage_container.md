# Azure Blob Storage Container

[Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) is Microsoft's object storage solution for the cloud. Blob Storage is optimized for storing massive amounts of unstructured data. Unstructured data is data that doesn't adhere to a particular data model or definition, such as text or binary data.

`Azure Blob Storage` is designed for:

- Serving images or documents directly to a browser.
- Storing files for distributed access.
- Streaming video and audio.
- Writing to log files.
- Storing data for backup and restore, disaster recovery, and archiving.
- Storing data for analysis by an on-premises or Azure-hosted service.

This notebook covers how to load document objects from a container on `Azure Blob Storage`.

```python
#!pip install azure-storage-blob  

```

```python
from langchain.document\_loaders import AzureBlobStorageContainerLoader  

```

```python
loader = AzureBlobStorageContainerLoader(conn\_str="<conn\_str>", container="<container>")  

```

```python
loader.load()  

```

```text
 [Document(page\_content='Lorem ipsum dolor sit amet.', lookup\_str='', metadata={'source': '/var/folders/y6/8\_bzdg295ld6s1\_97\_12m4lr0000gn/T/tmpaa9xl6ch/fake.docx'}, lookup\_index=0)]  

```

## Specifying a prefix[​](#specifying-a-prefix "Direct link to Specifying a prefix")

You can also specify a prefix for more finegrained control over what files to load.

```python
loader = AzureBlobStorageContainerLoader(  
 conn\_str="<conn\_str>", container="<container>", prefix="<prefix>"  
)  

```

```python
loader.load()  

```

```text
 [Document(page\_content='Lorem ipsum dolor sit amet.', lookup\_str='', metadata={'source': '/var/folders/y6/8\_bzdg295ld6s1\_97\_12m4lr0000gn/T/tmpujbkzf\_l/fake.docx'}, lookup\_index=0)]  

```

- [Specifying a prefix](#specifying-a-prefix)

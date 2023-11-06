# Azure Blob Storage File

[Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-introduction) offers fully managed file shares in the cloud that are accessible via the industry standard Server Message Block (`SMB`) protocol, Network File System (`NFS`) protocol, and `Azure Files REST API`.

This covers how to load document objects from a Azure Files.

```python
#!pip install azure-storage-blob  

```

```python
from langchain.document\_loaders import AzureBlobStorageFileLoader  

```

```python
loader = AzureBlobStorageFileLoader(  
 conn\_str="<connection string>",  
 container="<container name>",  
 blob\_name="<blob name>",  
)  

```

```python
loader.load()  

```

```text
 [Document(page\_content='Lorem ipsum dolor sit amet.', lookup\_str='', metadata={'source': '/var/folders/y6/8\_bzdg295ld6s1\_97\_12m4lr0000gn/T/tmpxvave6wl/fake.docx'}, lookup\_index=0)]  

```

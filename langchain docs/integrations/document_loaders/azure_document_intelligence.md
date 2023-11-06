# Azure Document Intelligence

Azure Document Intelligence (formerly known as Azure Forms Recognizer) is machine-learning
based service that extracts text (including handwriting), tables or key-value-pairs from
scanned documents or images.

This current implementation of a loader using Document Intelligence is able to incorporate content page-wise and turn it into LangChain documents.

Document Intelligence supports PDF, JPEG, PNG, BMP, or TIFF.

Further documentation is available at <https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/?view=doc-intel-3.1.0>.

```python
%pip install langchain azure-ai-formrecognizer -q  

```

## Example 1[​](#example-1 "Direct link to Example 1")

The first example uses a local file which will be sent to Azure Document Intelligence.

First, an instance of a DocumentAnalysisClient is created with endpoint and key for the Azure service.

```python
from azure.ai.formrecognizer import DocumentAnalysisClient  
from azure.core.credentials import AzureKeyCredential  
  
document\_analysis\_client = DocumentAnalysisClient(  
 endpoint="<service\_endpoint>", credential=AzureKeyCredential("<service\_key>")  
 )  

```

With the initialized document analysis client, we can proceed to create an instance of the DocumentIntelligenceLoader:

```python
from langchain.document\_loaders.pdf import DocumentIntelligenceLoader  
loader = DocumentIntelligenceLoader(  
 "<Local\_filename>",  
 client=document\_analysis\_client,  
 model="<model\_name>") # e.g. prebuilt-document  
  
documents = loader.load()  

```

The output contains each page of the source document as a LangChain document:

```python
documents  

```

```text
 [Document(page\_content='...', metadata={'source': '...', 'page': 1})]  

```

- [Example 1](#example-1)

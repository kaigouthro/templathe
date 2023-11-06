# Google Cloud Storage Directory

[Google Cloud Storage](https://en.wikipedia.org/wiki/Google_Cloud_Storage) is a managed service for storing unstructured data.

This covers how to load document objects from an `Google Cloud Storage (GCS) directory (bucket)`.

```python
# !pip install google-cloud-storage  

```

```python
from langchain.document\_loaders import GCSDirectoryLoader  

```

```python
loader = GCSDirectoryLoader(project\_name="aist", bucket="testing-hwc")  

```

```python
loader.load()  

```

```text
 /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/\_default.py:83: UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK without a quota project. You might receive a "quota exceeded" or "API not enabled" error. We recommend you rerun `gcloud auth application-default login` and make sure a quota project is added. Or you can use service accounts instead. For more information about service accounts, see https://cloud.google.com/docs/authentication/  
 warnings.warn(\_CLOUD\_SDK\_CREDENTIALS\_WARNING)  
 /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/\_default.py:83: UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK without a quota project. You might receive a "quota exceeded" or "API not enabled" error. We recommend you rerun `gcloud auth application-default login` and make sure a quota project is added. Or you can use service accounts instead. For more information about service accounts, see https://cloud.google.com/docs/authentication/  
 warnings.warn(\_CLOUD\_SDK\_CREDENTIALS\_WARNING)  
  
  
  
  
  
 [Document(page\_content='Lorem ipsum dolor sit amet.', lookup\_str='', metadata={'source': '/var/folders/y6/8\_bzdg295ld6s1\_97\_12m4lr0000gn/T/tmpz37njh7u/fake.docx'}, lookup\_index=0)]  

```

## Specifying a prefix[​](#specifying-a-prefix "Direct link to Specifying a prefix")

You can also specify a prefix for more finegrained control over what files to load.

```python
loader = GCSDirectoryLoader(project\_name="aist", bucket="testing-hwc", prefix="fake")  

```

```python
loader.load()  

```

```text
 /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/\_default.py:83: UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK without a quota project. You might receive a "quota exceeded" or "API not enabled" error. We recommend you rerun `gcloud auth application-default login` and make sure a quota project is added. Or you can use service accounts instead. For more information about service accounts, see https://cloud.google.com/docs/authentication/  
 warnings.warn(\_CLOUD\_SDK\_CREDENTIALS\_WARNING)  
 /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/\_default.py:83: UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK without a quota project. You might receive a "quota exceeded" or "API not enabled" error. We recommend you rerun `gcloud auth application-default login` and make sure a quota project is added. Or you can use service accounts instead. For more information about service accounts, see https://cloud.google.com/docs/authentication/  
 warnings.warn(\_CLOUD\_SDK\_CREDENTIALS\_WARNING)  
  
  
  
  
  
 [Document(page\_content='Lorem ipsum dolor sit amet.', lookup\_str='', metadata={'source': '/var/folders/y6/8\_bzdg295ld6s1\_97\_12m4lr0000gn/T/tmpylg6291i/fake.docx'}, lookup\_index=0)]  

```

- [Specifying a prefix](#specifying-a-prefix)

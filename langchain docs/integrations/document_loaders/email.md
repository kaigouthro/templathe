# Email

This notebook shows how to load email (`.eml`) or `Microsoft Outlook` (`.msg`) files.

## Using Unstructured[​](#using-unstructured "Direct link to Using Unstructured")

```python
#!pip install unstructured  

```

```python
from langchain.document\_loaders import UnstructuredEmailLoader  

```

```python
loader = UnstructuredEmailLoader("example\_data/fake-email.eml")  

```

```python
data = loader.load()  

```

```python
data  

```

```text
 [Document(page\_content='This is a test email to use for unit tests.\n\nImportant points:\n\nRoses are red\n\nViolets are blue', metadata={'source': 'example\_data/fake-email.eml'})]  

```

### Retain Elements[​](#retain-elements "Direct link to Retain Elements")

Under the hood, Unstructured creates different "elements" for different chunks of text. By default we combine those together, but you can easily keep that separation by specifying `mode="elements"`.

```python
loader = UnstructuredEmailLoader("example\_data/fake-email.eml", mode="elements")  

```

```python
data = loader.load()  

```

```python
data[0]  

```

```text
 Document(page\_content='This is a test email to use for unit tests.', metadata={'source': 'example\_data/fake-email.eml', 'filename': 'fake-email.eml', 'file\_directory': 'example\_data', 'date': '2022-12-16T17:04:16-05:00', 'filetype': 'message/rfc822', 'sent\_from': ['Matthew Robinson <mrobinson@unstructured.io>'], 'sent\_to': ['Matthew Robinson <mrobinson@unstructured.io>'], 'subject': 'Test Email', 'category': 'NarrativeText'})  

```

### Processing Attachments[​](#processing-attachments "Direct link to Processing Attachments")

You can process attachments with `UnstructuredEmailLoader` by setting `process_attachments=True` in the constructor. By default, attachments will be partitioned using the `partition` function from `unstructured`. You can use a different partitioning function by passing the function to the `attachment_partitioner` kwarg.

```python
loader = UnstructuredEmailLoader(  
 "example\_data/fake-email.eml",  
 mode="elements",  
 process\_attachments=True,  
)  

```

```python
data = loader.load()  

```

```python
data[0]  

```

```text
 Document(page\_content='This is a test email to use for unit tests.', metadata={'source': 'example\_data/fake-email.eml', 'filename': 'fake-email.eml', 'file\_directory': 'example\_data', 'date': '2022-12-16T17:04:16-05:00', 'filetype': 'message/rfc822', 'sent\_from': ['Matthew Robinson <mrobinson@unstructured.io>'], 'sent\_to': ['Matthew Robinson <mrobinson@unstructured.io>'], 'subject': 'Test Email', 'category': 'NarrativeText'})  

```

## Using OutlookMessageLoader[​](#using-outlookmessageloader "Direct link to Using OutlookMessageLoader")

```python
#!pip install extract\_msg  

```

```python
from langchain.document\_loaders import OutlookMessageLoader  

```

```python
loader = OutlookMessageLoader("example\_data/fake-email.msg")  

```

```python
data = loader.load()  

```

```python
data[0]  

```

```text
 Document(page\_content='This is a test email to experiment with the MS Outlook MSG Extractor\r\n\r\n\r\n-- \r\n\r\n\r\nKind regards\r\n\r\n\r\n\r\n\r\nBrian Zhou\r\n\r\n', metadata={'subject': 'Test for TIF files', 'sender': 'Brian Zhou <brizhou@gmail.com>', 'date': 'Mon, 18 Nov 2013 16:26:24 +0800'})  

```

- [Using Unstructured](#using-unstructured)

  - [Retain Elements](#retain-elements)
  - [Processing Attachments](#processing-attachments)

- [Using OutlookMessageLoader](#using-outlookmessageloader)

- [Retain Elements](#retain-elements)

- [Processing Attachments](#processing-attachments)

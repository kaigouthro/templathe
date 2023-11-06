# Tencent COS File

This covers how to load document object from a `Tencent COS File`.

```python
#! pip install cos-python-sdk-v5  

```

```python
from langchain.document\_loaders import TencentCOSFileLoader  
from qcloud\_cos import CosConfig  

```

```python
conf = CosConfig(  
 Region="your cos region",  
 SecretId="your cos secret\_id",  
 SecretKey="your cos secret\_key",  
)  
loader = TencentCOSFileLoader(conf=conf, bucket="you\_cos\_bucket", key="fake.docx")  

```

```python
loader.load()  

```

# Tencent COS Directory

This covers how to load document objects from a `Tencent COS Directory`.

```python
#! pip install cos-python-sdk-v5  

```

```python
from langchain.document\_loaders import TencentCOSDirectoryLoader  
from qcloud\_cos import CosConfig  

```

```python
conf = CosConfig(  
 Region="your cos region",  
 SecretId="your cos secret\_id",  
 SecretKey="your cos secret\_key",  
)  
loader = TencentCOSDirectoryLoader(conf=conf, bucket="you\_cos\_bucket")  

```

```python
loader.load()  

```

## Specifying a prefix[​](#specifying-a-prefix "Direct link to Specifying a prefix")

You can also specify a prefix for more finegrained control over what files to load.

```python
loader = TencentCOSDirectoryLoader(conf=conf, bucket="you\_cos\_bucket", prefix="fake")  

```

```python
loader.load()  

```

- [Specifying a prefix](#specifying-a-prefix)

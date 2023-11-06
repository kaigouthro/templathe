# Huawei OBS File

The following code demonstrates how to load an object from the Huawei OBS (Object Storage Service) as document.

```python
# Install the required package  
# pip install esdk-obs-python  

```

```python
from langchain.document\_loaders.obs\_file import OBSFileLoader  

```

```python
endpoint = "your-endpoint"  

```

```python
from obs import ObsClient  
obs\_client = ObsClient(access\_key\_id="your-access-key", secret\_access\_key="your-secret-key", server=endpoint)  
loader = OBSFileLoader("your-bucket-name", "your-object-key", client=obs\_client)  

```

```python
loader.load()  

```

## Each Loader with Separate Authentication Information[​](#each-loader-with-separate-authentication-information "Direct link to Each Loader with Separate Authentication Information")

If you don't need to reuse OBS connections between different loaders, you can directly configure the `config`. The loader will use the config information to initialize its own OBS client.

```python
# Configure your access credentials\n  
config = {  
 "ak": "your-access-key",  
 "sk": "your-secret-key"  
}  
loader = OBSFileLoader("your-bucket-name", "your-object-key",endpoint=endpoint, config=config)  

```

```python
loader.load()  

```

## Get Authentication Information from ECS[​](#get-authentication-information-from-ecs "Direct link to Get Authentication Information from ECS")

If your langchain is deployed on Huawei Cloud ECS and [Agency is set up](https://support.huaweicloud.com/intl/en-us/usermanual-ecs/ecs_03_0166.html#section7), the loader can directly get the security token from ECS without needing access key and secret key.

```python
config = {"get\_token\_from\_ecs": True}  
loader = OBSFileLoader("your-bucket-name", "your-object-key", endpoint=endpoint, config=config)  

```

```python
loader.load()  

```

## Access a Publicly Accessible Object[​](#access-a-publicly-accessible-object "Direct link to Access a Publicly Accessible Object")

If the object you want to access allows anonymous user access (anonymous users have `GetObject` permission), you can directly load the object without configuring the `config` parameter.

```python
loader = OBSFileLoader("your-bucket-name", "your-object-key", endpoint=endpoint)  

```

```python
loader.load()  

```

- [Each Loader with Separate Authentication Information](#each-loader-with-separate-authentication-information)
- [Get Authentication Information from ECS](#get-authentication-information-from-ecs)
- [Access a Publicly Accessible Object](#access-a-publicly-accessible-object)

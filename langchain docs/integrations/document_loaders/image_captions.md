# Image captions

By default, the loader utilizes the pre-trained [Salesforce BLIP image captioning model](https://huggingface.co/Salesforce/blip-image-captioning-base).

This notebook shows how to use the `ImageCaptionLoader` to generate a query-able index of image captions

```python
#!pip install transformers  

```

```python
from langchain.document\_loaders import ImageCaptionLoader  

```

### Prepare a list of image urls from Wikimedia[​](#prepare-a-list-of-image-urls-from-wikimedia "Direct link to Prepare a list of image urls from Wikimedia")

```python
list\_image\_urls = [  
 "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Hyla\_japonica\_sep01.jpg/260px-Hyla\_japonica\_sep01.jpg",  
 "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Tibur%C3%B3n\_azul\_%28Prionace\_glauca%29%2C\_canal\_Fayal-Pico%2C\_islas\_Azores%2C\_Portugal%2C\_2020-07-27%2C\_DD\_14.jpg/270px-Tibur%C3%B3n\_azul\_%28Prionace\_glauca%29%2C\_canal\_Fayal-Pico%2C\_islas\_Azores%2C\_Portugal%2C\_2020-07-27%2C\_DD\_14.jpg",  
 "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Thure\_de\_Thulstrup\_-\_Battle\_of\_Shiloh.jpg/251px-Thure\_de\_Thulstrup\_-\_Battle\_of\_Shiloh.jpg",  
 "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Passion\_fruits\_-\_whole\_and\_halved.jpg/270px-Passion\_fruits\_-\_whole\_and\_halved.jpg",  
 "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Messier83\_-\_Heic1403a.jpg/277px-Messier83\_-\_Heic1403a.jpg",  
 "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/2022-01-22\_Men%27s\_World\_Cup\_at\_2021-22\_St.\_Moritz%E2%80%93Celerina\_Luge\_World\_Cup\_and\_European\_Championships\_by\_Sandro\_Halank%E2%80%93257.jpg/288px-2022-01-22\_Men%27s\_World\_Cup\_at\_2021-22\_St.\_Moritz%E2%80%93Celerina\_Luge\_World\_Cup\_and\_European\_Championships\_by\_Sandro\_Halank%E2%80%93257.jpg",  
 "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Wiesen\_Pippau\_%28Crepis\_biennis%29-20220624-RM-123950.jpg/224px-Wiesen\_Pippau\_%28Crepis\_biennis%29-20220624-RM-123950.jpg",  
]  

```

### Create the loader[​](#create-the-loader "Direct link to Create the loader")

```python
loader = ImageCaptionLoader(path\_images=list\_image\_urls)  
list\_docs = loader.load()  
list\_docs  

```

```python
from PIL import Image  
import requests  
  
Image.open(requests.get(list\_image\_urls[0], stream=True).raw).convert("RGB")  

```

### Create the index[​](#create-the-index "Direct link to Create the index")

```python
from langchain.indexes import VectorstoreIndexCreator  
  
index = VectorstoreIndexCreator().from\_loaders([loader])  

```

### Query[​](#query "Direct link to Query")

```python
query = "What's the painting about?"  
index.query(query)  

```

```python
query = "What kind of images are there?"  
index.query(query)  

```

- [Prepare a list of image urls from Wikimedia](#prepare-a-list-of-image-urls-from-wikimedia)
- [Create the loader](#create-the-loader)
- [Create the index](#create-the-index)
- [Query](#query)

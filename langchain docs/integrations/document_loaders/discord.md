# Discord

[Discord](https://discord.com/) is a VoIP and instant messaging social platform. Users have the ability to communicate with voice calls, video calls, text messaging, media and files in private chats or as part of communities called "servers". A server is a collection of persistent chat rooms and voice channels which can be accessed via invite links.

Follow these steps to download your `Discord` data:

1. Go to your **User Settings**
1. Then go to **Privacy and Safety**
1. Head over to the **Request all of my Data** and click on **Request Data** button

It might take 30 days for you to receive your data. You'll receive an email at the address which is registered with Discord. That email will have a download button using which you would be able to download your personal Discord data.

```python
import pandas as pd  
import os  

```

```python
path = input('Please enter the path to the contents of the Discord "messages" folder: ')  
li = []  
for f in os.listdir(path):  
 expected\_csv\_path = os.path.join(path, f, "messages.csv")  
 csv\_exists = os.path.isfile(expected\_csv\_path)  
 if csv\_exists:  
 df = pd.read\_csv(expected\_csv\_path, index\_col=None, header=0)  
 li.append(df)  
  
df = pd.concat(li, axis=0, ignore\_index=True, sort=False)  

```

```python
from langchain.document\_loaders.discord import DiscordChatLoader  

```

```python
loader = DiscordChatLoader(df, user\_id\_col="ID")  
print(loader.load())  

```

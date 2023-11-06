# Telegram

[Telegram Messenger](https://web.telegram.org/a/) is a globally accessible freemium, cross-platform, encrypted, cloud-based and centralized instant messaging service. The application also provides optional end-to-end encrypted chats and video calling, VoIP, file sharing and several other features.

This notebook covers how to load data from `Telegram` into a format that can be ingested into LangChain.

```python
from langchain.document\_loaders import TelegramChatFileLoader, TelegramChatApiLoader  

```

```python
loader = TelegramChatFileLoader("example\_data/telegram.json")  

```

```python
loader.load()  

```

```text
 [Document(page\_content="Henry on 2020-01-01T00:00:02: It's 2020...\n\nHenry on 2020-01-01T00:00:04: Fireworks!\n\nGrace ðŸ§¤ ðŸ\x8d’ on 2020-01-01T00:00:05: You're a minute late!\n\n", metadata={'source': 'example\_data/telegram.json'})]  

```

`TelegramChatApiLoader` loads data directly from any specified chat from Telegram. In order to export the data, you will need to authenticate your Telegram account.

You can get the API_HASH and API_ID from <https://my.telegram.org/auth?to=apps>

chat_entity – recommended to be the [entity](https://docs.telethon.dev/en/stable/concepts/entities.html?highlight=Entity#what-is-an-entity) of a channel.

```python
loader = TelegramChatApiLoader(  
 chat\_entity="<CHAT\_URL>", # recommended to use Entity here  
 api\_hash="<API HASH >",  
 api\_id="<API\_ID>",  
 user\_name="", # needed only for caching the session.  
)  

```

```python
loader.load()  

```

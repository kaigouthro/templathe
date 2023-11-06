# YouTube transcripts

[YouTube](https://www.youtube.com/) is an online video sharing and social media platform created by Google.

This notebook covers how to load documents from `YouTube transcripts`.

```python
from langchain.document\_loaders import YoutubeLoader  

```

```python
# !pip install youtube-transcript-api  

```

```python
loader = YoutubeLoader.from\_youtube\_url(  
 "https://www.youtube.com/watch?v=QsYGlZkevEg", add\_video\_info=True  
)  

```

```python
loader.load()  

```

### Add video info[​](#add-video-info "Direct link to Add video info")

```python
# ! pip install pytube  

```

```python
loader = YoutubeLoader.from\_youtube\_url(  
 "https://www.youtube.com/watch?v=QsYGlZkevEg", add\_video\_info=True  
)  
loader.load()  

```

### Add language preferences[​](#add-language-preferences "Direct link to Add language preferences")

Language param : It's a list of language codes in a descending priority, `en` by default.

translation param : It's a translate preference when the youtube does'nt have your select language, `en` by default.

```python
loader = YoutubeLoader.from\_youtube\_url(  
 "https://www.youtube.com/watch?v=QsYGlZkevEg",  
 add\_video\_info=True,  
 language=["en", "id"],  
 translation="en",  
)  
loader.load()  

```

## YouTube loader from Google Cloud[​](#youtube-loader-from-google-cloud "Direct link to YouTube loader from Google Cloud")

### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

1. Create a Google Cloud project or use an existing project
1. Enable the [Youtube Api](https://console.cloud.google.com/apis/enableflow?apiid=youtube.googleapis.com&project=sixth-grammar-344520)
1. [Authorize credentials for desktop app](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application)
1. `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib youtube-transcript-api`

### 🧑 Instructions for ingesting your Google Docs data[​](#-instructions-for-ingesting-your-google-docs-data "Direct link to 🧑 Instructions for ingesting your Google Docs data")

By default, the `GoogleDriveLoader` expects the `credentials.json` file to be `~/.credentials/credentials.json`, but this is configurable using the `credentials_file` keyword argument. Same thing with `token.json`. Note that `token.json` will be created automatically the first time you use the loader.

`GoogleApiYoutubeLoader` can load from a list of Google Docs document ids or a folder id. You can obtain your folder and document id from the URL:
Note depending on your set up, the `service_account_path` needs to be set up. See [here](https://developers.google.com/drive/api/v3/quickstart/python) for more details.

```python
from langchain.document\_loaders import GoogleApiClient, GoogleApiYoutubeLoader  
  
# Init the GoogleApiClient  
from pathlib import Path  
  
  
google\_api\_client = GoogleApiClient(credentials\_path=Path("your\_path\_creds.json"))  
  
  
# Use a Channel  
youtube\_loader\_channel = GoogleApiYoutubeLoader(  
 google\_api\_client=google\_api\_client,  
 channel\_name="Reducible",  
 captions\_language="en",  
)  
  
# Use Youtube Ids  
  
youtube\_loader\_ids = GoogleApiYoutubeLoader(  
 google\_api\_client=google\_api\_client, video\_ids=["TrdevFK\_am4"], add\_video\_info=True  
)  
  
# returns a list of Documents  
youtube\_loader\_channel.load()  

```

- [Add video info](#add-video-info)

- [Add language preferences](#add-language-preferences)

- [YouTube loader from Google Cloud](#youtube-loader-from-google-cloud)

  - [Prerequisites](#prerequisites)
  - [🧑 Instructions for ingesting your Google Docs data](#-instructions-for-ingesting-your-google-docs-data)

- [Prerequisites](#prerequisites)

- [🧑 Instructions for ingesting your Google Docs data](#-instructions-for-ingesting-your-google-docs-data)

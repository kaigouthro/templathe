# Google Drive tool

This notebook walks through connecting a LangChain to the Google Drive API.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

1. Create a Google Cloud project or use an existing project
1. Enable the [Google Drive API](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com)
1. [Authorize credentials for desktop app](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application)
1. `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

## Instructions for retrieving your Google Docs data[​](#instructions-for-retrieving-your-google-docs-data "Direct link to Instructions for retrieving your Google Docs data")

By default, the `GoogleDriveTools` and `GoogleDriveWrapper` expects the `credentials.json` file to be `~/.credentials/credentials.json`, but this is configurable using the `GOOGLE_ACCOUNT_FILE` environment variable.
The location of `token.json` use the same directory (or use the parameter `token_path`). Note that `token.json` will be created automatically the first time you use the tool.

`GoogleDriveSearchTool` can retrieve a selection of files with some requests.

By default, If you use a `folder_id`, all the files inside this folder can be retrieved to `Document`, if the name match the query.

```python
#!pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib  

```

You can obtain your folder and document id from the URL:

- Folder: <https://drive.google.com/drive/u/0/folders/1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5> -> folder id is `"1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5"`
- Document: <https://docs.google.com/document/d/1bfaMQ18_i56204VaQDVeAFpqEijJTgvurupdEDiaUQw/edit> -> document id is `"1bfaMQ18_i56204VaQDVeAFpqEijJTgvurupdEDiaUQw"`

The special value `root` is for your personal home.

```python
folder\_id="root"  
#folder\_id='1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5'  

```

By default, all files with these mime-type can be converted to `Document`.

- text/text
- text/plain
- text/html
- text/csv
- text/markdown
- image/png
- image/jpeg
- application/epub+zip
- application/pdf
- application/rtf
- application/vnd.google-apps.document (GDoc)
- application/vnd.google-apps.presentation (GSlide)
- application/vnd.google-apps.spreadsheet (GSheet)
- application/vnd.google.colaboratory (Notebook colab)
- application/vnd.openxmlformats-officedocument.presentationml.presentation (PPTX)
- application/vnd.openxmlformats-officedocument.wordprocessingml.document (DOCX)

It's possible to update or customize this. See the documentation of `GoogleDriveAPIWrapper`.

But, the corresponding packages must installed.

```python
#!pip install unstructured  

```

```python
from langchain\_googledrive.utilities.google\_drive import GoogleDriveAPIWrapper  
from langchain\_googledrive.tools.google\_drive.tool import GoogleDriveSearchTool  
  
# By default, search only in the filename.  
tool = GoogleDriveSearchTool(  
 api\_wrapper=GoogleDriveAPIWrapper(  
 folder\_id=folder\_id,  
 num\_results=2,  
 template="gdrive-query-in-folder", # Search in the body of documents  
 )  
)  

```

```python
import logging  
logging.basicConfig(level=logging.INFO)  

```

```python
tool.run("machine learning")  

```

```python
tool.description  

```

```python
from langchain.agents import load\_tools  
tools = load\_tools(["google-drive-search"],  
 folder\_id=folder\_id,  
 template="gdrive-query-in-folder",  
 )  

```

## Use within an Agent[​](#use-within-an-agent "Direct link to Use within an Agent")

```python
from langchain.llms import OpenAI  
from langchain.agents import initialize\_agent, AgentType  
llm = OpenAI(temperature=0)  
agent = initialize\_agent(  
 tools=tools,  
 llm=llm,  
 agent=AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
)  

```

```python
agent.run(  
 "Search in google drive, who is 'Yann LeCun' ?"  
)  

```

- [Prerequisites](#prerequisites)
- [Instructions for retrieving your Google Docs data](#instructions-for-retrieving-your-google-docs-data)
- [Use within an Agent](#use-within-an-agent)

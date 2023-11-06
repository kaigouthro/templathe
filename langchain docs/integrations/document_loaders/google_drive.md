# Google Drive

[Google Drive](https://en.wikipedia.org/wiki/Google_Drive) is a file storage and synchronization service developed by Google.

This notebook covers how to load documents from `Google Drive`. Currently, only `Google Docs` are supported.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

1. Create a Google Cloud project or use an existing project
1. Enable the [Google Drive API](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com)
1. [Authorize credentials for desktop app](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application)
1. `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

## 🧑 Instructions for ingesting your Google Docs data[​](#-instructions-for-ingesting-your-google-docs-data "Direct link to 🧑 Instructions for ingesting your Google Docs data")

By default, the `GoogleDriveLoader` expects the `credentials.json` file to be `~/.credentials/credentials.json`, but this is configurable using the `credentials_path` keyword argument. Same thing with `token.json` - `token_path`. Note that `token.json` will be created automatically the first time you use the loader.

The first time you use GoogleDriveLoader, you will be displayed with the consent screen in your browser. If this doesn't happen and you get a `RefreshError`, do not use `credentials_path` in your `GoogleDriveLoader` constructor call. Instead, put that path in a `GOOGLE_APPLICATION_CREDENTIALS` environmental variable.

`GoogleDriveLoader` can load from a list of Google Docs document ids or a folder id. You can obtain your folder and document id from the URL:

- Folder: <https://drive.google.com/drive/u/0/folders/1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5> -> folder id is `"1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5"`
- Document: <https://docs.google.com/document/d/1bfaMQ18_i56204VaQDVeAFpqEijJTgvurupdEDiaUQw/edit> -> document id is `"1bfaMQ18_i56204VaQDVeAFpqEijJTgvurupdEDiaUQw"`

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib  

```

```python
from langchain.document\_loaders import GoogleDriveLoader  

```

```python
loader = GoogleDriveLoader(  
 folder\_id="1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5",  
 token\_path='/path/where/you/want/token/to/be/created/google\_token.json'  
 # Optional: configure whether to recursively fetch files from subfolders. Defaults to False.  
 recursive=False,  
)  

```

```python
docs = loader.load()  

```

When you pass a `folder_id` by default all files of type document, sheet and pdf are loaded. You can modify this behaviour by passing a `file_types` argument

```python
loader = GoogleDriveLoader(  
 folder\_id="1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5",  
 file\_types=["document", "sheet"],  
 recursive=False  
)  

```

## Passing in Optional File Loaders[​](#passing-in-optional-file-loaders "Direct link to Passing in Optional File Loaders")

When processing files other than Google Docs and Google Sheets, it can be helpful to pass an optional file loader to `GoogleDriveLoader`. If you pass in a file loader, that file loader will be used on documents that do not have a Google Docs or Google Sheets MIME type. Here is an example of how to load an Excel document from Google Drive using a file loader.

```python
from langchain.document\_loaders import GoogleDriveLoader  
from langchain.document\_loaders import UnstructuredFileIOLoader  

```

```python
file\_id = "1x9WBtFPWMEAdjcJzPScRsjpjQvpSo\_kz"  
loader = GoogleDriveLoader(  
 file\_ids=[file\_id],  
 file\_loader\_cls=UnstructuredFileIOLoader,  
 file\_loader\_kwargs={"mode": "elements"},  
)  

```

```python
docs = loader.load()  

```

```python
docs[0]  

```

You can also process a folder with a mix of files and Google Docs/Sheets using the following pattern:

```python
folder\_id = "1asMOHY1BqBS84JcRbOag5LOJac74gpmD"  
loader = GoogleDriveLoader(  
 folder\_id=folder\_id,  
 file\_loader\_cls=UnstructuredFileIOLoader,  
 file\_loader\_kwargs={"mode": "elements"},  
)  

```

```python
docs = loader.load()  

```

```python
docs[0]  

```

## Extended usage[​](#extended-usage "Direct link to Extended usage")

An external component can manage the complexity of Google Drive : `langchain-googledrive`
It's compatible with the ̀`langchain.document_loaders.GoogleDriveLoader` and can be used
in its place.

To be compatible with containers, the authentication uses an environment variable ̀GOOGLE_ACCOUNT_FILE\` to credential file (for user or service).

```bash
pip install langchain-googledrive  

```

```python
folder\_id='root'  
#folder\_id='1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5'  

```

```python
# Use the advanced version.  
from langchain\_googledrive.document\_loaders import GoogleDriveLoader  

```

```python
loader = GoogleDriveLoader(  
 folder\_id=folder\_id,  
 recursive=False,  
 num\_results=2, # Maximum number of file to load  
)  

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

It's possible to update or customize this. See the documentation of `GDriveLoader`.

But, the corresponding packages must be installed.

```bash
pip install unstructured  

```

```python
for doc in loader.load():  
 print("---")  
 print(doc.page\_content.strip()[:60]+"...")  

```

### Customize the search pattern[​](#customize-the-search-pattern "Direct link to Customize the search pattern")

All parameter compatible with Google [`list()`](https://developers.google.com/drive/api/v3/reference/files/list)
API can be set.

To specify the new pattern of the Google request, you can use a `PromptTemplate()`.
The variables for the prompt can be set with `kwargs` in the constructor.
Some pre-formated request are proposed (use `{query}`, `{folder_id}` and/or `{mime_type}`):

You can customize the criteria to select the files. A set of predefined filter are proposed:
| template | description |
| -------------------------------------- | --------------------------------------------------------------------- |
| gdrive-all-in-folder | Return all compatible files from a `folder_id` |
| gdrive-query | Search `query` in all drives |
| gdrive-by-name | Search file with name `query` |
| gdrive-query-in-folder | Search `query` in `folder_id` (and sub-folders if `recursive=true`) |
| gdrive-mime-type | Search a specific `mime_type` |
| gdrive-mime-type-in-folder | Search a specific `mime_type` in `folder_id` |
| gdrive-query-with-mime-type | Search `query` with a specific `mime_type` |
| gdrive-query-with-mime-type-and-folder | Search `query` with a specific `mime_type` and in `folder_id` |

```python
loader = GoogleDriveLoader(  
 folder\_id=folder\_id,  
 recursive=False,  
 template="gdrive-query", # Default template to use  
 query="machine learning",  
 num\_results=2, # Maximum number of file to load  
 supportsAllDrives=False, # GDrive `list()` parameter  
)  
for doc in loader.load():  
 print("---")  
 print(doc.page\_content.strip()[:60]+"...")  

```

You can customize your pattern.

```python
from langchain.prompts.prompt import PromptTemplate  
loader = GoogleDriveLoader(  
 folder\_id=folder\_id,  
 recursive=False,  
 template=PromptTemplate(  
 input\_variables=["query", "query\_name"],  
 template="fullText contains '{query}' and name contains '{query\_name}' and trashed=false",  
 ), # Default template to use  
 query="machine learning",  
 query\_name="ML",   
 num\_results=2, # Maximum number of file to load  
)  
for doc in loader.load():  
 print("---")  
 print(doc.page\_content.strip()[:60]+"...")  

```

#### Modes for GSlide and GSheet[​](#modes-for-gslide-and-gsheet "Direct link to Modes for GSlide and GSheet")

The parameter mode accepts different values:

- "document": return the body of each document
- "snippets": return the description of each file (set in metadata of Google Drive files).

The conversion can manage in Markdown format:

- bullet
- link
- table
- titles

The parameter `gslide_mode` accepts different values:

- "single" : one document with <PAGE BREAK>
- "slide" : one document by slide
- "elements" : one document for each elements.

```python
loader = GoogleDriveLoader(  
 template="gdrive-mime-type",  
 mime\_type="application/vnd.google-apps.presentation", # Only GSlide files  
 gslide\_mode="slide",  
 num\_results=2, # Maximum number of file to load  
)  
for doc in loader.load():  
 print("---")  
 print(doc.page\_content.strip()[:60]+"...")  

```

The parameter `gsheet_mode` accepts different values:

- `"single"`: Generate one document by line
- `"elements"` : one document with markdown array and <PAGE BREAK> tags.

```python
loader = GoogleDriveLoader(  
 template="gdrive-mime-type",  
 mime\_type="application/vnd.google-apps.spreadsheet", # Only GSheet files  
 gsheet\_mode="elements",  
 num\_results=2, # Maximum number of file to load  
)  
for doc in loader.load():  
 print("---")  
 print(doc.page\_content.strip()[:60]+"...")  

```

### Advanced usage[​](#advanced-usage "Direct link to Advanced usage")

All Google File have a 'description' in the metadata. This field can be used to memorize a summary of the document or others indexed tags (See method `lazy_update_description_with_summary()`).

If you use the `mode="snippet"`, only the description will be used for the body. Else, the `metadata['summary']` has the field.

Sometime, a specific filter can be used to extract some information from the filename, to select some files with specific criteria. You can use a filter.

Sometimes, many documents are returned. It's not necessary to have all documents in memory at the same time. You can use the lazy versions of methods, to get one document at a time. It's better to use a complex query in place of a recursive search. For each folder, a query must be applied if you activate `recursive=True`.

```python
import os  
loader = GoogleDriveLoader(  
 gdrive\_api\_file=os.environ["GOOGLE\_ACCOUNT\_FILE"],  
 num\_results=2,  
 template="gdrive-query",  
 filter=lambda search, file: "#test" not in file.get('description',''),  
 query='machine learning',  
 supportsAllDrives=False,  
 )  
for doc in loader.load():  
 print("---")  
 print(doc.page\_content.strip()[:60]+"...")  

```

- [Prerequisites](#prerequisites)

- [🧑 Instructions for ingesting your Google Docs data](#-instructions-for-ingesting-your-google-docs-data)

- [Passing in Optional File Loaders](#passing-in-optional-file-loaders)

- [Extended usage](#extended-usage)

  - [Customize the search pattern](#customize-the-search-pattern)
  - [Advanced usage](#advanced-usage)

- [Customize the search pattern](#customize-the-search-pattern)

- [Advanced usage](#advanced-usage)

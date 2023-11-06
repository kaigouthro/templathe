# EverNote

[EverNote](https://evernote.com/) is intended for archiving and creating notes in which photos, audio and saved web content can be embedded. Notes are stored in virtual "notebooks" and can be tagged, annotated, edited, searched, and exported.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

First, you need to install `lxml` and `html2text` python packages.

```bash
pip install lxml  
pip install html2text  

```

## Document Loader[​](#document-loader "Direct link to Document Loader")

See a [usage example](/docs/integrations/document_loaders/evernote).

```python
from langchain.document\_loaders import EverNoteLoader  

```

- [Installation and Setup](#installation-and-setup)
- [Document Loader](#document-loader)

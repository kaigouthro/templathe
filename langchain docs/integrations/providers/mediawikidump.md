# MediaWikiDump

[MediaWiki XML Dumps](https://www.mediawiki.org/wiki/Manual:Importing_XML_dumps) contain the content of a wiki
(wiki pages with all their revisions), without the site-related data. A XML dump does not create a full backup
of the wiki database, the dump does not contain user accounts, images, edit logs, etc.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

We need to install several python packages.

The `mediawiki-utilities` supports XML schema 0.11 in unmerged branches.

```bash
pip install -qU git+https://github.com/mediawiki-utilities/python-mwtypes@updates\_schema\_0.11  

```

The `mediawiki-utilities mwxml` has a bug, fix PR pending.

```bash
pip install -qU git+https://github.com/gdedrouas/python-mwxml@xml\_format\_0.11  
pip install -qU mwparserfromhell  

```

## Document Loader[​](#document-loader "Direct link to Document Loader")

See a [usage example](/docs/integrations/document_loaders/mediawikidump).

```python
from langchain.document\_loaders import MWDumpLoader  

```

- [Installation and Setup](#installation-and-setup)
- [Document Loader](#document-loader)

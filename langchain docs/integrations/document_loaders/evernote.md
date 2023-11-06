# EverNote

[EverNote](https://evernote.com/) is intended for archiving and creating notes in which photos, audio and saved web content can be embedded. Notes are stored in virtual "notebooks" and can be tagged, annotated, edited, searched, and exported.

This notebook shows how to load an `Evernote` [export](https://help.evernote.com/hc/en-us/articles/209005557-Export-notes-and-notebooks-as-ENEX-or-HTML) file (.enex) from disk.

A document will be created for each note in the export.

```python
# lxml and html2text are required to parse EverNote notes  
# !pip install lxml  
# !pip install html2text  

```

```python
from langchain.document\_loaders import EverNoteLoader  
  
# By default all notes are combined into a single Document  
loader = EverNoteLoader("example\_data/testing.enex")  
loader.load()  

```

```text
 [Document(page\_content='testing this\n\nwhat happens?\n\nto the world?\*\*Jan - March 2022\*\*', metadata={'source': 'example\_data/testing.enex'})]  

```

```python
# It's likely more useful to return a Document for each note  
loader = EverNoteLoader("example\_data/testing.enex", load\_single\_document=False)  
loader.load()  

```

```text
 [Document(page\_content='testing this\n\nwhat happens?\n\nto the world?', metadata={'title': 'testing', 'created': time.struct\_time(tm\_year=2023, tm\_mon=2, tm\_mday=9, tm\_hour=3, tm\_min=47, tm\_sec=46, tm\_wday=3, tm\_yday=40, tm\_isdst=-1), 'updated': time.struct\_time(tm\_year=2023, tm\_mon=2, tm\_mday=9, tm\_hour=3, tm\_min=53, tm\_sec=28, tm\_wday=3, tm\_yday=40, tm\_isdst=-1), 'note-attributes.author': 'Harrison Chase', 'source': 'example\_data/testing.enex'}),  
 Document(page\_content='\*\*Jan - March 2022\*\*', metadata={'title': 'Summer Training Program', 'created': time.struct\_time(tm\_year=2022, tm\_mon=12, tm\_mday=27, tm\_hour=1, tm\_min=59, tm\_sec=48, tm\_wday=1, tm\_yday=361, tm\_isdst=-1), 'note-attributes.author': 'Mike McGarry', 'note-attributes.source': 'mobile.iphone', 'source': 'example\_data/testing.enex'})]  

```

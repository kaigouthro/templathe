# Airtable

```bash
pip install pyairtable  

```

```python
from langchain.document\_loaders import AirtableLoader  

```

- Get your API key [here](https://support.airtable.com/docs/creating-and-using-api-keys-and-access-tokens).
- Get ID of your base [here](https://airtable.com/developers/web/api/introduction).
- Get your table ID from the table url as shown [here](https://www.highviewapps.com/kb/where-can-i-find-the-airtable-base-id-and-table-id/#:~:text=Both%20the%20Airtable%20Base%20ID,URL%20that%20begins%20with%20tbl).

```python
api\_key = "xxx"  
base\_id = "xxx"  
table\_id = "xxx"  

```

```python
loader = AirtableLoader(api\_key, table\_id, base\_id)  
docs = loader.load()  

```

Returns each table row as `dict`.

```python
len(docs)  

```

```text
 3  

```

```python
eval(docs[0].page\_content)  

```

```text
 {'id': 'recF3GbGZCuh9sXIQ',  
 'createdTime': '2023-06-09T04:47:21.000Z',  
 'fields': {'Priority': 'High',  
 'Status': 'In progress',  
 'Name': 'Document Splitters'}}  

```

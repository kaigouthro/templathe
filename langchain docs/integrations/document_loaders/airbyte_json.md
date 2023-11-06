# Airbyte JSON

[Airbyte](https://github.com/airbytehq/airbyte) is a data integration platform for ELT pipelines from APIs, databases & files to warehouses & lakes. It has the largest catalog of ELT connectors to data warehouses and databases.

This covers how to load any source from Airbyte into a local JSON file that can be read in as a document

Prereqs:
Have docker desktop installed

Steps:

1. Clone Airbyte from GitHub - `git clone https://github.com/airbytehq/airbyte.git`

1. Switch into Airbyte directory - `cd airbyte`

1. Start Airbyte - `docker compose up`

1. In your browser, just visit http://localhost:8000. You will be asked for a username and password. By default, that's username `airbyte` and password `password`.

1. Setup any source you wish.

1. Set destination as Local JSON, with specified destination path - lets say `/json_data`. Set up manual sync.

1. Run the connection.

1. To see what files are create, you can navigate to: `file:///tmp/airbyte_local`

1. Find your data and copy path. That path should be saved in the file variable below. It should start with `/tmp/airbyte_local`

```python
from langchain.document\_loaders import AirbyteJSONLoader  

```

```bash
ls /tmp/airbyte\_local/json\_data/  

```

```text
 \_airbyte\_raw\_pokemon.jsonl  

```

```python
loader = AirbyteJSONLoader("/tmp/airbyte\_local/json\_data/\_airbyte\_raw\_pokemon.jsonl")  

```

```python
data = loader.load()  

```

```python
print(data[0].page\_content[:500])  

```

```text
 abilities:   
 ability:   
 name: blaze  
 url: https://pokeapi.co/api/v2/ability/66/  
   
 is\_hidden: False  
 slot: 1  
   
   
 ability:   
 name: solar-power  
 url: https://pokeapi.co/api/v2/ability/94/  
   
 is\_hidden: True  
 slot: 3  
   
 base\_experience: 267  
 forms:   
 name: charizard  
 url: https://pokeapi.co/api/v2/pokemon-form/6/  
   
 game\_indices:   
 game\_index: 180  
 version:   
 name: red  
 url: https://pokeapi.co/api/v2/version/1/  
   
   
   
 game\_index: 180  
 version:   
 name: blue  
 url: https://pokeapi.co/api/v2/version/2/  
   
   
   
 game\_index: 180  
 version:   
 n  

```

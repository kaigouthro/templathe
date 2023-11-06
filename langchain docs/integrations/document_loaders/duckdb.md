# DuckDB

[DuckDB](https://duckdb.org/) is an in-process SQL OLAP database management system.

Load a `DuckDB` query with one document per row.

```python
#!pip install duckdb  

```

```python
from langchain.document\_loaders import DuckDBLoader  

```

```python
Team,Payroll  
Nationals,81.34  
Reds,82.20  

```

```text
 Writing example.csv  

```

```python
loader = DuckDBLoader("SELECT \* FROM read\_csv\_auto('example.csv')")  
  
data = loader.load()  

```

```python
print(data)  

```

```text
 [Document(page\_content='Team: Nationals\nPayroll: 81.34', metadata={}), Document(page\_content='Team: Reds\nPayroll: 82.2', metadata={})]  

```

## Specifying Which Columns are Content vs Metadata[​](#specifying-which-columns-are-content-vs-metadata "Direct link to Specifying Which Columns are Content vs Metadata")

```python
loader = DuckDBLoader(  
 "SELECT \* FROM read\_csv\_auto('example.csv')",  
 page\_content\_columns=["Team"],  
 metadata\_columns=["Payroll"],  
)  
  
data = loader.load()  

```

```python
print(data)  

```

```text
 [Document(page\_content='Team: Nationals', metadata={'Payroll': 81.34}), Document(page\_content='Team: Reds', metadata={'Payroll': 82.2})]  

```

## Adding Source to Metadata[​](#adding-source-to-metadata "Direct link to Adding Source to Metadata")

```python
loader = DuckDBLoader(  
 "SELECT Team, Payroll, Team As source FROM read\_csv\_auto('example.csv')",  
 metadata\_columns=["source"],  
)  
  
data = loader.load()  

```

```python
print(data)  

```

```text
 [Document(page\_content='Team: Nationals\nPayroll: 81.34\nsource: Nationals', metadata={'source': 'Nationals'}), Document(page\_content='Team: Reds\nPayroll: 82.2\nsource: Reds', metadata={'source': 'Reds'})]  

```

- [Specifying Which Columns are Content vs Metadata](#specifying-which-columns-are-content-vs-metadata)
- [Adding Source to Metadata](#adding-source-to-metadata)

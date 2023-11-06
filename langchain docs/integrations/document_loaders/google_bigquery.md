# Google BigQuery

[Google BigQuery](https://cloud.google.com/bigquery) is a serverless and cost-effective enterprise data warehouse that works across clouds and scales with your data.
`BigQuery` is a part of the `Google Cloud Platform`.

Load a `BigQuery` query with one document per row.

```python
#!pip install google-cloud-bigquery  

```

```python
from langchain.document\_loaders import BigQueryLoader  

```

```python
BASE\_QUERY = """  
SELECT  
 id,  
 dna\_sequence,  
 organism  
FROM (  
 SELECT  
 ARRAY (  
 SELECT  
 AS STRUCT 1 AS id, "ATTCGA" AS dna\_sequence, "Lokiarchaeum sp. (strain GC14\_75)." AS organism  
 UNION ALL  
 SELECT  
 AS STRUCT 2 AS id, "AGGCGA" AS dna\_sequence, "Heimdallarchaeota archaeon (strain LC\_2)." AS organism  
 UNION ALL  
 SELECT  
 AS STRUCT 3 AS id, "TCCGGA" AS dna\_sequence, "Acidianus hospitalis (strain W1)." AS organism) AS new\_array),  
 UNNEST(new\_array)  
"""  

```

## Basic Usage[​](#basic-usage "Direct link to Basic Usage")

```python
loader = BigQueryLoader(BASE\_QUERY)  
  
data = loader.load()  

```

```python
print(data)  

```

```text
 [Document(page\_content='id: 1\ndna\_sequence: ATTCGA\norganism: Lokiarchaeum sp. (strain GC14\_75).', lookup\_str='', metadata={}, lookup\_index=0), Document(page\_content='id: 2\ndna\_sequence: AGGCGA\norganism: Heimdallarchaeota archaeon (strain LC\_2).', lookup\_str='', metadata={}, lookup\_index=0), Document(page\_content='id: 3\ndna\_sequence: TCCGGA\norganism: Acidianus hospitalis (strain W1).', lookup\_str='', metadata={}, lookup\_index=0)]  

```

## Specifying Which Columns are Content vs Metadata[​](#specifying-which-columns-are-content-vs-metadata "Direct link to Specifying Which Columns are Content vs Metadata")

```python
loader = BigQueryLoader(  
 BASE\_QUERY,  
 page\_content\_columns=["dna\_sequence", "organism"],  
 metadata\_columns=["id"],  
)  
  
data = loader.load()  

```

```python
print(data)  

```

```text
 [Document(page\_content='dna\_sequence: ATTCGA\norganism: Lokiarchaeum sp. (strain GC14\_75).', lookup\_str='', metadata={'id': 1}, lookup\_index=0), Document(page\_content='dna\_sequence: AGGCGA\norganism: Heimdallarchaeota archaeon (strain LC\_2).', lookup\_str='', metadata={'id': 2}, lookup\_index=0), Document(page\_content='dna\_sequence: TCCGGA\norganism: Acidianus hospitalis (strain W1).', lookup\_str='', metadata={'id': 3}, lookup\_index=0)]  

```

## Adding Source to Metadata[​](#adding-source-to-metadata "Direct link to Adding Source to Metadata")

```python
# Note that the `id` column is being returned twice, with one instance aliased as `source`  
ALIASED\_QUERY = """  
SELECT  
 id,  
 dna\_sequence,  
 organism,  
 id as source  
FROM (  
 SELECT  
 ARRAY (  
 SELECT  
 AS STRUCT 1 AS id, "ATTCGA" AS dna\_sequence, "Lokiarchaeum sp. (strain GC14\_75)." AS organism  
 UNION ALL  
 SELECT  
 AS STRUCT 2 AS id, "AGGCGA" AS dna\_sequence, "Heimdallarchaeota archaeon (strain LC\_2)." AS organism  
 UNION ALL  
 SELECT  
 AS STRUCT 3 AS id, "TCCGGA" AS dna\_sequence, "Acidianus hospitalis (strain W1)." AS organism) AS new\_array),  
 UNNEST(new\_array)  
"""  

```

```python
loader = BigQueryLoader(ALIASED\_QUERY, metadata\_columns=["source"])  
  
data = loader.load()  

```

```python
print(data)  

```

```text
 [Document(page\_content='id: 1\ndna\_sequence: ATTCGA\norganism: Lokiarchaeum sp. (strain GC14\_75).\nsource: 1', lookup\_str='', metadata={'source': 1}, lookup\_index=0), Document(page\_content='id: 2\ndna\_sequence: AGGCGA\norganism: Heimdallarchaeota archaeon (strain LC\_2).\nsource: 2', lookup\_str='', metadata={'source': 2}, lookup\_index=0), Document(page\_content='id: 3\ndna\_sequence: TCCGGA\norganism: Acidianus hospitalis (strain W1).\nsource: 3', lookup\_str='', metadata={'source': 3}, lookup\_index=0)]  

```

- [Basic Usage](#basic-usage)
- [Specifying Which Columns are Content vs Metadata](#specifying-which-columns-are-content-vs-metadata)
- [Adding Source to Metadata](#adding-source-to-metadata)

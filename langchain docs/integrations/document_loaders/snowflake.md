# Snowflake

This notebooks goes over how to load documents from Snowflake

```bash
pip install snowflake-connector-python  

```

```python
import settings as s  
from langchain.document\_loaders import SnowflakeLoader  

```

```python
QUERY = "select text, survey\_id from CLOUD\_DATA\_SOLUTIONS.HAPPY\_OR\_NOT.OPEN\_FEEDBACK limit 10"  
snowflake\_loader = SnowflakeLoader(  
 query=QUERY,  
 user=s.SNOWFLAKE\_USER,  
 password=s.SNOWFLAKE\_PASS,  
 account=s.SNOWFLAKE\_ACCOUNT,  
 warehouse=s.SNOWFLAKE\_WAREHOUSE,  
 role=s.SNOWFLAKE\_ROLE,  
 database=s.SNOWFLAKE\_DATABASE,  
 schema=s.SNOWFLAKE\_SCHEMA,  
)  
snowflake\_documents = snowflake\_loader.load()  
print(snowflake\_documents)  

```

```python
from snowflakeLoader import SnowflakeLoader  
import settings as s  
  
QUERY = "select text, survey\_id as source from CLOUD\_DATA\_SOLUTIONS.HAPPY\_OR\_NOT.OPEN\_FEEDBACK limit 10"  
snowflake\_loader = SnowflakeLoader(  
 query=QUERY,  
 user=s.SNOWFLAKE\_USER,  
 password=s.SNOWFLAKE\_PASS,  
 account=s.SNOWFLAKE\_ACCOUNT,  
 warehouse=s.SNOWFLAKE\_WAREHOUSE,  
 role=s.SNOWFLAKE\_ROLE,  
 database=s.SNOWFLAKE\_DATABASE,  
 schema=s.SNOWFLAKE\_SCHEMA,  
 metadata\_columns=["source"],  
)  
snowflake\_documents = snowflake\_loader.load()  
print(snowflake\_documents)  

```

# PySpark

This notebook goes over how to load data from a [PySpark](https://spark.apache.org/docs/latest/api/python/) DataFrame.

```python
#!pip install pyspark  

```

```python
from pyspark.sql import SparkSession  

```

```python
spark = SparkSession.builder.getOrCreate()  

```

```text
 Setting default log level to "WARN".  
 To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).  
 23/05/31 14:08:33 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable  

```

```python
df = spark.read.csv("example\_data/mlb\_teams\_2012.csv", header=True)  

```

```python
from langchain.document\_loaders import PySparkDataFrameLoader  

```

```python
loader = PySparkDataFrameLoader(spark, df, page\_content\_column="Team")  

```

```python
loader.load()  

```

```text
 [Stage 8:> (0 + 1) / 1]  
  
  
  
  
 [Document(page\_content='Nationals', metadata={' "Payroll (millions)"': ' 81.34', ' "Wins"': ' 98'}),  
 Document(page\_content='Reds', metadata={' "Payroll (millions)"': ' 82.20', ' "Wins"': ' 97'}),  
 Document(page\_content='Yankees', metadata={' "Payroll (millions)"': ' 197.96', ' "Wins"': ' 95'}),  
 Document(page\_content='Giants', metadata={' "Payroll (millions)"': ' 117.62', ' "Wins"': ' 94'}),  
 Document(page\_content='Braves', metadata={' "Payroll (millions)"': ' 83.31', ' "Wins"': ' 94'}),  
 Document(page\_content='Athletics', metadata={' "Payroll (millions)"': ' 55.37', ' "Wins"': ' 94'}),  
 Document(page\_content='Rangers', metadata={' "Payroll (millions)"': ' 120.51', ' "Wins"': ' 93'}),  
 Document(page\_content='Orioles', metadata={' "Payroll (millions)"': ' 81.43', ' "Wins"': ' 93'}),  
 Document(page\_content='Rays', metadata={' "Payroll (millions)"': ' 64.17', ' "Wins"': ' 90'}),  
 Document(page\_content='Angels', metadata={' "Payroll (millions)"': ' 154.49', ' "Wins"': ' 89'}),  
 Document(page\_content='Tigers', metadata={' "Payroll (millions)"': ' 132.30', ' "Wins"': ' 88'}),  
 Document(page\_content='Cardinals', metadata={' "Payroll (millions)"': ' 110.30', ' "Wins"': ' 88'}),  
 Document(page\_content='Dodgers', metadata={' "Payroll (millions)"': ' 95.14', ' "Wins"': ' 86'}),  
 Document(page\_content='White Sox', metadata={' "Payroll (millions)"': ' 96.92', ' "Wins"': ' 85'}),  
 Document(page\_content='Brewers', metadata={' "Payroll (millions)"': ' 97.65', ' "Wins"': ' 83'}),  
 Document(page\_content='Phillies', metadata={' "Payroll (millions)"': ' 174.54', ' "Wins"': ' 81'}),  
 Document(page\_content='Diamondbacks', metadata={' "Payroll (millions)"': ' 74.28', ' "Wins"': ' 81'}),  
 Document(page\_content='Pirates', metadata={' "Payroll (millions)"': ' 63.43', ' "Wins"': ' 79'}),  
 Document(page\_content='Padres', metadata={' "Payroll (millions)"': ' 55.24', ' "Wins"': ' 76'}),  
 Document(page\_content='Mariners', metadata={' "Payroll (millions)"': ' 81.97', ' "Wins"': ' 75'}),  
 Document(page\_content='Mets', metadata={' "Payroll (millions)"': ' 93.35', ' "Wins"': ' 74'}),  
 Document(page\_content='Blue Jays', metadata={' "Payroll (millions)"': ' 75.48', ' "Wins"': ' 73'}),  
 Document(page\_content='Royals', metadata={' "Payroll (millions)"': ' 60.91', ' "Wins"': ' 72'}),  
 Document(page\_content='Marlins', metadata={' "Payroll (millions)"': ' 118.07', ' "Wins"': ' 69'}),  
 Document(page\_content='Red Sox', metadata={' "Payroll (millions)"': ' 173.18', ' "Wins"': ' 69'}),  
 Document(page\_content='Indians', metadata={' "Payroll (millions)"': ' 78.43', ' "Wins"': ' 68'}),  
 Document(page\_content='Twins', metadata={' "Payroll (millions)"': ' 94.08', ' "Wins"': ' 66'}),  
 Document(page\_content='Rockies', metadata={' "Payroll (millions)"': ' 78.06', ' "Wins"': ' 64'}),  
 Document(page\_content='Cubs', metadata={' "Payroll (millions)"': ' 88.19', ' "Wins"': ' 61'}),  
 Document(page\_content='Astros', metadata={' "Payroll (millions)"': ' 60.65', ' "Wins"': ' 55'})]  

```

# Polars DataFrame

This notebook goes over how to load data from a [polars](https://pola-rs.github.io/polars-book/user-guide/) DataFrame.

```python
#!pip install polars  

```

```python
import polars as pl  

```

```python
df = pl.read\_csv("example\_data/mlb\_teams\_2012.csv")  

```

```python
df.head()  

```

```html
<div><style>  
.dataframe > thead > tr > th,  
.dataframe > tbody > tr > td {  
 text-align: right;  
}  
</style>  
<small>shape: (5, 3)</small><table border="1" class="dataframe"><thead><tr><th>Team</th><th> &quot;Payroll (millions)&quot;</th><th> &quot;Wins&quot;</th></tr><tr><td>str</td><td>f64</td><td>i64</td></tr></thead><tbody><tr><td>&quot;Nationals&quot;</td><td>81.34</td><td>98</td></tr><tr><td>&quot;Reds&quot;</td><td>82.2</td><td>97</td></tr><tr><td>&quot;Yankees&quot;</td><td>197.96</td><td>95</td></tr><tr><td>&quot;Giants&quot;</td><td>117.62</td><td>94</td></tr><tr><td>&quot;Braves&quot;</td><td>83.31</td><td>94</td></tr></tbody></table></div>  

```

```python
from langchain.document\_loaders import PolarsDataFrameLoader  

```

```python
loader = PolarsDataFrameLoader(df, page\_content\_column="Team")  

```

```python
loader.load()  

```

```text
 [Document(page\_content='Nationals', metadata={' "Payroll (millions)"': 81.34, ' "Wins"': 98}),  
 Document(page\_content='Reds', metadata={' "Payroll (millions)"': 82.2, ' "Wins"': 97}),  
 Document(page\_content='Yankees', metadata={' "Payroll (millions)"': 197.96, ' "Wins"': 95}),  
 Document(page\_content='Giants', metadata={' "Payroll (millions)"': 117.62, ' "Wins"': 94}),  
 Document(page\_content='Braves', metadata={' "Payroll (millions)"': 83.31, ' "Wins"': 94}),  
 Document(page\_content='Athletics', metadata={' "Payroll (millions)"': 55.37, ' "Wins"': 94}),  
 Document(page\_content='Rangers', metadata={' "Payroll (millions)"': 120.51, ' "Wins"': 93}),  
 Document(page\_content='Orioles', metadata={' "Payroll (millions)"': 81.43, ' "Wins"': 93}),  
 Document(page\_content='Rays', metadata={' "Payroll (millions)"': 64.17, ' "Wins"': 90}),  
 Document(page\_content='Angels', metadata={' "Payroll (millions)"': 154.49, ' "Wins"': 89}),  
 Document(page\_content='Tigers', metadata={' "Payroll (millions)"': 132.3, ' "Wins"': 88}),  
 Document(page\_content='Cardinals', metadata={' "Payroll (millions)"': 110.3, ' "Wins"': 88}),  
 Document(page\_content='Dodgers', metadata={' "Payroll (millions)"': 95.14, ' "Wins"': 86}),  
 Document(page\_content='White Sox', metadata={' "Payroll (millions)"': 96.92, ' "Wins"': 85}),  
 Document(page\_content='Brewers', metadata={' "Payroll (millions)"': 97.65, ' "Wins"': 83}),  
 Document(page\_content='Phillies', metadata={' "Payroll (millions)"': 174.54, ' "Wins"': 81}),  
 Document(page\_content='Diamondbacks', metadata={' "Payroll (millions)"': 74.28, ' "Wins"': 81}),  
 Document(page\_content='Pirates', metadata={' "Payroll (millions)"': 63.43, ' "Wins"': 79}),  
 Document(page\_content='Padres', metadata={' "Payroll (millions)"': 55.24, ' "Wins"': 76}),  
 Document(page\_content='Mariners', metadata={' "Payroll (millions)"': 81.97, ' "Wins"': 75}),  
 Document(page\_content='Mets', metadata={' "Payroll (millions)"': 93.35, ' "Wins"': 74}),  
 Document(page\_content='Blue Jays', metadata={' "Payroll (millions)"': 75.48, ' "Wins"': 73}),  
 Document(page\_content='Royals', metadata={' "Payroll (millions)"': 60.91, ' "Wins"': 72}),  
 Document(page\_content='Marlins', metadata={' "Payroll (millions)"': 118.07, ' "Wins"': 69}),  
 Document(page\_content='Red Sox', metadata={' "Payroll (millions)"': 173.18, ' "Wins"': 69}),  
 Document(page\_content='Indians', metadata={' "Payroll (millions)"': 78.43, ' "Wins"': 68}),  
 Document(page\_content='Twins', metadata={' "Payroll (millions)"': 94.08, ' "Wins"': 66}),  
 Document(page\_content='Rockies', metadata={' "Payroll (millions)"': 78.06, ' "Wins"': 64}),  
 Document(page\_content='Cubs', metadata={' "Payroll (millions)"': 88.19, ' "Wins"': 61}),  
 Document(page\_content='Astros', metadata={' "Payroll (millions)"': 60.65, ' "Wins"': 55})]  

```

```python
# Use lazy load for larger table, which won't read the full table into memory  
for i in loader.lazy\_load():  
 print(i)  

```

```text
 page\_content='Nationals' metadata={' "Payroll (millions)"': 81.34, ' "Wins"': 98}  
 page\_content='Reds' metadata={' "Payroll (millions)"': 82.2, ' "Wins"': 97}  
 page\_content='Yankees' metadata={' "Payroll (millions)"': 197.96, ' "Wins"': 95}  
 page\_content='Giants' metadata={' "Payroll (millions)"': 117.62, ' "Wins"': 94}  
 page\_content='Braves' metadata={' "Payroll (millions)"': 83.31, ' "Wins"': 94}  
 page\_content='Athletics' metadata={' "Payroll (millions)"': 55.37, ' "Wins"': 94}  
 page\_content='Rangers' metadata={' "Payroll (millions)"': 120.51, ' "Wins"': 93}  
 page\_content='Orioles' metadata={' "Payroll (millions)"': 81.43, ' "Wins"': 93}  
 page\_content='Rays' metadata={' "Payroll (millions)"': 64.17, ' "Wins"': 90}  
 page\_content='Angels' metadata={' "Payroll (millions)"': 154.49, ' "Wins"': 89}  
 page\_content='Tigers' metadata={' "Payroll (millions)"': 132.3, ' "Wins"': 88}  
 page\_content='Cardinals' metadata={' "Payroll (millions)"': 110.3, ' "Wins"': 88}  
 page\_content='Dodgers' metadata={' "Payroll (millions)"': 95.14, ' "Wins"': 86}  
 page\_content='White Sox' metadata={' "Payroll (millions)"': 96.92, ' "Wins"': 85}  
 page\_content='Brewers' metadata={' "Payroll (millions)"': 97.65, ' "Wins"': 83}  
 page\_content='Phillies' metadata={' "Payroll (millions)"': 174.54, ' "Wins"': 81}  
 page\_content='Diamondbacks' metadata={' "Payroll (millions)"': 74.28, ' "Wins"': 81}  
 page\_content='Pirates' metadata={' "Payroll (millions)"': 63.43, ' "Wins"': 79}  
 page\_content='Padres' metadata={' "Payroll (millions)"': 55.24, ' "Wins"': 76}  
 page\_content='Mariners' metadata={' "Payroll (millions)"': 81.97, ' "Wins"': 75}  
 page\_content='Mets' metadata={' "Payroll (millions)"': 93.35, ' "Wins"': 74}  
 page\_content='Blue Jays' metadata={' "Payroll (millions)"': 75.48, ' "Wins"': 73}  
 page\_content='Royals' metadata={' "Payroll (millions)"': 60.91, ' "Wins"': 72}  
 page\_content='Marlins' metadata={' "Payroll (millions)"': 118.07, ' "Wins"': 69}  
 page\_content='Red Sox' metadata={' "Payroll (millions)"': 173.18, ' "Wins"': 69}  
 page\_content='Indians' metadata={' "Payroll (millions)"': 78.43, ' "Wins"': 68}  
 page\_content='Twins' metadata={' "Payroll (millions)"': 94.08, ' "Wins"': 66}  
 page\_content='Rockies' metadata={' "Payroll (millions)"': 78.06, ' "Wins"': 64}  
 page\_content='Cubs' metadata={' "Payroll (millions)"': 88.19, ' "Wins"': 61}  
 page\_content='Astros' metadata={' "Payroll (millions)"': 60.65, ' "Wins"': 55}  

```

# Alpha Vantage

[Alpha Vantage](https://www.alphavantage.co) Alpha Vantage provides realtime and historical financial market data through a set of powerful and developer-friendly data APIs and spreadsheets.

Use the `AlphaVantageAPIWrapper` to get currency exchange rates.

```python
import getpass  
import os  
  
os.environ["ALPHAVANTAGE\_API\_KEY"] = getpass.getpass()  

```

```text
 ········  

```

```python
from langchain.utilities.alpha\_vantage import AlphaVantageAPIWrapper  

```

```python
alpha\_vantage = AlphaVantageAPIWrapper()  

```

```python
alpha\_vantage.run("USD", "JPY")  

```

```text
 {'1. From\_Currency Code': 'USD',  
 '2. From\_Currency Name': 'United States Dollar',  
 '3. To\_Currency Code': 'JPY',  
 '4. To\_Currency Name': 'Japanese Yen',  
 '5. Exchange Rate': '144.93000000',  
 '6. Last Refreshed': '2023-08-11 21:31:01',  
 '7. Time Zone': 'UTC',  
 '8. Bid Price': '144.92600000',  
 '9. Ask Price': '144.93400000'}  

```

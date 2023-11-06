# Custom functions with OpenAI Functions Agent

This notebook goes through how to integrate custom functions with OpenAI Functions agent.

Install libraries which are required to run this example notebook:

```bash
pip install -q openai langchain yfinance  

```

## Define custom functions[​](#define-custom-functions "Direct link to Define custom functions")

```python
import yfinance as yf  
from datetime import datetime, timedelta  
  
  
def get\_current\_stock\_price(ticker):  
 """Method to get current stock price"""  
  
 ticker\_data = yf.Ticker(ticker)  
 recent = ticker\_data.history(period="1d")  
 return {"price": recent.iloc[0]["Close"], "currency": ticker\_data.info["currency"]}  
  
  
def get\_stock\_performance(ticker, days):  
 """Method to get stock price change in percentage"""  
  
 past\_date = datetime.today() - timedelta(days=days)  
 ticker\_data = yf.Ticker(ticker)  
 history = ticker\_data.history(start=past\_date)  
 old\_price = history.iloc[0]["Close"]  
 current\_price = history.iloc[-1]["Close"]  
 return {"percent\_change": ((current\_price - old\_price) / old\_price) \* 100}  

```

```python
get\_current\_stock\_price("MSFT")  

```

```text
 {'price': 334.57000732421875, 'currency': 'USD'}  

```

```python
get\_stock\_performance("MSFT", 30)  

```

```text
 {'percent\_change': 1.014466941163018}  

```

## Make custom tools[​](#make-custom-tools "Direct link to Make custom tools")

```python
from typing import Type  
from pydantic import BaseModel, Field  
from langchain.tools import BaseTool  
  
  
class CurrentStockPriceInput(BaseModel):  
 """Inputs for get\_current\_stock\_price"""  
  
 ticker: str = Field(description="Ticker symbol of the stock")  
  
  
class CurrentStockPriceTool(BaseTool):  
 name = "get\_current\_stock\_price"  
 description = """  
 Useful when you want to get current stock price.  
 You should enter the stock ticker symbol recognized by the yahoo finance  
 """  
 args\_schema: Type[BaseModel] = CurrentStockPriceInput  
  
 def \_run(self, ticker: str):  
 price\_response = get\_current\_stock\_price(ticker)  
 return price\_response  
  
 def \_arun(self, ticker: str):  
 raise NotImplementedError("get\_current\_stock\_price does not support async")  
  
  
class StockPercentChangeInput(BaseModel):  
 """Inputs for get\_stock\_performance"""  
  
 ticker: str = Field(description="Ticker symbol of the stock")  
 days: int = Field(description="Timedelta days to get past date from current date")  
  
  
class StockPerformanceTool(BaseTool):  
 name = "get\_stock\_performance"  
 description = """  
 Useful when you want to check performance of the stock.  
 You should enter the stock ticker symbol recognized by the yahoo finance.  
 You should enter days as number of days from today from which performance needs to be check.  
 output will be the change in the stock price represented as a percentage.  
 """  
 args\_schema: Type[BaseModel] = StockPercentChangeInput  
  
 def \_run(self, ticker: str, days: int):  
 response = get\_stock\_performance(ticker, days)  
 return response  
  
 def \_arun(self, ticker: str):  
 raise NotImplementedError("get\_stock\_performance does not support async")  

```

## Create Agent[​](#create-agent "Direct link to Create Agent")

```python
from langchain.agents import AgentType  
from langchain.chat\_models import ChatOpenAI  
from langchain.agents import initialize\_agent  
  
llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)  
  
tools = [CurrentStockPriceTool(), StockPerformanceTool()]  
  
agent = initialize\_agent(tools, llm, agent=AgentType.OPENAI\_FUNCTIONS, verbose=True)  

```

```python
agent.run(  
 "What is the current price of Microsoft stock? How it has performed over past 6 months?"  
)  

```

```text
   
   
 > Entering new chain...  
   
 Invoking: `get\_current\_stock\_price` with `{'ticker': 'MSFT'}`  
   
   
 {'price': 334.57000732421875, 'currency': 'USD'}  
 Invoking: `get\_stock\_performance` with `{'ticker': 'MSFT', 'days': 180}`  
   
   
 {'percent\_change': 40.163963297187905}The current price of Microsoft stock is $334.57 USD.   
   
 Over the past 6 months, Microsoft stock has performed well with a 40.16% increase in its price.  
   
 > Finished chain.  
  
  
  
  
  
 'The current price of Microsoft stock is $334.57 USD. \n\nOver the past 6 months, Microsoft stock has performed well with a 40.16% increase in its price.'  

```

```python
agent.run("Give me recent stock prices of Google and Meta?")  

```

```text
   
   
 > Entering new chain...  
   
 Invoking: `get\_current\_stock\_price` with `{'ticker': 'GOOGL'}`  
   
   
 {'price': 118.33000183105469, 'currency': 'USD'}  
 Invoking: `get\_current\_stock\_price` with `{'ticker': 'META'}`  
   
   
 {'price': 287.04998779296875, 'currency': 'USD'}The recent stock price of Google (GOOGL) is $118.33 USD and the recent stock price of Meta (META) is $287.05 USD.  
   
 > Finished chain.  
  
  
  
  
  
 'The recent stock price of Google (GOOGL) is $118.33 USD and the recent stock price of Meta (META) is $287.05 USD.'  

```

```python
agent.run(  
 "In the past 3 months, which stock between Microsoft and Google has performed the best?"  
)  

```

```text
   
   
 > Entering new chain...  
   
 Invoking: `get\_stock\_performance` with `{'ticker': 'MSFT', 'days': 90}`  
   
   
 {'percent\_change': 18.043096235165596}  
 Invoking: `get\_stock\_performance` with `{'ticker': 'GOOGL', 'days': 90}`  
   
   
 {'percent\_change': 17.286155760642853}In the past 3 months, Microsoft (MSFT) has performed better than Google (GOOGL). Microsoft's stock price has increased by 18.04% while Google's stock price has increased by 17.29%.  
   
 > Finished chain.  
  
  
  
  
  
 "In the past 3 months, Microsoft (MSFT) has performed better than Google (GOOGL). Microsoft's stock price has increased by 18.04% while Google's stock price has increased by 17.29%."  

```

- [Define custom functions](#define-custom-functions)
- [Make custom tools](#make-custom-tools)
- [Create Agent](#create-agent)

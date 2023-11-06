# Yahoo Finance News

This notebook goes over how to use the `yahoo_finance_news` tool with an agent.

## Setting up[​](#setting-up "Direct link to Setting up")

First, you need to install `yfinance` python package.

```bash
pip install yfinance  

```

## Example with Chain[​](#example-with-chain "Direct link to Example with Chain")

```python
import os  
  
os.environ["OPENAI\_API\_KEY"] = "..."  

```

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.agents import initialize\_agent, AgentType  
from langchain.tools.yahoo\_finance\_news import YahooFinanceNewsTool  
   
  
llm = ChatOpenAI(temperature=0.0)  
tools = [YahooFinanceNewsTool()]  
agent\_chain = initialize\_agent(  
 tools,  
 llm,  
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
)  

```

```python
agent\_chain.run(  
 "What happens today with Microsoft stocks?",  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I should check the latest financial news about Microsoft stocks.  
 Action: yahoo\_finance\_news  
 Action Input: MSFT  
 Observation: Microsoft (MSFT) Gains But Lags Market: What You Should Know  
 In the latest trading session, Microsoft (MSFT) closed at $328.79, marking a +0.12% move from the previous day.  
 Thought:I have the latest information on Microsoft stocks.  
 Final Answer: Microsoft (MSFT) closed at $328.79, with a +0.12% move from the previous day.  
   
 > Finished chain.  
  
  
  
  
  
 'Microsoft (MSFT) closed at $328.79, with a +0.12% move from the previous day.'  

```

```python
agent\_chain.run(  
 "How does Microsoft feels today comparing with Nvidia?",  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I should compare the current sentiment of Microsoft and Nvidia.  
 Action: yahoo\_finance\_news  
 Action Input: MSFT  
 Observation: Microsoft (MSFT) Gains But Lags Market: What You Should Know  
 In the latest trading session, Microsoft (MSFT) closed at $328.79, marking a +0.12% move from the previous day.  
 Thought:I need to find the current sentiment of Nvidia as well.  
 Action: yahoo\_finance\_news  
 Action Input: NVDA  
 Observation:   
 Thought:I now know the current sentiment of both Microsoft and Nvidia.  
 Final Answer: I cannot compare the sentiment of Microsoft and Nvidia as I only have information about Microsoft.  
   
 > Finished chain.  
  
  
  
  
  
 'I cannot compare the sentiment of Microsoft and Nvidia as I only have information about Microsoft.'  

```

# How YahooFinanceNewsTool works?

```python
tool = YahooFinanceNewsTool()  

```

```python
tool.run("NVDA")  

```

```text
 'No news found for company that searched with NVDA ticker.'  

```

```python
res = tool.run("AAPL")  
print(res)  

```

```text
 Top Research Reports for Apple, Broadcom & Caterpillar  
 Today's Research Daily features new research reports on 16 major stocks, including Apple Inc. (AAPL), Broadcom Inc. (AVGO) and Caterpillar Inc. (CAT).  
   
 Apple Stock on Pace for Worst Month of the Year  
 Apple (AAPL) shares are on pace for their worst month of the year, according to Dow Jones Market Data. The stock is down 4.8% so far in August, putting it on pace for its worst month since December 2022, when it fell 12%.  

```

- [Setting up](#setting-up)
- [Example with Chain](#example-with-chain)

# Using tools

You can use any Tools with Runnables easily.

```bash
pip install duckduckgo-search  

```

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate  
from langchain.schema.output\_parser import StrOutputParser  
from langchain.tools import DuckDuckGoSearchRun  

```

```python
search = DuckDuckGoSearchRun()  

```

```python
template = """turn the following user input into a search query for a search engine:  
  
{input}"""  
prompt = ChatPromptTemplate.from\_template(template)  
  
model = ChatOpenAI()  

```

```python
chain = prompt | model | StrOutputParser() | search  

```

```python
chain.invoke({"input": "I'd like to figure out what games are tonight"})  

```

```text
 'What sports games are on TV today & tonight? Watch and stream live sports on TV today, tonight, tomorrow. Today\'s 2023 sports TV schedule includes football, basketball, baseball, hockey, motorsports, soccer and more. Watch on TV or stream online on ESPN, FOX, FS1, CBS, NBC, ABC, Peacock, Paramount+, fuboTV, local channels and many other networks. MLB Games Tonight: How to Watch on TV, Streaming & Odds - Thursday, September 7. Seattle Mariners\' Julio Rodriguez greets teammates in the dugout after scoring against the Oakland Athletics in a ... Circle - Country Music and Lifestyle. Live coverage of all the MLB action today is available to you, with the information provided below. The Brewers will look to pick up a road win at PNC Park against the Pirates on Wednesday at 12:35 PM ET. Check out the latest odds and with BetMGM Sportsbook. Use bonus code "GNPLAY" for special offers! MLB Games Tonight: How to Watch on TV, Streaming & Odds - Tuesday, September 5. Houston Astros\' Kyle Tucker runs after hitting a double during the fourth inning of a baseball game against the Los Angeles Angels, Sunday, Aug. 13, 2023, in Houston. (AP Photo/Eric Christian Smith) (APMedia) The Houston Astros versus the Texas Rangers is one of ... The second half of tonight\'s college football schedule still has some good games remaining to watch on your television.. We\'ve already seen an exciting one when Colorado upset TCU. And we saw some ...'  

```

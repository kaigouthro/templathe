# Fireworks

[Fireworks](https://app.fireworks.ai/) accelerates product development on generative AI by creating an innovative AI experiment and production platform.

This example goes over how to use LangChain to interact with `Fireworks` models.

```python
from langchain.llms.fireworks import Fireworks  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
from langchain.prompts.chat import (  
 ChatPromptTemplate,  
 HumanMessagePromptTemplate,  
)  
import os  

```

# Setup

1. Make sure the `fireworks-ai` package is installed in your environment.
1. Sign in to [Fireworks AI](http://fireworks.ai) for the an API Key to access our models, and make sure it is set as the `FIREWORKS_API_KEY` environment variable.
1. Set up your model using a model id. If the model is not set, the default model is fireworks-llama-v2-7b-chat. See the full, most up-to-date model list on [app.fireworks.ai](https://app.fireworks.ai).

```python
import os  
import getpass  
  
if "FIREWORKS\_API\_KEY" not in os.environ:  
 os.environ["FIREWORKS\_API\_KEY"] = getpass.getpass("Fireworks API Key:")  
  
# Initialize a Fireworks model  
llm = Fireworks(model="accounts/fireworks/models/llama-v2-13b")  

```

# Calling the Model Directly

You can call the model directly with string prompts to get completions.

```python
# Single prompt  
output = llm("Who's the best quarterback in the NFL?")  
print(output)  

```

```text
   
   
 Is it Tom Brady? Peyton Manning? Aaron Rodgers? Or maybe even Andrew Luck?  
   
 Well, let's look at some stats to decide.  
   
 First, let's talk about touchdowns. Who's thrown the most touchdowns this season?  
   
 (pause for dramatic effect)  
   
 It's... Aaron Rodgers! With 28 touchdowns, he's leading the league in that category.  
   
 But what about interceptions? Who's thrown the fewest picks?  
   
 (drumroll)  
   
 It's... Tom Brady! With only 4 interceptions, he's got the fewest picks in the league.  
   
 Now, let's talk about passer rating. Who's got the highest passer rating this season?  
   
 (pause for suspense)  
   
 It's... Peyton Manning! With a rating of 114.2, he's been lights out this season.  
   
 But what about wins? Who's got the most wins this season?  
   
 (drumroll)  
   
 It's... Andrew Luck! With 8 wins, he's got the most victories this season.  
   
 So, there you have it folks. According to these stats, the best quarterback in the NFL this season is... (drumroll) Aaron Rodgers!  
   
 But wait, there's more! Each of these quarterbacks has their own unique strengths and weaknesses.  
   
 Tom Brady is a master of the short pass, but can struggle with deep balls. Peyton Manning is a genius at reading defenses, but can be prone to turnovers. Aaron Rodgers has a cannon for an arm, but can be inconsistent at times. Andrew Luck is a pure pocket passer, but can struggle outside of his comfort zone.  
   
 So, who's the best quarterback in the NFL? It's a tough call, but one thing's for sure: each of these quarterbacks is an elite talent, and they'll continue to light up the scoreboard for their respective teams all season long.  

```

```python
# Calling multiple prompts  
output = llm.generate([  
 "Who's the best cricket player in 2016?",  
 "Who's the best basketball player in the league?",  
])  
print(output.generations)  

```

```text
 [[Generation(text='\nasked Dec 28, 2016 in Sports by anonymous\nWho is the best cricket player in 2016?\nHere are some of the top contenders for the title of best cricket player in 2016:\n\n1. Virat Kohli (India): Kohli had a phenomenal year in 2016, scoring over 2,000 runs in international cricket, including 12 centuries. He was named the ICC Cricketer of the Year and the ICC Test Player of the Year.\n2. Steve Smith (Australia): Smith had a great year as well, scoring over 1,000 runs in Test cricket and leading Australia to the No. 1 ranking in Test cricket. He was named the ICC ODI Player of the Year.\n3. Joe Root (England): Root had a strong year, scoring over 1,000 runs in Test cricket and leading England to the No. 2 ranking in Test cricket.\n4. Kane Williamson (New Zealand): Williamson had a great year, scoring over 1,000 runs in all formats of the game and leading New Zealand to the ICC World T20 final.\n5. Quinton de Kock (South Africa): De Kock had a great year behind the wickets, scoring over 1,000 runs in all formats of the game and effecting over 100 dismissals.\n6. David Warner (Australia): Warner had a great year, scoring over 1,000 runs in all formats of the game and leading Australia to the ICC World T20 title.\n7. AB de Villiers (South Africa): De Villiers had a great year, scoring over 1,000 runs in all formats of the game and effecting over 50 dismissals.\n8. Chris Gayle (West Indies): Gayle had a great year, scoring over 1,000 runs in all formats of the game and leading the West Indies to the ICC World T20 title.\n9. Shakib Al Hasan (Bangladesh): Shakib had a great year, scoring over 1,000 runs in all formats of the game and taking over 50 wickets.\n10', generation\_info=None)], [Generation(text="\n\n A) LeBron James\n B) Kevin Durant\n C) Steph Curry\n D) James Harden\n\nAnswer: C) Steph Curry\n\nIn recent years, Curry has established himself as the premier shooter in the NBA, leading the league in three-point shooting and earning back-to-back MVP awards. He's also a strong ball handler and playmaker, making him a threat to score from anywhere on the court. While other players like LeBron James and Kevin Durant are certainly talented, Curry's unique skill set and consistent dominance make him the best basketball player in the league right now.", generation\_info=None)]]  

```

```python
# Setting additional parameters: temperature, max\_tokens, top\_p  
llm = Fireworks(model="accounts/fireworks/models/llama-v2-13b-chat", model\_kwargs={"temperature":0.7, "max\_tokens":15, "top\_p":1.0})  
print(llm("What's the weather like in Kansas City in December?"))  

```

```text
   
 What's the weather like in Kansas City in December?   

```

# Simple Chain with Non-Chat Model

You can use the LangChain Expression Language to create a simple chain with non-chat models.

```python
from langchain.prompts import PromptTemplate  
from langchain.llms.fireworks import Fireworks  
  
llm = Fireworks(model="accounts/fireworks/models/llama-v2-13b", model\_kwargs={"temperature":0, "max\_tokens":100, "top\_p":1.0})  
prompt = PromptTemplate.from\_template("Tell me a joke about {topic}?")  
chain = prompt | llm  
  
print(chain.invoke({"topic": "bears"}))  

```

```text
   
 A bear walks into a bar and says, "I'll have a beer and a muffin." The bartender says, "Sorry, we don't serve muffins here." The bear says, "OK, give me a beer and I'll make my own muffin."  
 What do you call a bear with no teeth?  
 A gummy bear.  
 What do you call a bear with no teeth and no hair?  
   

```

You can stream the output, if you want.

```python
for token in chain.stream({"topic": "bears"}):  
 print(token, end='', flush=True)  

```

```text
   
 A bear walks into a bar and says, "I'll have a beer and a muffin." The bartender says, "Sorry, we don't serve muffins here." The bear says, "OK, give me a beer and I'll make my own muffin."  
 What do you call a bear with no teeth?  
 A gummy bear.  
 What do you call a bear with no teeth and no hair?  

```

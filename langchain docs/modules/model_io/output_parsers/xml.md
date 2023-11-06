# XML parser

This output parser allows users to obtain results from LLM in the popular XML format.

Keep in mind that large language models are leaky abstractions! You'll have to use an LLM with sufficient capacity to generate well-formed XML.

In the following example we use Claude model (<https://docs.anthropic.com/claude/docs>) which works really well with XML tags.

```python
from langchain.prompts import PromptTemplate  
from langchain.llms import Anthropic  
from langchain.output\_parsers import XMLOutputParser  

```

```python
model = Anthropic(model="claude-2", max\_tokens\_to\_sample=512, temperature=0.1)  

```

```text
 /Users/harrisonchase/workplace/langchain/libs/langchain/langchain/llms/anthropic.py:171: UserWarning: This Anthropic LLM is deprecated. Please use `from langchain.chat\_models import ChatAnthropic` instead  
 warnings.warn(  

```

Let's start with the simple request to the model.

```python
actor\_query = "Generate the shortened filmography for Tom Hanks."  
output = model(  
 f"""  
  
Human:  
{actor\_query}  
Please enclose the movies in <movie></movie> tags  
Assistant:  
"""  
)  
print(output)  

```

```text
 Here is the shortened filmography for Tom Hanks enclosed in <movie> tags:  
   
 <movie>Splash (1984)</movie>  
 <movie>Big (1988)</movie>   
 <movie>A League of Their Own (1992)</movie>  
 <movie>Sleepless in Seattle (1993)</movie>   
 <movie>Forrest Gump (1994)</movie>  
 <movie>Apollo 13 (1995)</movie>  
 <movie>Toy Story (1995)</movie>  
 <movie>Saving Private Ryan (1998)</movie>  
 <movie>Cast Away (2000)</movie>  
 <movie>The Da Vinci Code (2006)</movie>  
 <movie>Toy Story 3 (2010)</movie>  
 <movie>Captain Phillips (2013)</movie>  
 <movie>Bridge of Spies (2015)</movie>  
 <movie>Toy Story 4 (2019)</movie>  

```

Now we will use the XMLOutputParser in order to get the structured output.

```python
parser = XMLOutputParser()  
  
prompt = PromptTemplate(  
 template="""  
   
 Human:  
 {query}  
 {format\_instructions}  
 Assistant:""",  
 input\_variables=["query"],  
 partial\_variables={"format\_instructions": parser.get\_format\_instructions()},  
)  
  
chain = prompt | model | parser  
  
output = chain.invoke({"query": actor\_query})  
print(output)  

```

```text
 {'filmography': [{'movie': [{'title': 'Splash'}, {'year': '1984'}]}, {'movie': [{'title': 'Big'}, {'year': '1988'}]}, {'movie': [{'title': 'A League of Their Own'}, {'year': '1992'}]}, {'movie': [{'title': 'Sleepless in Seattle'}, {'year': '1993'}]}, {'movie': [{'title': 'Forrest Gump'}, {'year': '1994'}]}, {'movie': [{'title': 'Toy Story'}, {'year': '1995'}]}, {'movie': [{'title': 'Apollo 13'}, {'year': '1995'}]}, {'movie': [{'title': 'Saving Private Ryan'}, {'year': '1998'}]}, {'movie': [{'title': 'Cast Away'}, {'year': '2000'}]}, {'movie': [{'title': 'Catch Me If You Can'}, {'year': '2002'}]}, {'movie': [{'title': 'The Polar Express'}, {'year': '2004'}]}, {'movie': [{'title': 'Bridge of Spies'}, {'year': '2015'}]}]}  

```

Finally, let's add some tags to tailor the output to our needs.

```python
parser = XMLOutputParser(tags=["movies", "actor", "film", "name", "genre"])  
prompt = PromptTemplate(  
 template="""  
   
 Human:  
 {query}  
 {format\_instructions}  
 Assistant:""",  
 input\_variables=["query"],  
 partial\_variables={"format\_instructions": parser.get\_format\_instructions()},  
)  
  
  
chain = prompt | model | parser  
  
output = chain.invoke({"query": actor\_query})  
  
print(output)  

```

```text
 {'movies': [{'actor': [{'name': 'Tom Hanks'}, {'film': [{'name': 'Splash'}, {'genre': 'Comedy'}]}, {'film': [{'name': 'Big'}, {'genre': 'Comedy'}]}, {'film': [{'name': 'A League of Their Own'}, {'genre': 'Comedy'}]}, {'film': [{'name': 'Sleepless in Seattle'}, {'genre': 'Romance'}]}, {'film': [{'name': 'Forrest Gump'}, {'genre': 'Drama'}]}, {'film': [{'name': 'Toy Story'}, {'genre': 'Animation'}]}, {'film': [{'name': 'Apollo 13'}, {'genre': 'Drama'}]}, {'film': [{'name': 'Saving Private Ryan'}, {'genre': 'War'}]}, {'film': [{'name': 'Cast Away'}, {'genre': 'Adventure'}]}, {'film': [{'name': 'The Green Mile'}, {'genre': 'Drama'}]}]}]}  

```

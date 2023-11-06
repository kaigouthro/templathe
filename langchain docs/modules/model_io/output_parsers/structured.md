# Structured output parser

This output parser can be used when you want to return multiple fields. While the Pydantic/JSON parser is more powerful, we initially experimented with data structures having text fields only.

```python
from langchain.output\_parsers import StructuredOutputParser, ResponseSchema  
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate  
from langchain.llms import OpenAI  
from langchain.chat\_models import ChatOpenAI  

```

Here we define the response schema we want to receive.

```python
response\_schemas = [  
 ResponseSchema(name="answer", description="answer to the user's question"),  
 ResponseSchema(name="source", description="source used to answer the user's question, should be a website.")  
]  
output\_parser = StructuredOutputParser.from\_response\_schemas(response\_schemas)  

```

We now get a string that contains instructions for how the response should be formatted, and we then insert that into our prompt.

```python
format\_instructions = output\_parser.get\_format\_instructions()  
prompt = PromptTemplate(  
 template="answer the users question as best as possible.\n{format\_instructions}\n{question}",  
 input\_variables=["question"],  
 partial\_variables={"format\_instructions": format\_instructions}  
)  

```

We can now use this to format a prompt to send to the language model, and then parse the returned result.

```python
model = OpenAI(temperature=0)  

```

```python
\_input = prompt.format\_prompt(question="what's the capital of france?")  
output = model(\_input.to\_string())  

```

```python
output\_parser.parse(output)  

```

```text
 {'answer': 'Paris',  
 'source': 'https://www.worldatlas.com/articles/what-is-the-capital-of-france.html'}  

```

And here's an example of using this in a chat model

```python
chat\_model = ChatOpenAI(temperature=0)  

```

```python
prompt = ChatPromptTemplate(  
 messages=[  
 HumanMessagePromptTemplate.from\_template("answer the users question as best as possible.\n{format\_instructions}\n{question}")  
 ],  
 input\_variables=["question"],  
 partial\_variables={"format\_instructions": format\_instructions}  
)  

```

```python
\_input = prompt.format\_prompt(question="what's the capital of france?")  
output = chat\_model(\_input.to\_messages())  

```

```python
output\_parser.parse(output.content)  

```

```text
 {'answer': 'Paris', 'source': 'https://en.wikipedia.org/wiki/Paris'}  

```

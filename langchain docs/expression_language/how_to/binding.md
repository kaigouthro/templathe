# Bind runtime args

Sometimes we want to invoke a Runnable within a Runnable sequence with constant arguments that are not part of the output of the preceding Runnable in the sequence, and which are not part of the user input. We can use `Runnable.bind()` to easily pass these arguments in.

Suppose we have a simple prompt + model sequence:

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate  
from langchain.schema import StrOutputParser  
from langchain.schema.runnable import RunnablePassthrough  
  
prompt = ChatPromptTemplate.from\_messages(  
 [  
 ("system", "Write out the following equation using algebraic symbols then solve it. Use the format\n\nEQUATION:...\nSOLUTION:...\n\n"),  
 ("human", "{equation\_statement}")  
 ]  
)  
model = ChatOpenAI(temperature=0)  
runnable = {"equation\_statement": RunnablePassthrough()} | prompt | model | StrOutputParser()  
  
print(runnable.invoke("x raised to the third plus seven equals 12"))  

```

```text
 EQUATION: x^3 + 7 = 12  
   
 SOLUTION:  
 Subtracting 7 from both sides of the equation, we get:  
 x^3 = 12 - 7  
 x^3 = 5  
   
 Taking the cube root of both sides, we get:  
 x = ∛5  
   
 Therefore, the solution to the equation x^3 + 7 = 12 is x = ∛5.  

```

and want to call the model with certain `stop` words:

```python
runnable = (  
 {"equation\_statement": RunnablePassthrough()}   
 | prompt   
 | model.bind(stop="SOLUTION")   
 | StrOutputParser()  
)  
print(runnable.invoke("x raised to the third plus seven equals 12"))  

```

```text
 EQUATION: x^3 + 7 = 12  
   
   

```

## Attaching OpenAI functions[​](#attaching-openai-functions "Direct link to Attaching OpenAI functions")

One particularly useful application of binding is to attach OpenAI functions to a compatible OpenAI model:

```python
functions = [  
 {  
 "name": "solver",  
 "description": "Formulates and solves an equation",  
 "parameters": {  
 "type": "object",  
 "properties": {  
 "equation": {  
 "type": "string",  
 "description": "The algebraic expression of the equation"  
 },  
 "solution": {  
 "type": "string",  
 "description": "The solution to the equation"  
 }  
 },  
 "required": ["equation", "solution"]  
 }  
 }  
 ]  

```

```python
# Need gpt-4 to solve this one correctly  
prompt = ChatPromptTemplate.from\_messages(  
 [  
 ("system", "Write out the following equation using algebraic symbols then solve it."),  
 ("human", "{equation\_statement}")  
 ]  
)  
model = ChatOpenAI(model="gpt-4", temperature=0).bind(function\_call={"name": "solver"}, functions=functions)  
runnable = (  
 {"equation\_statement": RunnablePassthrough()}   
 | prompt   
 | model  
)  
runnable.invoke("x raised to the third plus seven equals 12")  

```

```text
 AIMessage(content='', additional\_kwargs={'function\_call': {'name': 'solver', 'arguments': '{\n"equation": "x^3 + 7 = 12",\n"solution": "x = ∛5"\n}'}}, example=False)  

```

- [Attaching OpenAI functions](#attaching-openai-functions)

# Multiple chains

Runnables can easily be used to string together multiple Chains

```python
from operator import itemgetter  
  
from langchain.chat\_models import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate  
from langchain.schema import StrOutputParser  
  
prompt1 = ChatPromptTemplate.from\_template("what is the city {person} is from?")  
prompt2 = ChatPromptTemplate.from\_template("what country is the city {city} in? respond in {language}")  
  
model = ChatOpenAI()  
  
chain1 = prompt1 | model | StrOutputParser()  
  
chain2 = {"city": chain1, "language": itemgetter("language")} | prompt2 | model | StrOutputParser()  
  
chain2.invoke({"person": "obama", "language": "spanish"})  

```

```text
 'El país donde se encuentra la ciudad de Honolulu, donde nació Barack Obama, el 44º Presidente de los Estados Unidos, es Estados Unidos. Honolulu se encuentra en la isla de Oahu, en el estado de Hawái.'  

```

```python
from langchain.schema.runnable import RunnableMap, RunnablePassthrough  
  
prompt1 = ChatPromptTemplate.from\_template("generate a {attribute} color. Return the name of the color and nothing else:")  
prompt2 = ChatPromptTemplate.from\_template("what is a fruit of color: {color}. Return the name of the fruit and nothing else:")  
prompt3 = ChatPromptTemplate.from\_template("what is a country with a flag that has the color: {color}. Return the name of the country and nothing else:")  
prompt4 = ChatPromptTemplate.from\_template("What is the color of {fruit} and the flag of {country}?")  
  
model\_parser = model | StrOutputParser()  
  
color\_generator = {"attribute": RunnablePassthrough()} | prompt1 | {"color": model\_parser}  
color\_to\_fruit = prompt2 | model\_parser  
color\_to\_country = prompt3 | model\_parser  
question\_generator = color\_generator | {"fruit": color\_to\_fruit, "country": color\_to\_country} | prompt4  

```

```python
question\_generator.invoke("warm")  

```

```text
 ChatPromptValue(messages=[HumanMessage(content='What is the color of strawberry and the flag of China?', additional\_kwargs={}, example=False)])  

```

```python
prompt = question\_generator.invoke("warm")  
model.invoke(prompt)  

```

```text
 AIMessage(content='The color of an apple is typically red or green. The flag of China is predominantly red with a large yellow star in the upper left corner and four smaller yellow stars surrounding it.', additional\_kwargs={}, example=False)  

```

### Branching and Merging[​](#branching-and-merging "Direct link to Branching and Merging")

You may want the output of one component to be processed by 2 or more other components. [RunnableMaps](https://api.python.langchain.com/en/latest/schema/langchain.schema.runnable.base.RunnableMap.html) let you split or fork the chain so multiple components can process the input in parallel. Later, other components can join or merge the results to synthesize a final response. This type of chain creates a computation graph that looks like the following:

```text
 Input  
 / \  
 / \  
 Branch1 Branch2  
 \ /  
 \ /  
 Combine  

```

```python
planner = (  
 ChatPromptTemplate.from\_template(  
 "Generate an argument about: {input}"  
 )  
 | ChatOpenAI()  
 | StrOutputParser()  
 | {"base\_response": RunnablePassthrough()}  
)  
  
arguments\_for = (  
 ChatPromptTemplate.from\_template(  
 "List the pros or positive aspects of {base\_response}"  
 )  
 | ChatOpenAI()  
 | StrOutputParser()  
)  
arguments\_against = (  
 ChatPromptTemplate.from\_template(  
 "List the cons or negative aspects of {base\_response}"  
 )  
 | ChatOpenAI()  
 | StrOutputParser()  
)  
  
final\_responder = (  
 ChatPromptTemplate.from\_messages(  
 [  
 ("ai", "{original\_response}"),  
 ("human", "Pros:\n{results\_1}\n\nCons:\n{results\_2}"),  
 ("system", "Generate a final response given the critique"),  
 ]  
 )  
 | ChatOpenAI()  
 | StrOutputParser()  
)  
  
chain = (  
 planner   
 | {  
 "results\_1": arguments\_for,  
 "results\_2": arguments\_against,  
 "original\_response": itemgetter("base\_response"),  
 }  
 | final\_responder  
)  

```

```python
chain.invoke({"input": "scrum"})  

```

```text
 'While Scrum has its potential cons and challenges, many organizations have successfully embraced and implemented this project management framework to great effect. The cons mentioned above can be mitigated or overcome with proper training, support, and a commitment to continuous improvement. It is also important to note that not all cons may be applicable to every organization or project.\n\nFor example, while Scrum may be complex initially, with proper training and guidance, teams can quickly grasp the concepts and practices. The lack of predictability can be mitigated by implementing techniques such as velocity tracking and release planning. The limited documentation can be addressed by maintaining a balance between lightweight documentation and clear communication among team members. The dependency on team collaboration can be improved through effective communication channels and regular team-building activities.\n\nScrum can be scaled and adapted to larger projects by using frameworks like Scrum of Scrums or LeSS (Large Scale Scrum). Concerns about speed versus quality can be addressed by incorporating quality assurance practices, such as continuous integration and automated testing, into the Scrum process. Scope creep can be managed by having a well-defined and prioritized product backlog, and a strong product owner can be developed through training and mentorship.\n\nResistance to change can be overcome by providing proper education and communication to stakeholders and involving them in the decision-making process. Ultimately, the cons of Scrum can be seen as opportunities for growth and improvement, and with the right mindset and support, they can be effectively managed.\n\nIn conclusion, while Scrum may have its challenges and potential cons, the benefits and advantages it offers in terms of collaboration, flexibility, adaptability, transparency, and customer satisfaction make it a widely adopted and successful project management framework. With proper implementation and continuous improvement, organizations can leverage Scrum to drive innovation, efficiency, and project success.'  

```

- [Branching and Merging](#branching-and-merging)

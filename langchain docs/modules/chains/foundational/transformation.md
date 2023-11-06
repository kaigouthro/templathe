# Transformation

Often we want to transform inputs as they are passed from one component to another.

As an example, we will create a dummy transformation that takes in a super long text, filters the text to only the first 3 paragraphs, and then passes that into a chain to summarize those.

```python
from langchain.prompts import PromptTemplate  
  
prompt = PromptTemplate.from\_template(  
 """Summarize this text:  
  
{output\_text}  
  
Summary:"""  
)  

```

```python
with open("../../state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  

```

## Using LCEL[​](#using-lcel "Direct link to Using LCEL")

With LCEL this is trivial, since we can add functions in any `RunnableSequence`.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import StrOutputParser  
  
runnable = {"output\_text": lambda text: "\n\n".join(text.split("\n\n")[:3])} | prompt | ChatOpenAI() | StrOutputParser()  
runnable.invoke(state\_of\_the\_union)  

```

```text
 'The speaker acknowledges the presence of important figures in the government and addresses the audience as fellow Americans. They highlight the impact of COVID-19 on keeping people apart in the previous year but express joy in being able to come together again. The speaker emphasizes the unity of Democrats, Republicans, and Independents as Americans.'  

```

## \[Legacy\] TransformationChain[​](#legacy-transformationchain "Direct link to legacy-transformationchain")

This notebook showcases using a generic transformation chain.

```python
from langchain.chains import TransformChain, LLMChain, SimpleSequentialChain  
from langchain.llms import OpenAI  

```

```python
def transform\_func(inputs: dict) -> dict:  
 text = inputs["text"]  
 shortened\_text = "\n\n".join(text.split("\n\n")[:3])  
 return {"output\_text": shortened\_text}  
  
transform\_chain = TransformChain(  
 input\_variables=["text"], output\_variables=["output\_text"], transform=transform\_func  
)  

```

```python
template = """Summarize this text:  
  
{output\_text}  
  
Summary:"""  
prompt = PromptTemplate(input\_variables=["output\_text"], template=template)  
llm\_chain = LLMChain(llm=OpenAI(), prompt=prompt)  

```

```python
sequential\_chain = SimpleSequentialChain(chains=[transform\_chain, llm\_chain])  

```

```python
sequential\_chain.run(state\_of\_the\_union)  

```

```text
 ' In an address to the nation, the speaker acknowledges the hardships of the past year due to the COVID-19 pandemic, but emphasizes that regardless of political affiliation, all Americans can come together.'  

```

- [Using LCEL](#using-lcel)
- [Legacy TransformationChain](#legacy-transformationchain)

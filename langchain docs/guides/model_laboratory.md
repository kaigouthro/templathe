# Model comparison

Constructing your language model application will likely involved choosing between many different options of prompts, models, and even chains to use. When doing so, you will want to compare these different options on different inputs in an easy, flexible, and intuitive way.

LangChain provides the concept of a ModelLaboratory to test out and try different models.

```python
from langchain.chains import LLMChain  
from langchain.llms import OpenAI, Cohere, HuggingFaceHub  
from langchain.prompts import PromptTemplate  
from langchain.model\_laboratory import ModelLaboratory  

```

```python
llms = [  
 OpenAI(temperature=0),  
 Cohere(model="command-xlarge-20221108", max\_tokens=20, temperature=0),  
 HuggingFaceHub(repo\_id="google/flan-t5-xl", model\_kwargs={"temperature": 1}),  
]  

```

```python
model\_lab = ModelLaboratory.from\_llms(llms)  

```

```python
model\_lab.compare("What color is a flamingo?")  

```

```text
 Input:  
 What color is a flamingo?  
   
 OpenAI  
 Params: {'model': 'text-davinci-002', 'temperature': 0.0, 'max\_tokens': 256, 'top\_p': 1, 'frequency\_penalty': 0, 'presence\_penalty': 0, 'n': 1, 'best\_of': 1}  
   
   
 Flamingos are pink.  
   
 Cohere  
 Params: {'model': 'command-xlarge-20221108', 'max\_tokens': 20, 'temperature': 0.0, 'k': 0, 'p': 1, 'frequency\_penalty': 0, 'presence\_penalty': 0}  
   
   
 Pink  
   
 HuggingFaceHub  
 Params: {'repo\_id': 'google/flan-t5-xl', 'temperature': 1}  
 pink  
   

```

```python
prompt = PromptTemplate(  
 template="What is the capital of {state}?", input\_variables=["state"]  
)  
model\_lab\_with\_prompt = ModelLaboratory.from\_llms(llms, prompt=prompt)  

```

```python
model\_lab\_with\_prompt.compare("New York")  

```

```text
 Input:  
 New York  
   
 OpenAI  
 Params: {'model': 'text-davinci-002', 'temperature': 0.0, 'max\_tokens': 256, 'top\_p': 1, 'frequency\_penalty': 0, 'presence\_penalty': 0, 'n': 1, 'best\_of': 1}  
   
   
 The capital of New York is Albany.  
   
 Cohere  
 Params: {'model': 'command-xlarge-20221108', 'max\_tokens': 20, 'temperature': 0.0, 'k': 0, 'p': 1, 'frequency\_penalty': 0, 'presence\_penalty': 0}  
   
   
 The capital of New York is Albany.  
   
 HuggingFaceHub  
 Params: {'repo\_id': 'google/flan-t5-xl', 'temperature': 1}  
 st john s  
   

```

```python
from langchain.chains import SelfAskWithSearchChain  
from langchain.utilities import SerpAPIWrapper  
  
open\_ai\_llm = OpenAI(temperature=0)  
search = SerpAPIWrapper()  
self\_ask\_with\_search\_openai = SelfAskWithSearchChain(  
 llm=open\_ai\_llm, search\_chain=search, verbose=True  
)  
  
cohere\_llm = Cohere(temperature=0, model="command-xlarge-20221108")  
search = SerpAPIWrapper()  
self\_ask\_with\_search\_cohere = SelfAskWithSearchChain(  
 llm=cohere\_llm, search\_chain=search, verbose=True  
)  

```

```python
chains = [self\_ask\_with\_search\_openai, self\_ask\_with\_search\_cohere]  
names = [str(open\_ai\_llm), str(cohere\_llm)]  

```

```python
model\_lab = ModelLaboratory(chains, names=names)  

```

```python
model\_lab.compare("What is the hometown of the reigning men's U.S. Open champion?")  

```

```text
 Input:  
 What is the hometown of the reigning men's U.S. Open champion?  
   
 OpenAI  
 Params: {'model': 'text-davinci-002', 'temperature': 0.0, 'max\_tokens': 256, 'top\_p': 1, 'frequency\_penalty': 0, 'presence\_penalty': 0, 'n': 1, 'best\_of': 1}  
   
   
 > Entering new chain...  
 What is the hometown of the reigning men's U.S. Open champion?  
 Are follow up questions needed here: Yes.  
 Follow up: Who is the reigning men's U.S. Open champion?  
 Intermediate answer: Carlos Alcaraz.  
 Follow up: Where is Carlos Alcaraz from?  
 Intermediate answer: El Palmar, Spain.  
 So the final answer is: El Palmar, Spain  
 > Finished chain.  
   
 So the final answer is: El Palmar, Spain  
   
 Cohere  
 Params: {'model': 'command-xlarge-20221108', 'max\_tokens': 256, 'temperature': 0.0, 'k': 0, 'p': 1, 'frequency\_penalty': 0, 'presence\_penalty': 0}  
   
   
 > Entering new chain...  
 What is the hometown of the reigning men's U.S. Open champion?  
 Are follow up questions needed here: Yes.  
 Follow up: Who is the reigning men's U.S. Open champion?  
 Intermediate answer: Carlos Alcaraz.  
 So the final answer is:  
   
 Carlos Alcaraz  
 > Finished chain.  
   
 So the final answer is:  
   
 Carlos Alcaraz  
   

```
